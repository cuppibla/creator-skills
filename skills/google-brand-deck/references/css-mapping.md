# CSS → PPTX Mapping

PPTX is a fixed object model (shapes on a canvas) while HTML/CSS is fluid (flex, grid, blur filters, animations). This document records the standard approximations for Annie's design system. When you encounter a CSS feature, look it up here before improvising.

## backdrop-filter: blur(40px) saturate(1.8)

**PPTX equivalent:** Semi-transparent tinted rounded rectangle + soft shadow.

Implemented in `addGlass()`. The HTML achieves a frosted-glass look by blurring whatever is behind the card. PPTX has no blur filter, so we approximate with:
- Rounded rectangle (radius 0.12") matching the visual shape
- Fill: color at 92% transparency (so the background shows through subtly)
- Border: same color at 75% transparency for a soft edge
- Drop shadow: 0.05 opacity, 8pt blur, 1pt offset

Reads as glass-like in context. Don't try to fake the blur with a separate blurred image — it costs too much for too little.

## linear-gradient(135deg, blue, blueDk)

**PPTX equivalent:** Solid fill + transparent overlay rectangle on one side.

The HTML uses gradient backgrounds for title slides and section dividers. PPTX *does* support gradients natively but pptxgenjs has spotty gradient support across renderers. Cleaner approach:

```js
slide.background = { color: C.blue };
slide.addShape(pres.shapes.RECTANGLE, {
  x: SW * 0.5, y: 0, w: SW * 0.5, h: SH,
  fill: { color: C.blueDk, transparency: 50 }, line: { type: "none" },
});
```

This gives a two-tone diagonal feel that reads as a gradient at slide-deck scale. Annie can right-click → Format options → Gradient in Slides if she wants to upgrade to a true gradient.

## CSS animations (pulse, fade-in, transition)

**PPTX equivalent:** Drop them. Render the static end-state visual.

The HTML has `@keyframes pulse-dot` on the "LIVE DEMO" badge red dot, and ring pulsing on demo slides. Slides supports custom animations but they're a different mental model (entry/exit/emphasis effects per element). Don't try to recreate them — Annie's decks don't depend on motion.

If a slide is *entirely* about showing motion (like an animated diagram explaining how something works), tell Annie the slide will be static and offer to add Slides-native entrance animations after the file opens in Slides.

## flex-wrap for pill rows

**PPTX equivalent:** Manual position math per pill.

There's no native auto-wrap layout. The pattern:

```js
const innerW = colW - 0.6;
let px = x + 0.3, py = y + 0.75;
const pillVGap = 0.12, pillHGap = 0.1, pillH = 0.32;
pills.forEach((p) => {
  const pw = Math.max(0.7, Math.min(1.55, p.length * 0.085 + 0.2));
  if (px + pw > x + 0.3 + innerW) {
    px = x + 0.3;
    py += pillH + pillVGap;
  }
  H.addPill(s, px, py, pw, p, pillBg, pillFg, 10);
  px += pw + pillHGap;
});
```

Width is approximated as `length * 0.085 + 0.2` for fontSize 10. Adjust the coefficient if using a different size.

Limitation: if Annie edits a pill label in Slides, the layout won't reflow. Mention this in the delivery note if pills are central to a slide.

## Google Sans web font

**PPTX equivalent:** Specify `"Google Sans"`; Slides falls back to Roboto.

Google Sans is internal to Google and not available in Slides by default. If Annie has it installed on her Google account it'll render natively. Otherwise Slides substitutes Roboto, which is visually very close.

In the delivery note, offer two paths:
1. Quickest: select all in Slides → font → Roboto
2. Closer: Extensions → Fonts → "More fonts" to add Google Sans if available

For monospace, use `"Roboto Mono"`. "Google Sans Mono" exists but is rarely installed.

## Custom emoji + symbols

Most emoji render correctly: 🗺 ✓ ✗ 🏃 ☁ 🏠 🤖 🚨 ⚠ 📦 🔧 🚀 🎬 📖 💻 🎨 🔮 🔄 🛡 🏘 💰 🎯 📏

Edge cases:
- Some emoji look different on Mac vs Windows vs Linux rendering. If a deck is rendering server-side via LibreOffice for QA, you'll see Linux emoji rendering, which differs from what Slides shows on a Mac.
- Avoid skin-tone modifiers and complex ZWJ sequences (👨‍🏫 etc.) — patchy support.

If an emoji is critical and rendering oddly in the LibreOffice preview, don't panic — Slides on Annie's machine will likely render it correctly. Note it in the delivery and let her check.

## CSS `:hover`, `:focus`, transitions

**PPTX equivalent:** N/A. Drop them.

## `position: absolute` with z-index

**PPTX equivalent:** Object stacking order is determined by add order. Add background elements first, foreground elements last. Use `z-index: 99` in HTML as a signal to add that element last in the build script.

## SVG inside HTML

**PPTX equivalent:** Recreate using pptxgenjs shape primitives (`RECTANGLE`, `OVAL`, `RIGHT_TRIANGLE`, `ROUNDED_RECTANGLE`) or embed as an image.

For simple arrows / chevrons / dots, use shapes. For complex SVGs (icons, illustrations), it's faster to render the SVG to PNG and add as an image. PPTX supports inline images.

## Tables with `border-collapse: separate; border-radius`

**PPTX equivalent:** `pres.addTable(...)` with `border: { type: "none" }`, color the header row, alternate row fills.

PPTX tables don't have rounded corners. Accept the visual loss. The alternating row fills + colored header carries the visual style.

## `code` (inline monospace inside prose)

**PPTX equivalent:** Use rich-text runs with `fontFace: MONO`.

```js
s.addText([
  { text: "The function ", options: { fontFace: FONT, fontSize: 13, color: C.g800 } },
  { text: "call_agent()", options: { fontFace: MONO, fontSize: 12, color: C.g800 } },
  { text: " is the one entry point.", options: { fontFace: FONT, fontSize: 13, color: C.g800 } },
], { ... });
```

Notice the monospace size is 1pt smaller than the prose to compensate for monospace fonts looking visually larger.

## CSS variables (`var(--blue)`)

The HTML uses CSS custom properties. These are just constants. Map them directly to `C.blue`, `C.green`, etc. in `theme.js`. If the HTML defines a variable not in our palette, add it to theme.js rather than hardcoding the hex inline.
