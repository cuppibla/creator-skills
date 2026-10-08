# Helpers Reference

All helpers live in `scripts/helpers.js` and are accessed via the `H` object returned by `createHelpers(pres, theme)`. Constants come from `scripts/theme.js`.

## H.addGoogleBar(slide, y, width?)

Four-color top accent bar (blue, red, yellow, green).

- `slide` — pptxgen slide object
- `y` — vertical position in inches (default 0.42 for top of content slide)
- `width` — optional; if provided, the bar is centered horizontally at this width. Useful on title slides where the bar is a feature (3.5" wide, centered). Without `width`, it spans the content area (margin to margin).

## H.addSectionTag(slide, text, x, y, color?)

Small uppercase letter-spaced label like "SECTION 1 · ORCHESTRATION".

- Default color is `C.blue`. Pass `C.tagOnBlue` etc. when placing on a colored divider background.
- Internally uses `charSpacing: 4` for the letter-spaced look.

## H.addSlideNum(slide, num, color?)

Bottom-right slide number ("1-A", "S2", etc.).

- Pass a lighter color (`C.tagOnBlue` or similar) on dark/colored backgrounds.

## H.addSlideHeader(slide, sectionTag, title, caption?, tagColor?)

Composite helper. Adds:
1. White background
2. Google bar at top (y=0.42)
3. Section tag at y=0.7
4. h2 title at y=1.0 (30pt bold, g800)
5. Optional caption at y=1.75 (15pt g600)

Use this on virtually every content slide. The content area below the header starts around y=2.0 (with caption) or y=1.75 (without).

## H.addGlass(slide, {x, y, w, h, tint})

Tinted semi-transparent rounded rectangle — the visual workhorse of Annie's decks.

Tints: `'blue' | 'green' | 'yellow' | 'red' | 'plain' | 'gray'`

- `blue/green/yellow/red` — 8% colored tint with matching border at 25% opacity
- `plain` — white with subtle gray border
- `gray` — light gray (g50) with gray border

Always reads as a "card" in context. Stack text and other elements on top.

## H.addCodeBlock(slide, x, y, w, h, lines)

Dark code block with syntax-colored monospace runs.

`lines` is a 2D array. Each line is an array of segments:

```js
[
  [{ t: "def", c: C.kw }, { t: " " }, { t: "get_agent", c: C.fn }, { t: "():" }],
  [{ t: "    agent = get_base_agent()" }],
  [{ t: "    agent.name = " }, { t: "\"my_name\"", c: C.str }],
]
```

- `t` — text
- `c` — color (use `C.kw`, `C.str`, `C.cm`, `C.fn`, `C.op`; defaults to `C.codeFg`)
- `size` — font size override (defaults to 11)

Syntax color palette:
- `C.kw` — keywords (`def`, `class`, `return`, `if`, `for`, `import`)
- `C.str` — strings (anything in quotes)
- `C.cm` — comments (`# ...`)
- `C.fn` — function names (typically the name in `def foo():` or call sites you want to highlight)
- `C.op` — operators / numbers / special punctuation

**Sizing rule of thumb:** at 11pt with `line-height: 1.6`, a code block needs roughly `0.22"` per line of vertical space, plus 0.3" for padding. So a 10-line block needs h ≈ 2.5".

## H.addPill(slide, x, y, w, text, bg, fg, fontSize?)

Small rounded label.

- Height is fixed at 0.32"
- Width is your responsibility — pre-compute based on text length or use a fixed grid
- For approximate text-width math at fontSize 10: `width ≈ length * 0.085 + 0.2`
- `bg` and `fg` are hex strings; use `C.pillBlue` etc. for light tints

## H.addBulletList(slide, items, x, y, w, h, opts?)

Bullet list with colored dots.

`items` is an array of `{ dot?, text }`:

```js
[
  { dot: C.blue, text: "Plain string bullet" },
  { dot: C.red,  text: [
    { text: "Rich text with ", options: { fontFace: FONT, fontSize: 13, color: C.g800 } },
    { text: "bold", options: { fontFace: FONT, fontSize: 13, color: C.g800, bold: true } },
    { text: " inside", options: { fontFace: FONT, fontSize: 13, color: C.g800 } },
  ]},
]
```

- `dot` defaults to `opts.defaultDot` or `C.blue`
- `opts.fontSize` (default 13)
- `opts.lineH` (default 0.34") — vertical spacing per item

## H.addQuote(slide, text, x, y, w, h?, accent?)

Italic quote with colored left accent bar (4px wide).

- `accent` defaults to `C.blue`. Use `C.red` / `C.green` / `C.yellowDk` to match section themes.
- Background is g50 (very light gray) so it stands apart from the white slide.

## H.addSectionDividerCustom(slide, opts)

Full-bleed colored divider slide.

```js
H.addSectionDividerCustom(slide, {
  tag: "SECTION 1 · 4:00 – 16:00",
  line1: "Section Title —",
  line2: "Continuation of Title",
  subtitle: "Optional one-line subtitle below the title",
  slideNum: "S1",
  bgColor: C.blue,
  bgColorDk: C.blueDk,
  tagColor: C.tagOnBlue,
});
```

Per-section themes:
- Blue: `bgColor: C.blue, bgColorDk: C.blueDk, tagColor: C.tagOnBlue`
- Green: `bgColor: C.green, bgColorDk: C.greenDk, tagColor: C.tagOnGreen`
- Red: `bgColor: C.red, bgColorDk: C.redDk, tagColor: C.tagOnRed`
- Yellow/Orange: `bgColor: C.yellowDk, bgColorDk: C.yellowDkD, tagColor: C.tagOnYellow`

## H.addFlowStep + H.addFlowConnector

For vertical flow diagrams (numbered steps connected by short lines).

```js
const flowX = ML + 0.5, flowW = 5.5, stepH = 0.6, stepGap = 0.18;
const steps = [
  { tint: "blue",   number: "1.", label: "Scan agents/skills/", sublabel: "→ shared skills" },
  { tint: "green",  number: "2.", label: "Merge by name", sublabel: "— local wins" },
];
steps.forEach((step, i) => {
  const y = startY + i * (stepH + stepGap);
  H.addFlowStep(slide, { x: flowX, y, w: flowW, h: stepH, tint: step.tint,
                          number: step.number, label: step.label, sublabel: step.sublabel });
  if (i < steps.length - 1) {
    H.addFlowConnector(slide, flowX + flowW / 2, y + stepH, stepGap);
  }
});
```

## H.addArrowRight(slide, x, y, len?, color?)

Single right-pointing arrow with shaft + triangular arrowhead. Useful in horizontal flow diagrams; place labels above using separate `addText` calls.

For an arrow pointing *left*, manually compose the shaft and use a `RIGHT_TRIANGLE` with `rotate: 270`.

## H.addBadge(slide, x, y, w, h, text, color)

Rounded pill badge with a colored dot to the left of the text. Used for "LIVE DEMO" markers.

Sizing: at fontSize 11, a 1.55" wide badge fits "LIVE DEMO" on one line. "Live Demo" (mixed case) is wider — use 1.8" or convert to uppercase.

## Constants quick reference (from theme.js)

```js
// Colors
C.blue, C.blueDk, C.red, C.redDk, C.yellow, C.yellowDk, C.yellowDkD, C.green, C.greenDk
C.g800, C.g600, C.g200, C.g100, C.g50, C.white
C.codeBg, C.codeFg
C.kw, C.str, C.cm, C.fn, C.op   // syntax colors
C.pillBlue, C.pillGreen, C.pillRed, C.pillYellow
C.tagOnBlue, C.tagOnGreen, C.tagOnRed, C.tagOnYellow

// Typography
FONT  // "Google Sans"
MONO  // "Roboto Mono"

// Dimensions
SW   // 13.333
SH   // 7.5
ML   // 0.7
MR   // 0.7
```
