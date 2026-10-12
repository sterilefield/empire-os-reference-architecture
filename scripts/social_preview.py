#!/usr/bin/env python3
"""Make a repo's 1280×640 social-preview card (navy/teal brand) as SVG, then PNG.

Usage: python3 scripts/social_preview.py "Title" "Outcome line with one number" "tag · tag · tag" [out_dir]
PNG needs Playwright (npx playwright install chromium); GitHub's social preview accepts PNG/JPG < 1 MB.
"""
import subprocess
import sys
from pathlib import Path

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif"
title, outcome, tags = sys.argv[1], sys.argv[2], sys.argv[3]
out = Path(sys.argv[4] if len(sys.argv) > 4 else "assets")
out.mkdir(parents=True, exist_ok=True)
esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

THEMES = {"dark": ("#0B1F3A", "#F1F5F9", "#2DD4BF", "#94A3B8"),
          "light": ("#F8FAFC", "#0B1F3A", "#0F766E", "#475569")}
for name, (bg, ink, teal, quiet) in THEMES.items():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="640" viewBox="0 0 1280 640">
<style>text{{font-family:{FONT}}}</style>
<rect width="1280" height="640" fill="{bg}"/>
<rect x="80" y="96" width="72" height="8" rx="4" fill="{teal}"/>
<text x="80" y="200" font-size="64" font-weight="700" fill="{ink}">{esc(title)}</text>
<text x="80" y="270" font-size="32" font-weight="600" fill="{teal}">{esc(outcome)}</text>
<text x="80" y="330" font-size="24" fill="{quiet}">{esc(tags)}</text>
<text x="80" y="560" font-size="22" font-weight="600" fill="{ink}">Dr. Ravi Teja Thiriveedhi</text>
<text x="80" y="592" font-size="18" fill="{quiet}">Clinician → AI systems architect · github.com/Raviteja2k2k</text>
</svg>'''
    (out / f"social-{name}.svg").write_text(svg, encoding="utf-8")

js = f'''import {{ chromium }} from "playwright";
const b = await chromium.launch(); const p = await b.newPage({{ viewport: {{ width: 1280, height: 640 }} }});
for (const t of ["dark","light"]) {{ await p.goto("file://{out.resolve()}/social-" + t + ".svg"); await p.screenshot({{ path: "{out.resolve()}/social-" + t + ".png" }}); }}
await b.close();'''
tmp = out / "_render.mjs"
tmp.write_text(js)
try:
    subprocess.run(["node", str(tmp)], check=True)
    print("PNG cards written to", out)
except Exception as exc:
    print("SVGs written; PNG render skipped:", exc)
finally:
    tmp.unlink(missing_ok=True)
