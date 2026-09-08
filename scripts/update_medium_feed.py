#!/usr/bin/env python3
"""Inject latest Medium posts into README between MEDIUM:START/END markers.
Keeps the terminal aesthetic. If no posts found, leaves README unchanged.
"""
import pathlib, re, sys

try:
    import feedparser
except ImportError:
    print("feedparser not installed — pip install feedparser in workflow")
    sys.exit(0)

FEED = "https://medium.com/feed/@glainejustin"
README = pathlib.Path(__file__).resolve().parent.parent / "README.md"

def fetch_items(limit=3):
    d = feedparser.parse(FEED)
    items = []
    for e in d.entries[:limit]:
        title = (e.title or "").strip()
        link = (e.link or "").strip()
        if title and link:
            items.append((title, link))
    return items

def build_block(items):
    if not items:
        return ""
    lines = ["<!-- MEDIUM:START -->", "<h3><code>glaine@github ~ $ ./writing.sh</code></h3>", "<ul>"]
    for title, link in items:
        # escape html in title
        esc = title.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")
        lines.append(f'<li><a href="{link}">{esc}</a></li>')
    lines += ["</ul>", "<!-- MEDIUM:END -->"]
    return "\n".join(lines)

def main():
    items = fetch_items()
    if not items:
        print("no medium items")
        return
    block = build_block(items)
    text = README.read_text(encoding="utf-8")
    if "<!-- MEDIUM:START -->" in text and "<!-- MEDIUM:END -->" in text:
        new_text = re.sub(r"<!-- MEDIUM:START -->.*?<!-- MEDIUM:END -->", block, text, flags=re.DOTALL)
    else:
        # Insert before final </div>
        if "</div>" in text:
            new_text = text.replace("</div>", block + "\n\n</div>", 1)
        else:
            new_text = text + "\n\n" + block
    if new_text != text:
        README.write_text(new_text, encoding="utf-8")
        print(f"injected {len(items)} medium posts")
    else:
        print("no change")

if __name__ == "__main__":
    main()
