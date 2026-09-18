#!/usr/bin/env python3
"""Generate and verify SWIR Progress SVG PRO assets for this repository."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "readme.md"
OUT = ROOT / "assets" / "readme"
PROJECT = "GitHub README Generator"
LEGACY_PATTERNS = (re.compile(r"[█▓▒░]{4,}"), re.compile(r"\[(?:[#=\-]{4,})\]"))


def card() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="180" viewBox="0 0 1200 180" role="img" aria-labelledby="title desc">
<title id="title">GitHub README Generator progress</title><desc id="desc">Product roadmap progress is N/A because no authoritative measurable product roadmap exists.</desc>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#02050A"/><stop offset="1" stop-color="#07111C"/></linearGradient><linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#0088FF"/><stop offset="1" stop-color="#62E5FF"/></linearGradient><pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="#62E5FF" stroke-opacity=".05"/></pattern></defs>
<rect x="1" y="1" width="1198" height="178" rx="22" fill="url(#bg)" stroke="#62E5FF" stroke-opacity=".25"/><rect x="1" y="1" width="1198" height="178" rx="22" fill="url(#grid)"/>
<text x="50" y="38" fill="#62E5FF" font-family="Segoe UI,Arial,sans-serif" font-size="15" font-weight="700" letter-spacing="3">SWIR PROGRESS</text><text x="50" y="73" fill="#F4FAFF" font-family="Segoe UI,Arial,sans-serif" font-size="27" font-weight="800">GitHub README Generator</text><text x="50" y="100" fill="#8DA8B8" font-family="Segoe UI,Arial,sans-serif" font-size="14">Product roadmap</text><text x="1138" y="73" text-anchor="end" fill="#F4FAFF" font-family="Segoe UI,Arial,sans-serif" font-size="32" font-weight="800">N/A</text><text x="1138" y="99" text-anchor="end" fill="#62E5FF" font-family="Segoe UI,Arial,sans-serif" font-size="13" font-weight="700">NO VERIFIED ROADMAP</text>
<rect x="50" y="119" width="1100" height="18" rx="9" fill="#08131F" stroke="#62E5FF" stroke-opacity=".16"/><path d="M68 128H1132" stroke="url(#accent)" stroke-width="2" stroke-dasharray="8 12" opacity=".34"/><text x="50" y="160" fill="#8DA8B8" font-family="Segoe UI,Arial,sans-serif" font-size="12">N/A — no authoritative measurable product roadmap</text>
</svg>'''


def mini() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="72" viewBox="0 0 900 72" role="img" aria-labelledby="title desc">
<title id="title">GitHub README Generator compact progress</title><desc id="desc">Product roadmap progress is N/A because no authoritative measurable product roadmap exists.</desc>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#02050A"/><stop offset="1" stop-color="#07111C"/></linearGradient><linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#0088FF"/><stop offset="1" stop-color="#62E5FF"/></linearGradient></defs>
<rect x="1" y="1" width="898" height="70" rx="15" fill="url(#bg)" stroke="#62E5FF" stroke-opacity=".25"/><text x="24" y="28" fill="#F4FAFF" font-family="Segoe UI,Arial,sans-serif" font-size="16" font-weight="700">GitHub README Generator</text><text x="24" y="49" fill="#8DA8B8" font-family="Segoe UI,Arial,sans-serif" font-size="11">Product roadmap</text><rect x="500" y="26" width="280" height="14" rx="7" fill="#08131F" stroke="#62E5FF" stroke-opacity=".16"/><path d="M512 33H768" stroke="url(#accent)" stroke-width="2" stroke-dasharray="6 10" opacity=".34"/><text x="860" y="39" text-anchor="end" fill="#62E5FF" font-family="Segoe UI,Arial,sans-serif" font-size="18" font-weight="800">N/A</text>
</svg>'''


def validate_svg(text: str, label: str) -> None:
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        raise SystemExit(f"{label}: invalid XML: {exc}")
    if root.tag.rsplit("}", 1)[-1] != "svg" or "viewBox" not in root.attrib:
        raise SystemExit(f"{label}: missing SVG root/viewBox")


def write_outputs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "progress-card.svg").write_text(card(), encoding="utf-8")
    (OUT / "progress-mini.svg").write_text(mini(), encoding="utf-8")


def check() -> None:
    expected = {"progress-card.svg": card(), "progress-mini.svg": mini()}
    for name, text in expected.items():
        validate_svg(text, name)
        path = OUT / name
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            raise SystemExit(f"{name}: missing or stale; run generator without --check")
    template = (OUT / "progress-template.svg").read_text(encoding="utf-8")
    validate_svg(template, "progress-template.svg")
    if "TEMPLATE / NOT PROJECT DATA" not in template:
        raise SystemExit("progress-template.svg: missing template label")
    readme = README.read_text(encoding="utf-8")
    if "assets/readme/progress-card.svg" not in readme or "assets/readme/progress-mini.svg" not in readme:
        raise SystemExit("README: required SVG embedding missing")
    for pattern in LEGACY_PATTERNS:
        if pattern.search(readme):
            raise SystemExit("README: legacy character progress meter found")
    print(f"OK: {PROJECT} product progress is N/A; SVG/XML, embeddings and legacy-meter cleanup verified.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        write_outputs()
    check()
    return 0


if __name__ == "__main__":
    sys.exit(main())
