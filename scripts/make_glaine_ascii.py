#!/usr/bin/env python3
"""Generate glainejustin terminal ASCII assets - typed portrait + 3d wordmark stub.
Requires no external deps. Produces deterministic SVGs matching terminal layout widths (370/490)."""

import pathlib, re, html, textwrap

BASE = pathlib.Path(__file__).resolve().parents[1]

GLAINE_ASCII = r"""
 ██████  ██       █████  ██ ███    ██ ███████          ██ ██    ██ ███████ ████████ ██ ███    ██
██       ██      ██   ██ ██ ████   ██ ██               ██ ██    ██ ██         ██    ██ ████   ██
██   ███ ██      ███████ ██ ██ ██  ██ █████            ██ ██    ██ ███████    ██    ██ ██ ██  ██
██    ██ ██      ██   ██ ██ ██  ██ ██ ██          ██   ██ ██    ██      ██    ██    ██ ██  ██ ██
 ██████  ███████ ██   ██ ██ ██   ████ ███████      █████   ██████  ███████    ██    ██ ██   ████
""".strip("\n")

JUSTIN_SUB = "glainejustin • builder • product • love"

# Simple hand-built mono portrait — pays homage to 's ASCII photo without needing an actual photo.
# Simple hand-built mono portrait — no external photo needed.
PORTRAIT_LINES = [
    "  .------------------------------.  ",
    "  |         ░░░░░░░░░░░░         |  ",
    "  |       ░░▒▒▓▓▓▓▓▓▒▒░░       |  ",
    "  |      ░▒▓████████████▓▒░      |  ",
    "  |     ░▓████████████████▓░     |  ",
    "  |    ░▓████ ▓██████▓ ████▓░    |  ",
    "  |    ▒████  ████████  ████▒    |  ",
    "  |    ▓████   ██████   ████▓    |  ",
    "  |    ▒████    ▀▀▀▀    ████▒    |  ",
    "  |    ░▓████           ████▓░    |  ",
    "  |     ░▓█████▄   ▄█████▓░     |  ",
    "  |      ░▒▓████████████▓▒░      |  ",
    "  |       ░░▒▒▓▓▓▓▓▓▒▒░░       |  ",
    "  |         ░░░░░░░░░░░░         |  ",
    "  `------------------------------'  ",
    "          glainejustin  ◈           ",
]

def _svg_text(lines, width, title):
    # Build minimal mono SVG with typed feel
    W = width
    line_h = 16
    pad = 14
    H = pad*2 + len(lines)*line_h + 10
    esc = lambda s: html.escape(s)
    # Background
    bg = "#0d1117" if "portrait" in title.lower() else "#0d1117"
    fg = "#c9d1d9"
    # Build tspans
    tspans = "\n".join(
        f'<tspan x="{pad}" dy="{line_h if i else 0}">{esc(line) if line.strip() else " "}</tspan>'
        for i, line in enumerate(lines)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(title)}">
<rect width="100%" height="100%" rx="12" fill="{bg}" stroke="#21262d"/>
<text x="{pad}" y="{pad+10}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12" fill="{fg}" xml:space="preserve" dominant-baseline="hanging">{tspans}
</text>
</svg>
'''

def _wordmark_svg():
    # Extruded block letters for GLAINE + JUSTIN
    lines = [
        "  ┏━┓ ╻  ┏━┓╻┏┓╻┏━╸      ┏┓╻╻ ╻┏━┓╺┳╸╻┏┓╻",
        "  ┃┓┃ ┃  ┣━┫┃┃┗┫┣╸   ─── ┃┗┫┃ ┃┗━┓ ┃ ┃┃┗┫",
        "  ┗┻┛┗━╸╹ ╹╹╹ ╹┗━╸      ╹ ╹┗━┛┗━┛ ╹ ╹╹ ╹",
        "  ────────────────────────────────  ",
        "  glainejustin  •  product builder  •  signout",
    ]
    # widen to ~490
    return _svg_text(lines, 490, "GLAINE JUSTIN — wordmark")

def main():
    BASE.mkdir(parents=True, exist_ok=True)
    portrait = _svg_text(PORTRAIT_LINES, 370, "glainejustin — ASCII portrait")
    (BASE / "glaine-ascii.svg").write_text(portrait, encoding="utf-8")
    (BASE / "wordmark.svg").write_text(_wordmark_svg(), encoding="utf-8")
    # Minimal heatmap placeholder — real one via Actions daily
    heatmap = '''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="120" viewBox="0 0 860 120" role="img" aria-label="contribution graph">
<rect width="100%" height="100%" rx="12" fill="#0d1117" stroke="#21262d"/>
<g font-family="ui-monospace,monospace" font-size="10" fill="#8b949e">
<text x="14" y="18">◼ ◼ ◼ ◼ ◼ ◼ ◼  ◼ ◼ ◼ ◼ ◼ ◼ ◼  ◼ ◼ ◼ ◼ ◼ ◼ ◼  ◼ ◼ ◼ ◼ ◼ ◼ ◼  ◼ ◼ ◼ ◼ ◼ ◼ ◼</text>
<text x="14" y="36">glainejustin contributions — auto-refreshed daily by GitHub Actions</text>
<text x="14" y="56" fill="#c9d1d9">SignOut ◈  Product Builder  •  AI-Native  •  Workforce Tech  —  with love 💖</text>
<text x="14" y="78" fill="#58a6ff">tip: star glainejustin/signout → github.com/glainejustin/signout</text>
</g>
</svg>'''
    (BASE / "contrib-heatmap.svg").write_text(heatmap, encoding="utf-8")
    print("wrote svgs")

if __name__ == "__main__":
    main()
