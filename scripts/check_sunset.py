#!/usr/bin/env python3
"""Scan data/*.yml for API versions whose `sunset` date is near or past.
Writes .sunset_alerts.md (used by the weekly workflow to open a tracking issue).
Keeps the repo visibly active and warns users before a version dies.
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT = ROOT / ".sunset_alerts.md"
WINDOW_DAYS = 60


def main() -> int:
    today = dt.date.today()
    rows: list[str] = []
    for f in sorted(DATA_DIR.glob("*.yml")):
        data = yaml.safe_load(f.read_text(encoding="utf-8"))
        for v in data.get("versions") or []:
            sunset = (v.get("sunset") or "").strip()
            if not sunset:
                continue
            try:
                d = dt.date.fromisoformat(sunset)
            except ValueError:
                continue
            days = (d - today).days
            if days <= WINDOW_DAYS:
                status = "❌ EXPIRED" if days < 0 else f"⏳ {days}d left"
                rows.append(
                    f"| {data['platform']} | {v.get('version')} | {sunset} | {status} |"
                )

    if rows:
        body = (
            "# 🔔 API version sunset alerts\n\n"
            f"_Generated {today.isoformat()} — versions expiring within {WINDOW_DAYS} days._\n\n"
            "| Platform | Version | Sunset | Status |\n|---|---|---|---|\n"
            + "\n".join(rows)
            + "\n\n> Update `data/*.yml` to the next supported version and migrate integrations.\n"
        )
        OUT.write_text(body, encoding="utf-8")
        print(f"{len(rows)} sunset alert(s) written.")
    else:
        if OUT.exists():
            OUT.unlink()
        print("No sunset alerts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
