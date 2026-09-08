#!/usr/bin/env python3
"""Legacy stub — delegates to make_ascii_svg.py + make_wordmark_svg.py. Do not call directly."""
import subprocess, pathlib, sys
print("make_glaine_ascii: delegating — use make_ascii_svg.py + make_wordmark_svg.py")
import os
base = pathlib.Path(__file__).resolve().parents[1]
if (base / "source-prepped.png").exists() or (base / "source.jpg").exists():
    src = "source-prepped.png" if (base / "source-prepped.png").exists() else "source.jpg"
    subprocess.run([sys.executable, str(base / "scripts/make_ascii_svg.py"), src, str(base / "glaine-ascii.svg")], check=False)
else:
    print("no source image — skipping portrait")
# wordmark
env = {**os.environ, "WORDMARK_TEXT": "GLAINE"}
subprocess.run([sys.executable, str(base / "scripts/make_wordmark_svg.py"), "--mode","rock","--out", str(base / "wordmark.svg")], env=env, check=False)
# patch title
try:
    w = (base / "wordmark.svg")
    w.write_text(w.read_text(encoding='utf-8').replace('avi@github','glaine@github'), encoding='utf-8')
except: pass
print("delegated done")
