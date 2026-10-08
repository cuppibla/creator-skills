"""Read the real geometry of every deck slide out of the browser, into build/layout.json.

The editable PPTX is built from this, so it lands where the HTML deck lands — no second
implementation of the CSS. Makes a copy of index.html with an extractor appended, renders it in
headless Chrome, and reads the JSON back out of the dumped DOM.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

EXTRACTOR = r"""
<script>
(async function () {
  await Promise.all([...document.images].map(im => im.complete && im.naturalWidth
    ? Promise.resolve()
    : new Promise(res => { im.addEventListener("load", res, { once: true });
                           im.addEventListener("error", res, { once: true }); })));
  const stage = document.getElementById("stage");
  const saved = stage.style.transform;
  stage.style.transform = "none";
  const MONO = /mono|menlo|consolas|courier/i;

  function col(c) {
    const m = String(c).match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(",").map(Number);
    if (p.length > 3 && p[3] === 0) return null;
    const hex = p.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, "0")).join("");
    return { hex: hex.toUpperCase(), a: p.length > 3 ? p[3] : 1 };
  }
  function runsOf(el, pre) {
    const out = [];
    (function walk(node) {
      for (const n of node.childNodes) {
        if (n.nodeType === 3) {
          let t = n.textContent;
          if (pre) {
            // a code block keeps its own spacing: only the very first newline goes
            if (out.length === 0) t = t.replace(/^\n/, "");
            if (t === "") continue;
          } else {
            if (!t.replace(/\s+/g, "")) {
              if (out.length && out[out.length - 1].t && !/\s$/.test(out[out.length - 1].t)) out[out.length - 1].t += " ";
              continue;
            }
            t = t.replace(/\s+/g, " ");
          }
          const cs = getComputedStyle(n.parentElement);
          out.push({
            t: t,
            sz: parseFloat(cs.fontSize), w: parseInt(cs.fontWeight) || 400,
            c: (col(cs.color) || { hex: "000000" }).hex,
            i: cs.fontStyle === "italic", st: /line-through/.test(cs.textDecorationLine),
            m: MONO.test(cs.fontFamily), ls: parseFloat(cs.letterSpacing) || 0,
          });
        } else if (n.nodeType === 1) {
          if (n.tagName === "BR") { out.push({ br: true }); continue; }
          walk(n);
        }
      }
    })(el);
    return out.filter(r => r.br || r.t.trim() !== "" || out.length > 1);
  }

  const data = [];
  document.querySelectorAll(".slide").forEach((sl, i) => {
    sl.classList.add("on");
    const o = stage.getBoundingClientRect();
    const boxes = [], texts = [], images = []; let z = 0;
    const rel = e => { const r = e.getBoundingClientRect(); return { x: r.left - o.left, y: r.top - o.top, w: r.width, h: r.height }; };

    (function walk(node) {
      for (const el of node.children) {
        const cs = getComputedStyle(el);
        if (cs.display === "none" || cs.visibility === "hidden") continue;
        const r = rel(el);
        if (r.w < 0.5 || r.h < 0.5) continue;
        const bg = col(cs.backgroundColor);
        const sides = ["Top", "Right", "Bottom", "Left"].map(s => parseFloat(cs["border" + s + "Width"]) || 0);
        const all = sides.every(v => v > 0) && sides.every(v => Math.abs(v - sides[0]) < 0.01);
        const bc = sides.some(v => v > 0) ? col(cs.borderTopColor) : null;
        if (bg || (bc && all)) boxes.push({
          z: z++, ...r, fill: bg && bg.hex, alpha: bg ? bg.a : 1, stroke: all && bc ? bc.hex : null, sw: all ? sides[0] : 0,
          r: parseFloat(cs.borderTopLeftRadius) || 0, dash: cs.borderTopStyle === "dashed",
        });
        if (bc && !all) sides.forEach((v, k) => {
          if (!v) return;
          const c = col(cs[["borderTopColor", "borderRightColor", "borderBottomColor", "borderLeftColor"][k]]);
          const seg = k === 0 ? { x: r.x, y: r.y, w: r.w, h: 0 } : k === 2 ? { x: r.x, y: r.y + r.h, w: r.w, h: 0 }
                    : k === 1 ? { x: r.x + r.w, y: r.y, w: 0, h: r.h } : { x: r.x, y: r.y, w: 0, h: r.h };
          boxes.push({ z: z++, ...seg, rule: true, stroke: c && c.hex, sw: v });
        });
        if (el.tagName === "IMG") {
          images.push({ z: z++, ...r, src: el.getAttribute("src"), nw: el.naturalWidth, nh: el.naturalHeight,
                        fit: cs.objectFit, r: parseFloat(cs.borderTopLeftRadius) || 0 });
          continue;
        }
        const hasText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
        if (hasText) {
          const pt = parseFloat(cs.paddingTop) || 0, pr = parseFloat(cs.paddingRight) || 0;
          const pb = parseFloat(cs.paddingBottom) || 0, pl = parseFloat(cs.paddingLeft) || 0;
          const pre = /pre/.test(cs.whiteSpace);
          texts.push({
            z: z++, x: r.x + pl, y: r.y + pt, w: Math.max(1, r.w - pl - pr), h: Math.max(1, r.h - pt - pb),
            align: cs.textAlign, lh: parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.2,
            pre, runs: runsOf(el, pre),
          });
        } else walk(el);
      }
    })(sl);

    data.push({ n: i + 1, boxes, texts, images });
    sl.classList.remove("on");
  });

  stage.style.transform = saved;
  document.body.innerHTML = '<pre id="LAYOUT">' + JSON.stringify(data) + "</pre>";
})();
</script>
"""


def main() -> None:
    BUILD.mkdir(exist_ok=True)
    src = (ROOT / "index.html").read_text()
    # the copy lives in build/, so give it a base URL back at the deck root or no image loads
    src = src.replace("<head>", f'<head>\n<base href="file://{ROOT}/">', 1)
    (BUILD / "extract.html").write_text(src.replace("</body>", EXTRACTOR + "\n</body>"))
    out = subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--window-size=1600,900", "--virtual-time-budget=20000",
         "--dump-dom", f"file://{BUILD / 'extract.html'}"],
        capture_output=True, text=True, timeout=180).stdout
    m = re.search(r'<pre id="LAYOUT">(.*?)</pre>', out, re.S)
    if not m:
        sys.exit("extractor did not run — no LAYOUT node in the dumped DOM")
    data = json.loads(m.group(1).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"'))
    (BUILD / "layout.json").write_text(json.dumps(data))
    print(f"slides: {len(data)}")
    for s in data[:3] + data[-1:]:
        print(f"  slide {s['n']:2}: {len(s['boxes'])} boxes · {len(s['texts'])} texts · {len(s['images'])} images")
    tot = sum(len(s["boxes"]) + len(s["texts"]) + len(s["images"]) for s in data)
    print("total elements:", tot, "· layout.json", (BUILD / "layout.json").stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
