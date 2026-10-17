#!/usr/bin/env python3
"""Checks the splash page before it is published. Standard library only.

    python3 check_site.py

- Only the expected files are published: no person pages, no GEDCOM, no data files.
- No page runs a script except the 404 page's fixed markup (it has none) and JSON-LD.
- Nothing is loaded from another server (links out are fine).
- Every name on the page is one of the public-record highlights in highlights.json, each with
  at least one outside link.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
errors = []

for f in SITE.rglob("*"):
    rel = f.relative_to(SITE).as_posix()
    if f.is_file() and (rel.startswith("people/") or f.suffix in {".ged", ".json"}):
        errors.append(f"{rel}: data or person pages must not be published")

for page in SITE.rglob("*.html"):
    html = page.read_text(encoding="utf-8")
    rel = page.relative_to(SITE).as_posix()
    for m in re.finditer(r"<script(?![^>]*application/ld\+json)[^>]*>", html):
        errors.append(f"{rel}: runs a script ({m.group(0)})")
    if re.search(r'\bsrc="https?://|url\(\s*["\']?https?://|@import'
                 r'|<link\b(?=[^>]*\brel="(?:stylesheet|icon|apple-touch-icon|manifest|preload)")[^>]*\bhref="https?://', html):
        errors.append(f"{rel}: loads something from another server")
    if 'http-equiv="Content-Security-Policy"' not in html:
        errors.append(f"{rel}: no Content-Security-Policy")

highlights = json.loads((ROOT / "highlights.json").read_text(encoding="utf-8"))
index = (SITE / "index.html").read_text(encoding="utf-8")
for h in highlights:
    if not h.get("links"):
        errors.append(f"highlights.json: {h['name']} has no outside source")
named = re.findall(r'<span class="hl-name">([^<]+)</span>', index)
expected = {h["name"] for h in highlights}
for n in named:
    if n.replace("&amp;", "&") not in expected:
        errors.append(f"index.html: {n} is listed but not in highlights.json")

for e in errors:
    print("FAIL:", e)
print(f"{'FAIL' if errors else 'OK'}: {len(list(SITE.rglob('*.html')))} pages, {len(named)} public-record highlights")
sys.exit(1 if errors else 0)
