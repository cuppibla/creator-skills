"""Parse the week-4 deck (index.html) and the talk track (script-natural.md).

Both PPTX builders import this, so the slides, the notes and the deck are one source.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


# ── the deck ────────────────────────────────────────────────────────────────
def _field(blk: str, name: str) -> str | None:
    m = re.search(name + r':\s*(?:I\+)?"((?:[^"\\]|\\.)*)"', blk)
    return html.unescape(m.group(1)) if m else None


def slides() -> list[dict]:
    src = (ROOT / "index.html").read_text()
    arr = src[src.index("const slides = ["):src.index("];", src.index("const slides = ["))]
    out = []
    for blk in re.split(r"\n  (?=\{ tag:\")", arr)[1:]:
        s = {"tag": _field(blk, "tag"), "act": _field(blk, "act") or "", "type": _field(blk, "type")}
        for k in ("src", "mem", "cap", "sub", "eyebrow", "h1", "note"):
            v = _field(blk, k)
            if v is not None:
                s[k] = v
        code = re.search(r"code:`([^`]*)`", blk)
        if code:
            s["code"] = html.unescape(code.group(1))
        lines = re.search(r"lines:\[(.*?)\]", blk, re.S)
        if lines:
            s["lines"] = [html.unescape(x) for x in re.findall(r'"((?:[^"\\]|\\.)*)"', lines.group(1))]
        for flag in ("tall", "art"):
            s[flag] = f"{flag}:true" in blk
        out.append(s)
    return out


# ── the talk track ──────────────────────────────────────────────────────────
ROW = re.compile(r"^\| (\d+) · (.*?) \| (.*?) \| (.*?) \| (\d+) \|$", re.M)


def notes(script: str = "script-natural.md") -> dict[int, dict]:
    text = (ROOT / script).read_text()
    act = ""
    out: dict[int, dict] = {}
    for line in text.splitlines():
        h = re.match(r"^## (.+?)(?: · about .*)?$", line)
        if h and not h.group(1).startswith(("Terms", "Cuts")):
            act = re.sub(r"\s*\(\d+[–-]\d+\)\s*$", "", h.group(1)).strip()
        m = ROW.match(line)
        if m:
            n, title, say, screen, sec = m.groups()
            out[int(n)] = {
                "act": act,
                "title": title.strip(),
                "say": [s.strip() for s in say.split("<br>") if s.strip()],
                "screen": "" if screen.strip() in {"—", "-"} else screen.strip(),
                "sec": int(sec),
            }
    return out


def note_text(n: int, note: dict) -> str:
    head = f"Slide {n} · {note['title']} · {note['act']} · {note['sec']}s"
    body = "\n".join(note["say"])
    tail = f"\nOn screen: {note['screen']}" if note["screen"] else ""
    return f"{head}\n{'-' * len(head)}\n\n{body}\n{tail}"


if __name__ == "__main__":
    sl, nt = slides(), notes()
    print(f"slides: {len(sl)} · notes: {len(nt)}")
    missing = [i for i in range(1, len(sl) + 1) if i not in nt]
    print("slides without notes:", missing or "none")
    kinds: dict[str, int] = {}
    for s in sl:
        kinds[s["type"]] = kinds.get(s["type"], 0) + 1
    print("types:", kinds)
    print("\n--- sample note, slide 12 ---")
    print(note_text(12, nt[12]))
