"""Screenshot every slide of a cream deck with headless Chrome, then tile them for review.

    python3 shoot_deck.py /abs/path/to/index.html OUT_DIR [N]

One Chrome launch per slide, NO --user-data-dir (a shared profile hangs on the second
launch), absolute file:// path (a relative one silently screenshots ERR_FILE_NOT_FOUND).
Writes s01.png … and 2×2 review grids g1.png … (each tile 1600×900 — review at THAT size).
"""
import re, subprocess, sys, pathlib
from PIL import Image

html = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
n = int(sys.argv[3]) if len(sys.argv) > 3 else len(re.findall(r'^\s*\{ tag:"S', html.read_text(), re.M))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
bad = []
for i in range(1, n + 1):
    f = out / f"s{i:02d}.png"; f.unlink(missing_ok=True)
    try:
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--window-size=1600,900", "--hide-scrollbars",
                        f"--screenshot={f}", f"file://{html}#{i}"], capture_output=True, timeout=40)
    except subprocess.TimeoutExpired:
        pass
    if not f.exists(): bad.append(i)
print(f"{n - len(bad)} / {n} shots; missing: {bad}")
for g in range(0, n, 4):
    im = Image.new("RGB", (3208, 1808), "#222")
    for j, k in enumerate(range(g + 1, min(g + 5, n + 1))):
        im.paste(Image.open(out / f"s{k:02d}.png").convert("RGB").resize((1600, 900), Image.LANCZOS), ((j % 2) * 1608, (j // 2) * 908))
    im.save(out / f"g{g // 4 + 1}.png")
print("grids:", (n + 3) // 4, "in", out)
