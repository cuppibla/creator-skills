# Layout Patterns

Recipes for the recurring slide layouts in Annie's HTML decks. Each pattern includes the HTML signal that identifies it, the PPTX recipe, and the visual QA gotchas that have actually bitten previous builds.

**Read the pattern *before* writing the slide.** The gotchas section is where the time gets saved.

## Table of contents

- [Title slide](#title-slide) — hero text, centered Google bar, pills
- [Live demo / dark slide](#live-demo--dark-slide) — dark bg, badge, ring
- [Episode roadmap](#episode-roadmap) — timed table with section labels
- [Section divider](#section-divider) — full-bleed colored slide
- [2×2 glass card grid](#2x2-glass-card-grid) — taxonomies, primitives
- [Two-column code + annotation](#two-column-code--annotation)
- [Comparison table](#comparison-table) — alternating row fills
- [Vertical flow](#vertical-flow) — numbered steps with connectors
- [Horizontal flow with arrow labels](#horizontal-flow-with-arrow-labels)
- [Schema field list](#schema-field-list) — key + type pill + description
- [Dashboard mock](#dashboard-mock) — health rows with status pills
- [Three-takeaway wrap-up](#three-takeaway-wrap-up)
- [Call to action](#call-to-action) — three cards + bottom pills

---

## Title slide

**HTML signal:** First slide of a deck, often `class="title-slide"`. Large h1, optional subtitle, pills at the bottom.

**Recipe:**
```js
s.background = { color: "F0F4FF" };
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: SW, h: SH,
  fill: { color: "FFFFFF", transparency: 40 }, line: { type: "none" },
});
H.addGoogleBar(s, 1.5, 3.5);   // centered, 3.5" wide
s.addText("Deck Title", { x: ML, y: 2.0, w: SW-ML-MR, h: 1.0,
  fontFace: FONT, fontSize: 50, bold: true, color: C.blueDk, align: "center", margin: 0 });
// ...subtitle, pills
```

**Gotchas:**
- Don't oversize the title (50pt max for 13.3" wide layout); long titles can overflow at 56pt
- Center the Google bar (`width: 3.5`) for visual symmetry with the centered text
- Pills should be horizontally centered: pre-compute `startX = (SW - totalPillsWidth) / 2`

---

## Live demo / dark slide

**HTML signal:** `class="demo-slide"`, dark `background: var(--g800)`, `.demo-badge` with a `live-dot`, often a pulsing ring.

**Recipe:**
```js
s.background = { color: C.g800 };
H.addBadge(s, ML, 0.7, 1.8, 0.34, "LIVE DEMO", C.red);  // 1.8" wide!
s.addText("Demo Title", { x: ML, y: 1.0, ..., color: C.white, ... });
H.addSlideNum(s, "X", "9AA0A6");  // light slide num on dark bg
```

**Gotchas:**
- Badge width must be 1.8" for "LIVE DEMO" at fontSize 11. 1.55" wraps to two lines (real bug from A2A deck).
- On dark slides, override slide number color to a light gray (`"9AA0A6"`).
- The pulsing ring animation drops; use a static double-circle (outer halo at 88% transparency, inner ring with colored border).

---

## Episode roadmap

**HTML signal:** `<table>` with Time / Section / Key Concept columns. Often the third slide.

**Recipe:** Use `s.addTable(rows, opts)` with `border: { type: "none" }`. Color the header row C.blue. Alternate row fills white / g50.

```js
const headerOpts = { fill: { color: C.blue }, color: C.white, bold: true, fontFace: FONT, fontSize: 14, valign: "middle" };
const cellBase  = { fontFace: FONT, fontSize: 13, color: C.g800, valign: "middle" };
const rows = [
  [{ text: "Time", options: headerOpts }, { text: "Section", options: headerOpts }, ...],
  [{ text: "4:00", options: { ...cellBase, fill: { color: C.white }, bold: true } }, ...],
  // ...
];
s.addTable(rows, { x: ML, y: 2.0, w: SW-ML-MR, colW: [1.1, 6.5, 4.3], rowH: 0.55, border: { type: "none" } });
```

**Gotchas:**
- `colW` array must sum to `w`. PPTX will silently expand if too wide (real bug from A2A deck slide 8). Verify the sum.
- Headers stay readable at 14pt; cells at 12-13pt.

---

## Section divider

**HTML signal:** `class="divider-slide"`, full-bleed gradient background, large white title.

**Recipe:** Use `H.addSectionDividerCustom(s, {...})`. See helpers reference for the per-section theme constants.

**Gotchas:**
- Long titles ("MCP vs Skills — Two Complementary Layers") need fontSize 40, not 44. The helper defaults to 40.
- Honor per-section themes when the HTML uses different `--blue` values for different `divider-slide` instances.

---

## 2×2 glass card grid

**HTML signal:** `display: grid; grid-template-columns: 1fr 1fr` with 4 children, each `.glass.glass-blue` etc.

**Recipe:**
```js
const colW = (SW - ML - MR - 0.3) / 2;
const cardH = 2.25, gap = 0.3;
cards.forEach((c, i) => {
  const col = i % 2, row = Math.floor(i / 2);
  const x = ML + col * (colW + 0.3);
  const y = startY + row * (cardH + gap);
  H.addGlass(s, { x, y, w: colW, h: cardH, tint: c.tint });
  // title (22pt bold, accent color)
  // body (14pt g800)
  // "Use for: ..." (12pt italic g600)
});
```

**Gotchas:**
- Use a 0.3" gap between columns (matches Annie's spacing rhythm).
- Title at 22pt bold in accent color; body at 14pt g800 (NOT g600 — too washed out).
- 4th card row index = `Math.floor(3/2) = 1`. Common off-by-one.

---

## Two-column code + annotation

**HTML signal:** Left side `<pre>` block, right side glass card with explanatory text.

**Recipe:**
```js
const colW = (SW - ML - MR - 0.3) / 2;
const lx = ML, rx = ML + colW + 0.3;
H.addCodeBlock(s, lx, ly, colW, codeH, [/* lines */]);
H.addGlass(s, { x: rx, y: ly, w: colW, h: ..., tint: "blue" });
// add title + text inside the glass
```

**Gotchas:**
- Estimate code block height carefully: ~0.22" per line + 0.3" padding. Underestimating leads to text overflowing the dark rect into whatever's below (real bug from ADK deck slide 23, fixed by extending block height).
- If the right column has multiple stacked cards, verify their combined height (with gaps) doesn't exceed the content area (~5.0" from y=2.0 to y=7.0).

---

## Comparison table

**HTML signal:** Wide `<table>` with feature names on left, comparison columns on right (e.g. "Skills vs MCP").

**Recipe:** Same as episode roadmap, but typically with a label column + 2 data columns:
```js
colW: [2.6, 4.65, 4.65]  // total = 11.9" (matches SW - ML - MR for std margins)
rowH: 0.45
```

**Gotchas:**
- For a comparison emphasizing color (✓ green vs ✗ red), apply `color: C.green` or `color: C.red` to the relevant cells, not to the whole row.
- 5-7 rows is the sweet spot. More than 8 starts to feel cramped.

---

## Vertical flow

**HTML signal:** Stacked `.glass` cards with small vertical lines between them. Each card has a number, title, sublabel.

**Recipe:** Use `H.addFlowStep` and `H.addFlowConnector` (see helpers reference).

```js
const steps = [
  { tint: "blue",   number: "1.", label: "Step one",   sublabel: "→ detail" },
  { tint: "green",  number: "2.", label: "Step two",   sublabel: "→ detail" },
  // ...
];
steps.forEach((step, i) => {
  const y = startY + i * (stepH + stepGap);
  H.addFlowStep(slide, { x, y, w: flowW, h: stepH, ...step });
  if (i < steps.length - 1) H.addFlowConnector(slide, x + flowW / 2, y + stepH, stepGap);
});
```

**Gotchas:**
- 5 steps fit comfortably in the content area at stepH 0.6, stepGap 0.18. More than 6 → reduce stepH.
- Connector goes from bottom of step `i` to top of step `i+1`. The height is `stepGap`.

---

## Horizontal flow with arrow labels

**HTML signal:** Boxes side-by-side with `.flow-arrow` containing a label and a thin line + arrowhead.

**Recipe:**
```js
const boxW = 2.2, boxH = 1.2, gap = 1.4;  // 1.4" gap, not 0.8"!
// Box 1, then:
const ax = bx + boxW + 0.05;
s.addText("Arrow Label", {                   // Label ABOVE arrow
  x: ax, y: flowY + 0.35, w: gap - 0.1, h: 0.3,
  fontFace: FONT, fontSize: 11, bold: true, color: arrowColor, align: "center", margin: 0,
});
s.addShape(pres.shapes.RECTANGLE, {           // Arrow shaft
  x: ax + 0.1, y: flowY + 0.78, w: gap - 0.4, h: 0.03,
  fill: { color: arrowColor }, line: { type: "none" },
});
s.addShape(pres.shapes.RIGHT_TRIANGLE, {      // Arrowhead
  x: ax + gap - 0.4, y: flowY + 0.68, w: 0.2, h: 0.22,
  fill: { color: arrowColor }, line: { type: "none" }, rotate: 90,
});
```

**Gotchas:** ⚠ This pattern has the most QA issues.

- **Gap width is critical.** "EvaluationResult" (16 chars) needs gap ≥ 1.4" at fontSize 10; "A2A: plan JSON" needs ≥ 1.3". If gap is too small, label wraps mid-word.
- **Label goes ABOVE the arrow shaft.** Earlier versions used center-vertical alignment and the label overlapped the arrow (real bug from A2A deck slide 2 & 19).
- For very long labels with narrow gaps, drop to fontSize 9 — readable, no wrap.
- For a left-pointing arrow, use `rotate: 270` on the RIGHT_TRIANGLE and shift the shaft start.

---

## Schema field list

**HTML signal:** Repeating rows of `{ key, type-pill, description }`, often inside a glass card. Used to document JSON schemas or Pydantic models.

**Recipe:**
```js
H.addGlass(s, { x, y, w, h, tint: "blue" });
s.addText("Schema Name", { ..., fontSize: 16, bold: true, color: C.blue });

const fieldH = 0.5;
fields.forEach((f, i) => {
  const fy = startY + i * fieldH;
  s.addText(f.key, { x: x+0.3, y: fy, w: 2.5, h: fieldH-0.05,           // wide key column!
    fontFace: MONO, fontSize: 11, bold: true, color: f.keyColor, valign: "middle", margin: 0 });
  H.addPill(s, x+2.85, fy+0.08, 0.55, f.type, f.typeBg, f.typeColor, 9);
  s.addText(f.desc, { x: x+3.5, y: fy, w: w-3.7, h: fieldH-0.05,
    fontFace: FONT, fontSize: 11, color: C.g600, valign: "middle", margin: 0 });
  // optional 1px divider line below
});
```

**Gotchas:**
- Key column must be wide enough for the longest key. "improvement_suggestions" at fontFace MONO fontSize 11 needs ~2.5" (real bug from A2A deck slide 15, fixed by widening key column).
- Type pill should be just wide enough for its label (`bool` → 0.55", `dict` → 0.55", `list` → 0.55"). At 0.6" some renderers add visible padding.

---

## Dashboard mock

**HTML signal:** A list of service rows, each with a status dot, name, secondary text, and a status pill. Often used to suggest a live admin UI.

**Recipe:**
```js
H.addGlass(s, { x, y, w, h, tint: "gray" });    // gray bg for dashboard "panel"
s.addText("Service Registry", { ..., fontSize: 16, bold: true, color: C.g800 });

const rowH = 0.6;
services.forEach((svc, i) => {
  const ry = startY + i * rowH;
  // status dot
  s.addShape(pres.shapes.OVAL, { x: ..., w: 0.18, h: 0.18, fill: { color: svc.dot }, line: { type: "none" } });
  // name (bold, red if error)
  // url (mono, gray)
  // status pill (right-aligned)
  H.addPill(s, x + colW - 1.3, ry + 0.09, 1.0, svc.status, pillBg, pillFg, 10);
});
```

**Gotchas:**
- Use `tint: "gray"` for the panel background — distinguishes the "UI" from the surrounding slide.
- Show one "Unhealthy" entry to make the demo idea (kill an agent → watch it go red) visually obvious.

---

## Three-takeaway wrap-up

**HTML signal:** Three large `.glass` cards side-by-side or stacked, each with a big number (1, 2, 3) and a takeaway statement.

**Recipe (horizontal version):**
```js
const colW = (SW - ML - MR - 0.4) / 3;
const cardH = 4.0;
takeaways.forEach((t, i) => {
  const x = ML + i * (colW + 0.2);
  H.addGlass(s, { x, y: ly, w: colW, h: cardH, tint: t.tint });
  s.addText(t.num, { ..., fontSize: 44, bold: true, color: t.color });    // BIG number
  s.addText(t.title, { ..., fontSize: 17, bold: true, color: t.color });  // 17pt title
  s.addText(t.body, { ..., fontSize: 13, color: C.g800 });                // 13pt body
});
```

**Gotchas:**
- The big number (44pt) is what makes this pattern read as "takeaways" rather than a generic 3-card layout. Don't shrink it.
- Card height of 4.0" gives the body room to breathe without feeling padded.

---

## Call to action

**HTML signal:** Final slide with "Try It Yourself" header, three cards with icons, bottom row of pills.

**Recipe:**
- Background: `"F0F4FF"` with white overlay at 40% transparency (matches title slide)
- Centered Google bar near top
- Large blue title (`fontSize: 46, color: C.blueDk`)
- Subtitle (18pt g600)
- Three cards horizontally, each with:
  - Icon (36pt)
  - Card title (17pt bold accent)
  - Two lines of detail (12pt g600)
- Row of 4 pills at bottom for tech stack

**Gotchas:**
- The slide should feel like a bookend to the title slide — same background treatment, same centered Google bar.
- Cards are slightly wider here (3.1") than in body slides because there are only 3 of them.

---

## When you see a pattern not in this list

1. Build it inline using the helpers
2. After QA, decide if it's truly reusable (used in ≥2 distinct decks)
3. If yes, lift into helpers.js and add a section here
4. If no, leave it inline

The library is for things Annie uses repeatedly. One-offs stay one-offs.
