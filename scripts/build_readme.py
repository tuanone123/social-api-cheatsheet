#!/usr/bin/env python3
"""Regenerate the tables in README.md from data/*.yml.

Only the block between the AUTOGEN markers is replaced, so hand-written intro
and contribution sections stay intact.
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
README = ROOT / "README.md"
START = "<!-- AUTOGEN:START -->"
END = "<!-- AUTOGEN:END -->"


def esc(v) -> str:
    return str(v if v is not None else "").replace("|", "\\|").replace("\n", " ")


def render(platform: dict) -> str:
    out: list[str] = []
    out.append(f"### {esc(platform['platform'])}")
    meta = (
        f"> Docs: <{platform.get('docs','')}> · "
        f"Changelog: <{platform.get('changelog','')}> · "
        f"Auth: {esc(platform.get('auth',''))}"
    )
    out.append(meta)
    if platform.get("base_url"):
        out.append(f">\n> Base URL: `{platform['base_url']}`")

    versions = platform.get("versions") or []
    has_sunset = any(v.get("sunset") for v in versions)
    if versions and platform.get("versioning"):
        out.append("\n**Versions**\n")
        if has_sunset:
            out.append("| Version | Released | Sunset |")
            out.append("|---|---|---|")
            for v in versions:
                out.append(
                    f"| {esc(v.get('version'))} | {esc(v.get('released'))} | {esc(v.get('sunset') or '—')} |"
                )
        else:
            out.append("| Version | Released |")
            out.append("|---|---|")
            for v in versions:
                out.append(f"| {esc(v.get('version'))} | {esc(v.get('released'))} |")

    endpoints = platform.get("endpoints") or []
    if endpoints:
        out.append("\n**Endpoints**\n")
        out.append("| Endpoint | Method | Path | Scopes | Key fields | Notes |")
        out.append("|---|---|---|---|---|---|")
        for e in endpoints:
            out.append(
                "| {name} | {method} | `{path}` | {scopes} | {fields} | {notes} |".format(
                    name=esc(e.get("name")),
                    method=esc(e.get("method")),
                    path=esc(e.get("path")),
                    scopes=esc(e.get("scopes")),
                    fields=esc(e.get("key_fields")),
                    notes=esc(e.get("notes")),
                )
            )
    if platform.get("last_checked"):
        out.append(f"\n_Last verified: {platform['last_checked']}_")
    return "\n".join(out)


def main() -> int:
    files = sorted(DATA_DIR.glob("*.yml"))
    blocks = []
    toc = []
    for f in files:
        data = yaml.safe_load(f.read_text(encoding="utf-8"))
        name = data["platform"]
        anchor = name.lower().replace(" ", "-")
        toc.append(f"- [{name}](#{anchor})")
        blocks.append(render(data))

    body = (
        "**Platforms:** " + " · ".join(f"[{yaml.safe_load(f.read_text(encoding='utf-8'))['platform']}]"
                                       f"(#{yaml.safe_load(f.read_text(encoding='utf-8'))['platform'].lower().replace(' ','-')})"
                                       for f in files)
        + "\n\n"
        + "\n\n".join(blocks)
    )

    text = README.read_text(encoding="utf-8")
    pre, _, rest = text.partition(START)
    _, _, post = rest.partition(END)
    new = f"{pre}{START}\n\n{body}\n\n{END}{post}"
    README.write_text(new, encoding="utf-8")
    print(f"README rebuilt from {len(files)} platform file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
