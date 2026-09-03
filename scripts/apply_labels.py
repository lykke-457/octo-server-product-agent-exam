#!/usr/bin/env python3
"""Create/update GitHub labels from .github/labels.yml.

Usage:
  GITHUB_TOKEN=*** python scripts/apply_labels.py --repo owner/name

No third-party deps: parses the simple labels.yml shape used in this repo.
"""
from __future__ import annotations
import argparse, json, os, re, sys, urllib.request, urllib.error
from pathlib import Path

def load_labels(path: Path) -> list[dict]:
    text = path.read_text()
    labels, cur = [], None
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("- name:"):
            if cur: labels.append(cur)
            cur = {"name": line.split(":",1)[1].strip().strip('"')}
        elif cur and re.match(r"\s+(color|description):", line):
            k,v=line.strip().split(":",1)
            cur[k]=v.strip().strip('"')
    if cur: labels.append(cur)
    return labels

def request(method: str, url: str, token: str, body: dict|None=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Accept":"application/vnd.github+json",
        "Content-Type":"application/json",
        "User-Agent":"octo-server-product-agent-exam",
        "X-GitHub-Api-Version":"2022-11-28",
        "Authorization":f"Bearer {token}",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        body=e.read().decode("utf-8","replace")
        return e.code, body

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--file", default=".github/labels.yml")
    args=ap.parse_args()
    token=os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print("missing GITHUB_TOKEN", file=sys.stderr); return 2
    labels=load_labels(Path(args.file))
    ok=0
    for l in labels:
        name=l["name"]
        payload={"name":name,"color":l.get("color","ededed"),"description":l.get("description","")}
        encoded=urllib.parse.quote(name, safe="")
        patch_status, patch_body = request("PATCH", f"https://api.github.com/repos/{args.repo}/labels/{encoded}", token, payload)
        if patch_status == 200:
            print(f"updated {name}"); ok+=1; continue
        if patch_status == 404:
            post_status, post_body = request("POST", f"https://api.github.com/repos/{args.repo}/labels", token, payload)
            if post_status in (200,201):
                print(f"created {name}"); ok+=1; continue
            print(f"failed create {name}: {post_status} {post_body[:300]}", file=sys.stderr); return 1
        if patch_status in (403,429):
            print(f"rate/permission blocked {name}: {patch_status} {patch_body[:300]}", file=sys.stderr); return 2
        print(f"failed update {name}: {patch_status} {patch_body[:300]}", file=sys.stderr); return 1
    print(f"done {ok}/{len(labels)}")
    return 0

if __name__ == "__main__":
    import urllib.parse
    raise SystemExit(main())
