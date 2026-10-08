"""The Agent-Memory workshop diagram style, as emitters.

Tokens and idioms are lifted from Topics/agent-memory-workshop/slide-diagrams/src/*.svg
(e1-adk-wired, d5-memory-bank, d4-policies): cream canvas, ink boxes with 3px
borders and rx 20, tan arrows, purple model nodes, green tools, a felt icon in a
corner, one bold line or one caveat strip at the bottom. Nothing here is a new
style — it is that deck's paint, so the two decks are one family.
"""
from __future__ import annotations

SANS = "-apple-system,'SF Pro Text',Arial"
MONO = "'SF Mono',Menlo"
BG, INK, SUB, TAN, FRAME, HEAD = "#FAF6F0", "#2A2520", "#8A8378", "#C9BCA9", "#F8F2E9", "#5A5248"
GREEN, GREEND, GREENBG = "#6E9A68", "#4E7A48", "#F3F7F2"
PURPLE, PURPLED, PURPLEBG, PURPLELT = "#8B7EC8", "#6B5FA8", "#F5F3FB", "#EDE9F7"
BLUE, BLUED, BLUEBG = "#6E9BC0", "#4E7A9E", "#F1F5F8"
AMBER, AMBERD, AMBERBG = "#C08A2E", "#9A6D20", "#FDF6E8"
TERRA, TERRABG = "#C96442", "#FBEDE7"
CAVBG, CAVLN, CAVINK = "#FBF3E2", "#E8D9B8", "#8A5A2B"
BOUND = "#B0A490"

KIND = {  # box kinds: (stroke, label colour, sub colour, fill)
    "ink":    (INK, INK, SUB, "#FFFFFF"),
    "green":  (GREEN, GREEND, SUB, "#FFFFFF"),
    "greenbg":(GREEN, GREEND, SUB, GREENBG),
    "purple": (PURPLE, PURPLED, SUB, "#FFFFFF"),
    "purplebg":(PURPLE, PURPLED, SUB, PURPLEBG),
    "blue":   (BLUE, BLUED, SUB, "#FFFFFF"),
    "bluebg": (BLUE, BLUED, SUB, BLUEBG),
    "amber":  (AMBER, AMBERD, SUB, AMBERBG),
    "terra":  (TERRA, TERRA, SUB, "#FFFFFF"),
    "tan":    (TAN, INK, SUB, "#FFFFFF"),
}
ARROW = {"tan": (TAN, "a", SUB), "purple": (PURPLE, "ap", PURPLED), "blue": (BLUE, "ab", BLUED),
         "green": (GREEN, "ag", GREEND), "amber": (AMBER, "am", AMBERD), "terra": (TERRA, "at", TERRA)}

HEADER = """<svg width="1600" height="{h}" viewBox="0 0 1600 {h}" xmlns="http://www.w3.org/2000/svg">
<defs>
{markers}
</defs>
<rect width="1600" height="{h}" fill="#FAF6F0"/>
"""


