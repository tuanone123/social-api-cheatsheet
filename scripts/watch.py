#!/usr/bin/env python3
"""Fetch each source in sources.yml, normalize its text, and diff against the
last saved snapshot. If anything changed, update the snapshot and record a
summary. The GitHub Action turns changed snapshots into a pull request so a
human can curate the actual cheat-sheet entry in data/*.yml.

We deliberately DO NOT auto-edit data/*.yml: upstream HTML is noisy and a bad
auto-parse would poison the cheat sheet. Detect -> notify -> human curates.
"""
from __future__ import annotations

import hashlib
import os
import re
import sys
from pathlib import Path

import requests
import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
SNAP_DIR = ROOT / "snapshots"
SUMMARY_FILE = ROOT / ".watch_summary.md"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 social-api-cheatsheet-bot"
)


def normalize(html: str, selector: str | None) -> str:
    """Extract visible text and strip noise so unrelated tweaks don't trigger diffs."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    node = None
    if selector:
        for sel in [s.strip() for s in selector.split(",")]:
            node = soup.select_one(sel)
            if node:
                break
    text = (node or soup).get_text("\n")
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]
    text = "\n".join(lines)
    # Drop volatile fragments (absolute timestamps, csrf-ish tokens).
    text = re.sub(r"\b\d{4}-\d{2}-\d{2}T[\d:.+Z-]+", "", text)
    return text.strip()


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    SNAP_DIR.mkdir(exist_ok=True)
    cfg = yaml.safe_load((ROOT / "sources.yml").read_text(encoding="utf-8"))
    changes: list[str] = []
    errors: list[str] = []

    for src in cfg.get("sources", []):
        slug = src["slug"]
        url = src["url"]
        snap_txt = SNAP_DIR / f"{slug}.txt"
        snap_sha = SNAP_DIR / f"{slug}.sha"
        try:
            resp = requests.get(url, headers={"User-Agent": UA}, timeout=45)
            resp.raise_for_status()
        except Exception as exc:  # network / blocking / redesign
            errors.append(f"- ⚠️ **{slug}**: fetch failed — {exc}")
            print(f"[warn] {slug}: {exc}", file=sys.stderr)
            continue

        text = normalize(resp.text, src.get("selector"))
        if not text:
            errors.append(f"- ⚠️ **{slug}**: empty extract (selector may be stale)")
            continue

        new_sha = sha(text)
        old_sha = snap_sha.read_text().strip() if snap_sha.exists() else ""

        if new_sha != old_sha:
            snap_txt.write_text(text, encoding="utf-8")
            snap_sha.write_text(new_sha, encoding="utf-8")
            state = "first snapshot" if not old_sha else "changed"
            changes.append(f"- 🔔 **{slug}** {state} — {url}")
            print(f"[change] {slug}: {state}")
        else:
            print(f"[ok] {slug}: unchanged")

    changed = bool(changes)
    lines = ["# API changelog watcher\n"]
    lines.append("## Changes detected\n" + ("\n".join(changes) if changes else "_none_"))
    if errors:
        lines.append("\n## Warnings\n" + "\n".join(errors))
    lines.append(
        "\n---\n> A snapshot changed means the upstream page moved. "
        "Please review the source and update the matching `data/*.yml` entry, "
        "then merge this PR."
    )
    SUMMARY_FILE.write_text("\n".join(lines), encoding="utf-8")

    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a", encoding="utf-8") as fh:
            fh.write(f"changed={'true' if changed else 'false'}\n")

    print(f"changed={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
