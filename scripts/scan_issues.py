#!/usr/bin/env python3
"""Scan GitHub issues and print actionable changes.

Usage:
  GITHUB_TOKEN=... python scripts/scan_issues.py --repo owner/name --state state/last-scan.json

Design:
- Read-only scan by default.
- Writes only local state file.
- Emits JSON with actionable changes.
- No-op scans should be logged locally by cron_tick.sh but must NOT be sent to the Octo group.
"""
from __future__ import annotations
import argparse, json, os, sys, time, urllib.request, urllib.error
from pathlib import Path

WATCH_LABEL_PREFIXES = ("type/", "priority/", "status/", "source/")

def gh_get(url: str, token: str) -> tuple[object, dict]:
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "octo-server-product-agent-exam",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {token}",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data, dict(resp.headers)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        if e.code in (403, 429):
            print(json.dumps({"ok": False, "blocked": "rate_limited_or_forbidden", "status": e.code, "body": body[:500]}, ensure_ascii=False))
            sys.exit(2)
        raise

def issue_snapshot(issue: dict) -> dict:
    labels = sorted(l["name"] for l in issue.get("labels", []) if any(l["name"].startswith(p) for p in WATCH_LABEL_PREFIXES))
    return {
        "number": issue["number"],
        "title": issue.get("title", ""),
        "state": issue.get("state", ""),
        "labels": labels,
        "updated_at": issue.get("updated_at", ""),
        "html_url": issue.get("html_url", ""),
    }

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="owner/name")
    ap.add_argument("--state", default="state/last-scan.json")
    ap.add_argument("--limit", type=int, default=100)
    args = ap.parse_args()
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print(json.dumps({"ok": False, "blocked": "missing_github_token"}, ensure_ascii=False))
        return 2
    state_path = Path(args.state)
    old = {}
    if state_path.exists():
        old = json.loads(state_path.read_text() or "{}")
    old_issues = {str(i["number"]): i for i in old.get("issues", [])}

    url = f"https://api.github.com/repos/{args.repo}/issues?state=all&per_page={min(args.limit,100)}&sort=updated&direction=desc"
    issues, headers = gh_get(url, token)
    snapshots = [issue_snapshot(i) for i in issues if "pull_request" not in i]
    changes = []
    for cur in snapshots:
        prev = old_issues.get(str(cur["number"]))
        if not prev:
            changes.append({"kind": "new_issue", "issue": cur})
            continue
        diffs = {}
        for key in ("state", "labels", "title"):
            if prev.get(key) != cur.get(key):
                diffs[key] = {"from": prev.get(key), "to": cur.get(key)}
        if diffs:
            changes.append({"kind": "issue_changed", "issue": cur, "diffs": diffs})

    new_state = {
        "repo": args.repo,
        "scanned_at": int(time.time()),
        "issues": snapshots,
        "rate": {
            "remaining": headers.get("X-RateLimit-Remaining"),
            "reset": headers.get("X-RateLimit-Reset"),
        },
    }
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(new_state, ensure_ascii=False, indent=2))
    print(json.dumps({"ok": True, "repo": args.repo, "scanned": len(snapshots), "changes": changes, "rate": new_state["rate"]}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