def _marker(mid, col):
    return (f' <marker id="{mid}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="8" markerHeight="8" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>')


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Svg:
    def __init__(self, h=900):
        self.h = h
        marks = "\n".join(_marker(m, c) for c, m, _ in ARROW.values())
        self.p = [HEADER.format(h=h, markers=marks)]
        self._clip = 0

    # ── text ────────────────────────────────────────────────────────────
    def title(self, t, sub=""):
        self.p.append(f'<text x="90" y="96" font-family="{SANS}" font-size="46" font-weight="800" fill="{INK}">{esc(t)}</text>')
        if sub:
            self.p.append(f'<text x="90" y="140" font-family="-apple-system,Arial" font-size="22" fill="{SUB}">{esc(sub)}</text>')

    def text(self, x, y, s, size=16, fill=SUB, mono=False, anchor="start", weight=None):
        ff = MONO if mono else "-apple-system,Arial"
        fw = f' font-weight="{weight}"' if weight else ""
        self.p.append(f'<text x="{x}" y="{y}" font-family="{ff}" font-size="{size}" fill="{fill}"{fw} text-anchor="{anchor}">{esc(s)}</text>')

    def lines(self, x, y, rows, size=16, fill=INK, mono=True, lh=26, anchor="start", weight=None):
        for i, r in enumerate(rows):
            s, c = (r, fill) if isinstance(r, str) else r
            self.text(x, y + i * lh, s, size=size, fill=c, mono=mono, anchor=anchor, weight=weight)

    def bottom(self, s, y=None):
        """The bold one-line takeaway the workshop diagrams end on."""
        self.text(90, y or self.h - 24, s, size=24, fill=INK, weight=800)

    def caveat(self, head, body="", y=None):
        y = y if y is not None else self.h - 118
        self.p.append(f'<rect x="90" y="{y}" width="1420" height="{"90" if body else "64"}" rx="16" fill="{CAVBG}" stroke="{CAVLN}" stroke-width="2.5"/>')
        self.text(120, y + 40, head, size=21, fill=CAVINK, weight=700)
        if body:
            self.text(120, y + 70, body, size=17, fill=CAVINK)

    # ── boxes ───────────────────────────────────────────────────────────
    def box(self, x, y, w, h, name, sub="", sub2="", kind="ink", stroke_w=3, name_size=22, mono_sub=False):
        stroke, col, subcol, fill = KIND[kind]
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"/>')
        n = 1 + bool(sub) + bool(sub2)
        cy = y + h / 2 + (8 if n == 1 else -8 if n == 2 else -22)
        self.text(x + w / 2, cy, name, size=name_size, fill=col, mono=True, anchor="middle", weight=700)
        if sub:
            self.text(x + w / 2, cy + 32, sub, size=16, fill=subcol, mono=mono_sub, anchor="middle")
        if sub2:
            self.text(x + w / 2, cy + 56, sub2, size=15, fill=subcol, mono=mono_sub, anchor="middle")

    def model(self, x, y, w, h, name, sub="", sub2=""):
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{PURPLE}"/>')
        n = 1 + bool(sub) + bool(sub2)
        cy = y + h / 2 + (8 if n == 1 else -8 if n == 2 else -22)
        self.text(x + w / 2, cy, "✦ " + name, size=22, fill="#FFFFFF", mono=True, anchor="middle", weight=700)
        if sub:
            self.text(x + w / 2, cy + 32, sub, size=15, fill=PURPLELT, anchor="middle")
        if sub2:
            self.text(x + w / 2, cy + 56, sub2, size=15, fill=PURPLELT, anchor="middle")

    def container(self, x, y, w, h, tag, tag2="", kind="process"):
        fill, stroke = (FRAME, BOUND) if kind == "process" else (PURPLEBG, PURPLE)
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="24" fill="{fill}" fill-opacity="0.55" stroke="{stroke}" stroke-width="2.5" stroke-dasharray="10 7"/>')
        self.text(x + 32, y + 45, tag, size=18, fill=HEAD if kind == "process" else PURPLED, mono=True, weight=700)
        if tag2:
            self.text(x + w - 32, y + 45, tag2, size=15, fill=SUB, mono=True, anchor="end")

    def store(self, x, y, w, h, name, sub, rows, row_h=44, kind="tan", size=16):
        """A dictionary or shelf: a box with white rows inside."""
        stroke, col, subcol, fill = KIND[kind]
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{FRAME}" stroke="{stroke}" stroke-width="3"/>')
        self.text(x + w / 2, y + 40, name, size=22, fill=col if kind != "tan" else INK, mono=True, anchor="middle", weight=700)
        self.text(x + w / 2, y + 66, sub, size=15, fill=subcol, anchor="middle")
        for i, r in enumerate(rows):
            s, c = (r, INK) if isinstance(r, str) else r
            ry = y + 86 + i * (row_h + 10)
            self.p.append(f'<rect x="{x + 26}" y="{ry}" width="{w - 52}" height="{row_h}" rx="10" fill="#FFFFFF" stroke="{TAN}" stroke-width="2"/>')
            self.text(x + 44, ry + row_h / 2 + 6, s, size=size, fill=c, mono=True)

    def panel(self, x, y, w, h, rows, size=16, lh=26, dark=True):
        """A code / prompt panel: ink on cream, or cream on ink."""
        if dark:
            self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{INK}"/>')
            self.lines(x + 24, y + 36, rows, size=size, fill="#F3EDE3", lh=lh)
        else:
            self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#FFFFFF" stroke="{TAN}" stroke-width="2.5"/>')
            self.lines(x + 24, y + 36, rows, size=size, fill=INK, lh=lh)

    def note(self, x, y, w, h, head, body, tone="amber"):
        fill, stroke, hc, bc = {"amber": (AMBERBG, AMBER, AMBERD, "#5A5248"),
                                "purple": (PURPLEBG, PURPLE, PURPLED, "#5A5248"),
                                "green": (GREENBG, GREEN, GREEND, "#5A5248"),
                                "blue": (BLUEBG, BLUE, BLUED, "#5A5248"),
                                "terra": (TERRABG, TERRA, TERRA, "#5A5248"),
                                "tan": ("#FFFFFF", TAN, INK, "#5A5248")}[tone]
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>')
        self.text(x + 28, y + 38, head, size=19, fill=hc, mono=True, weight=700)
        if isinstance(body, str):
            body = [body]
        for i, b in enumerate(body):
            self.text(x + 28, y + 68 + i * 25, b, size=17, fill=bc)

    def cylinder(self, cx, top, rx=50, ry=12, h=60, fill="#FFFFFF", stroke=INK):
        self.p.append(f'<path d="M{cx - rx} {top} L{cx - rx} {top + h} A{rx} {ry} 0 0 0 {cx + rx} {top + h} L{cx + rx} {top}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')
        self.p.append(f'<ellipse cx="{cx}" cy="{top}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')

    def icon(self, name, x=1360, y=28, size=150):
        """A felt icon from the workshop set, inlined by build_cream.py."""
        self._clip += 1
        self.p.append(f'<clipPath id="ic{self._clip}"><rect x="{x}" y="{y}" width="{size}" height="{size}" rx="26"/></clipPath>')
        self.p.append(f'<image href="@@ICON:{name}@@" x="{x}" y="{y}" width="{size}" height="{size}" clip-path="url(#ic{self._clip})"/>')

    # ── edges ───────────────────────────────────────────────────────────
    def arrow(self, pts, color="tan", dashed=False, label="", lx=None, ly=None, step=None, sx=None, sy=None, size=16, bold=None):
        col, mk, lc = ARROW[color]
        d = "M" + " L".join(f"{p[0]} {p[1]}" for p in pts)
        dash = ' stroke-dasharray="9 7"' if dashed else ""
        self.p.append(f'<path d="{d}" stroke="{col}" stroke-width="3" fill="none"{dash} marker-end="url(#{mk})"/>')
        if label:
            mx = lx if lx is not None else (pts[0][0] + pts[-1][0]) / 2
            my = ly if ly is not None else (pts[0][1] + pts[-1][1]) / 2 - 14
            w = 700 if (bold if bold is not None else color != "tan") else None
            self.text(mx, my, label, size=size, fill=lc, anchor="middle", weight=w)
        if step is not None:
            sx = sx if sx is not None else (lx if lx is not None else (pts[0][0] + pts[-1][0]) / 2)
            sy = sy if sy is not None else (pts[0][1] + pts[-1][1]) / 2
            self.step(sx, sy, step)

    def step(self, x, y, n):
        self.p.append(f'<circle cx="{x}" cy="{y}" r="16" fill="{INK}"/>')
        self.text(x, y + 6, str(n), size=15, fill="#FFFFFF", anchor="middle", weight=700)

    def cross(self, x, y, r=13):
        self.p.append(f'<circle cx="{x}" cy="{y}" r="{r + 5}" fill="#FFFFFF" stroke="{TERRA}" stroke-width="2.5"/>')
        k = r / 1.7
        self.p.append(f'<path d="M{x - k} {y - k} L{x + k} {y + k} M{x + k} {y - k} L{x - k} {y + k}" stroke="{TERRA}" stroke-width="3"/>')

    def save(self, path):
        self.p.append("</svg>\n")
        with open(path, "w") as f:
            f.write("\n".join(self.p))
