#!/usr/bin/env python3
"""Scan GitHub for open good-first-issue / help-wanted issues in configured
languages and write a ranked markdown summary to ISSUES.md.

Uses the GitHub REST search API via a plain HTTPS request (no extra deps),
authenticated with GITHUB_TOKEN / GH_TOKEN from the environment.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

LANGUAGES = ["python", "javascript", "typescript", "dart"]
LABELS = ["good first issue", "help wanted"]
MAX_PER_LANGUAGE = 8
API_URL = "https://api.github.com/search/issues"


def token() -> str:
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not tok:
        print("warning: no GITHUB_TOKEN/GH_TOKEN set, requests will be rate-limited", file=sys.stderr)
    return tok or ""


def search(language: str, label: str, tok: str) -> list[dict]:
    query = f'language:{language} label:"{label}" state:open is:issue no:assignee'
    params = f"?q={urllib.parse.quote(query)}&sort=updated&order=desc&per_page={MAX_PER_LANGUAGE}"
    req = urllib.request.Request(API_URL + params)
    req.add_header("Accept", "application/vnd.github+json")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.load(resp)
            return data.get("items", [])
    except Exception as exc:  # noqa: BLE001
        print(f"warning: search failed for {language}/{label}: {exc}", file=sys.stderr)
        return []


def render(results: dict[str, list[dict]]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Önerilen Issue'lar",
        "",
        f"_Son güncelleme: {now}_",
        "",
        "Bu liste her gün otomatik güncellenir. Bir issue seçip PR açtığında",
        "`scripts/log_contribution.sh` ile `CONTRIBUTIONS.md`'ye kaydet.",
        "",
    ]
    for lang, items in results.items():
        lines.append(f"## {lang.capitalize()}")
        lines.append("")
        if not items:
            lines.append("_Şu an uygun issue bulunamadı._")
            lines.append("")
            continue
        seen_urls = set()
        for item in items:
            url = item.get("html_url")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            title = item.get("title", "").strip()
            repo_url = item.get("repository_url", "")
            repo = repo_url.replace("https://api.github.com/repos/", "")
            updated = item.get("updated_at", "")[:10]
            lines.append(f"- [ ] [{title}]({url}) — `{repo}` (güncellendi: {updated})")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    tok = token()
    results: dict[str, list[dict]] = {}
    for lang in LANGUAGES:
        combined: list[dict] = []
        for label in LABELS:
            combined.extend(search(lang, label, tok))
        results[lang] = combined[:MAX_PER_LANGUAGE]

    output = render(results)
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ISSUES.md")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(output)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    import urllib.parse

    main()
