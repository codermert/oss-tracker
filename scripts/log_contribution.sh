#!/usr/bin/env bash
# Log a real contribution (PR) into CONTRIBUTIONS.md.
#
# Usage:
#   ./scripts/log_contribution.sh <owner/repo> <pr_url> <language> "<short description>"
set -euo pipefail

if [[ $# -lt 4 ]]; then
  echo "usage: $0 <owner/repo> <pr_url> <language> \"<short description>\"" >&2
  exit 1
fi

REPO="$1"
PR_URL="$2"
LANG="$3"
DESC="$4"
DATE="$(date -u +%Y-%m-%d)"

FILE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/CONTRIBUTIONS.md"

if [[ ! -f "$FILE" ]]; then
  {
    echo "# Katkı Günlüğü"
    echo
    echo "| Tarih | Repo | PR | Dil | Açıklama |"
    echo "|---|---|---|---|---|"
  } > "$FILE"
fi

echo "| $DATE | $REPO | [PR]($PR_URL) | $LANG | $DESC |" >> "$FILE"
echo "logged: $REPO -> $PR_URL"
