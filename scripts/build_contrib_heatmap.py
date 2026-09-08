#!/usr/bin/env python3
"""Build contrib-heatmap.svg from GitHub contributions (token optional).
Falls back to a tasteful placeholder if API unavailable.
Used by .github/workflows/update-profile-art.yml daily."""
import os, pathlib, datetime, json, urllib.request, html

BASE = pathlib.Path(__file__).resolve().parents[1]
OUT = BASE / "contrib-heatmap.svg"

def _placeholder(reason=""):
    now = datetime.date.today().isoformat()
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="118" viewBox="0 0 860 118" role="img" aria-label="contribution graph">
<rect width="100%" height="100%" rx="12" fill="#0d1117" stroke="#21262d"/>
<g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" fill="#8b949e">
<text x="14" y="20">glaine@github ~ $ ./contributions.sh  —  {html.escape(reason) or "auto-refreshed daily"}</text>
<text x="14" y="42" fill="#c9d1d9">SignOut  ◈   Product Builder  •  AI-Native  •  Workforce Tech — with love 💖</text>
<text x="14" y="64" fill="#58a6ff">github.com/glainejustin/signout — tap to clock in, GPS, rota &amp; Sheets sync</text>
<text x="14" y="86" fill="#8b949e">last update: {now}  •  data updates via GitHub Actions (contrib-heatmap)</text>
</g>
</svg>'''

def _fetch(username, token=None):
    # Use GraphQL contributionsCollection
    q = """
    query($login:String!) {
      user(login:$login) {
        contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { date contributionCount color } } } }
      }
    }"""
    body = json.dumps({"query": q, "variables": {"login": username}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
        "Content-Type": "application/json",
        "User-Agent": "glainejustin-profile-art"
    })
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=12) as r:
            j = json.loads(r.read().decode())
            return j["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    except Exception as e:
        print(f"fetch failed: {e}")
        return None

def _render(cal):
    if not cal: return _placeholder()
    weeks = cal["weeks"]
    # Layout
    cell = 11
    gap = 3
    pad = 14
    W = 860
    H = 118
    # Color ramp GitHub-like
    def level_color(c):
        if c == 0: return "#161b22"
        if c <= 2: return "#0e4429"
        if c <= 5: return "#006d32"
        if c <= 9: return "#26a641"
        return "#39d353"
    # Build cells
    rects = []
    x = pad
    for wi, w in enumerate(weeks[-52:]):  # last 52 weeks
        y = 28
        for d in w["contributionDays"]:
            c = int(d.get("contributionCount", 0))
            # prefer GitHub-provided color if present else ramp
            fill = d.get("color") or level_color(c)
            rects.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{fill}" stroke="#21262d" stroke-opacity="0.35"/>')
            y += cell + gap
        x += cell + gap
        if x > W - pad - cell: break
    total = cal.get("totalContributions", sum(int(d.get("contributionCount",0)) for w in weeks for d in w["contributionDays"]))
    label = f"{total} contributions in the last year"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="118" viewBox="0 0 860 118" role="img" aria-label="GitHub contribution graph">
<rect width="100%" height="100%" rx="12" fill="#0d1117" stroke="#21262d"/>
<text x="{pad}" y="20" font-family="ui-monospace, monospace" font-size="11" fill="#8b949e">glaine@github ~ $ ./contributions.sh  —  {html.escape(label)}</text>
<g>{chr(10).join(rects)}</g>
</svg>'''

def main():
    user = os.environ.get("PROFILE_USER", "glainejustin")
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    cal = _fetch(user, token)
    svg = _render(cal) if cal else _placeholder("token missing — showing placeholder until Actions runs")
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT} ({len(svg)} bytes)")

if __name__ == "__main__":
    main()
