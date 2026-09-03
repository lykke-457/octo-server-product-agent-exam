#!/usr/bin/env bash
set -euo pipefail

# Initialize this directory as a GitHub demand-pool repo.
# This script does NOT create a remote repo by itself. Create a public repo first,
# then run: REMOTE=git@github.com:owner/repo.git ./scripts/bootstrap_repo.sh

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
: "${REMOTE:?set REMOTE=git@github.com:owner/repo.git or https://github.com/owner/repo.git}"

cd "$ROOT"
if [ ! -d .git ]; then
  git init
fi
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REMOTE"
else
  git remote add origin "$REMOTE"
fi

git add .
git commit -m "Initial octo-server product agent exam pack" || true

echo "Repo initialized. Review files, then push with:"
echo "  git branch -M main"
echo "  git push -u origin main"
