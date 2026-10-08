---
name: google-brand-deck
description: Convert HTML slide decks into editable PowerPoint files in Annie's Google Brand visual style — Google Sans typography, glass-tinted cards, dark code blocks with syntax highlighting, blue gradient section dividers, the four-color Google bar. Use this whenever Annie uploads HTML slide files and wants a .pptx (which she'll typically import to Google Slides), wants a deck in her usual visual system, or asks for a Google-branded presentation. Trigger even if she doesn't say "skill" or "Google Brand" — uploaded `.html` files containing `--blue:#4285F4` CSS variables or `.glass` classes are the strongest signal.
---

# Google Brand Deck — HTML → PPTX

Annie's visual system for talks, workshops, and YouTube content. Built from her ADK / A2A / MCP / A2UI decks. Output is `.pptx` that imports cleanly to Google Slides with every element editable.

## When to use this

- HTML slide files (single or multiple) uploaded for conversion
- A "build me a deck about X in my usual style" request, where no HTML is supplied — generate the HTML mentally, then go straight to PPTX using the same primitives
- A request to extend or remix an existing deck Annie has produced before

If she names a specific connector or asks for Google Slides direct API output, fall back to the .pptx + manual import path. There's no Slides MCP connector available; .pptx + one click in Drive is the cleanest workflow today.

## The full workflow

```
1. Read every uploaded HTML file before writing any code
2. Inventory the slide count and per-slide layout patterns
3. Flag CSS features that need approximation (see references/css-mapping.md)
4. Confirm with Annie: total count, any themes to preserve, deliverable name
5. Write the build script (helpers.js + theme.js + per-slide blocks)
6. Render to PDF, screenshot every slide
7. Visual QA — fix overflow, wrapping, overlap, clipping
8. Re-render until clean
9. Copy to /mnt/user-data/outputs/ and call present_files
```

Never skip step 6. Every deck so far has had at least one issue that only surfaced after rendering (code block overflowing a card, table extending past its column, badge wrapping to two lines, arrow label clashing with arrow). Budget ~2-3 fixes per deck.

## Inventory the deck first

Before writing any pptxgenjs code, scan each HTML and write down:

- Total slide count across all files (`<div class="slide"`)
- Section structure — usually `S1, 1-A, 1-B, ..., S2, 2-A, ...` with section dividers between
- Per-section color themes — check the `.divider-slide` and `.section-tag` CSS, sometimes each section uses a different accent (blue / green / red / yellow). Honor these.
- Special slides that break the pattern — title, live demo (dark or with badges), wrap-up CTA, code-heavy slides
- New layouts not in the helper library — see "When you need a new helper" below

If the user asks for a quick build with no surprises, you can skip writing inventory down and go straight to coding. But for decks over ~15 slides, the inventory pass saves time.

## The helper library

All helpers are in `scripts/helpers.js` and palette in `scripts/theme.js`. Copy both into the working directory, then `require('./helpers.js')` and start building.

Read `references/helpers-reference.md` for the full API. The quick list:

- `addGoogleBar(slide, y, width?)` — four-color top accent
- `addSectionTag(slide, text, x, y, color?)` — small uppercase letter-spaced label
- `addSlideHeader(slide, sectionTag, title, caption?, tagColor?)` — section tag + h2 + optional caption + google bar
- `addSlideNum(slide, num, color?)` — bottom-right slide number
- `addGlass(slide, {x, y, w, h, tint})` — semi-transparent tinted rounded rect (blue/green/yellow/red/plain/gray)
- `addCodeBlock(slide, x, y, w, h, lines)` — dark rounded rect with syntax-colored monospace runs
- `addPill(slide, x, y, w, text, bg, fg, fontSize?)` — small rounded label
- `addBulletList(slide, items, x, y, w, h, opts?)` — colored-dot bullet list with rich-text support
- `addQuote(slide, text, x, y, w, h?, accent?)` — italic quote with left accent bar
- `addSectionDividerCustom(slide, opts)` — full-bleed colored divider slide
- `addFlowStep(slide, opts)` + `addFlowConnector(slide, x, y, height)` — vertical step diagrams

The starter template at `scripts/starter.js` has the imports wired and a title slide ready to extend.

## The patterns

Most slides Annie's HTML decks contain are one of these patterns. Read `references/patterns.md` *before* writing a slide — it has the table of contents, the HTML signal that identifies each pattern, the PPTX recipe, and (critically) the visual QA gotchas that have actually bitten previous builds.

Patterns covered:

- Title slide with hero text, four-color bar, pills
- Live demo / dark slide
- Episode roadmap with timed table
- Section divider (blue or per-section theme)
- 2×2 glass card grid (taxonomies, primitives)
- Two-column layout with code + annotation
- Comparison table with alternating row fills
- Vertical flow with connectors
- Horizontal flow with arrow labels
- Schema field list with type pills
- Dashboard mock with health rows
- Three-takeaway wrap-up
- Call to action with three cards

## CSS features that don't translate cleanly

PPTX has no equivalent for several CSS features Annie's decks use. The approximations are documented in `references/css-mapping.md`. The short version:

| CSS feature | PPTX approximation |
|---|---|
| `backdrop-filter: blur()` | semi-transparent tinted rounded rect + soft shadow |
| `background: linear-gradient(...)` | solid color + transparent overlay rectangle |
| CSS animations (pulse, fade) | static visual, drop the motion |
| `flex-wrap` for pill rows | manual position math per pill |
| Google Sans web font | spec it; Slides falls back to Roboto (close enough) |
| Custom emoji | render as text; many emoji work, some need swaps |

When in doubt, accept the visual loss and tell Annie in the delivery note. Don't try to fake a blur.

## Visual QA checklist

After rendering to PDF, view every slide and check:

1. **Text overflow** — does text extend past the box that contains it?
2. **Wrapping** — does a key label wrap awkwardly (one word per line, mid-word break)?
3. **Overlap** — do adjacent elements overlap?
4. **Code blocks** — does the code extend past the dark rounded rectangle?
5. **Tables** — do column widths sum to the table width? (PPTX tables expand if too wide)
6. **Arrow labels** — do they overlap their arrows?
7. **Section dividers** — long titles can run off the right edge; shrink font if needed
8. **Dark slides** — slide number color should be light, not the default gray

When fixing, prefer making the box bigger over making the text smaller. Annie's design system favors generous spacing. Only shrink fonts as a last resort for labels.

## Approximate slide dimensions

LAYOUT_WIDE = 13.333" × 7.5" (16:9, maps from 1920×1080 HTML proportionally)

Standard left/right margins: 0.7"
Standard content area: ~12" wide × 6" tall after header
Two-column gap: 0.3"
Three-column gap: 0.2"

## When you need a new helper

If the HTML uses a layout pattern not in the helper library:

1. Build it inline first (don't pre-abstract)
2. After QA, if the pattern is genuinely reusable, lift it into helpers.js
3. Add a pattern doc to `references/patterns/`

Resist the urge to add a helper for a one-off layout. The library is for things Annie uses repeatedly.

## Delivery

1. `cp` the final .pptx to `/mnt/user-data/outputs/`
2. Call `present_files` with the path
3. Write a 3-paragraph delivery note: what's in it, the Google Slides import flow, any fidelity approximations made (font fallback, gradient flattening, etc.)
4. Offer to extend it if there's a next section coming

## Tone for delivery notes

Annie prefers:
- Honest about what didn't translate ("CSS animations dropped, glass blur approximated")
- Not over-apologetic — just state the tradeoff and move on
- Skip the "let me know if you'd like changes" closer; her workflow is to iterate explicitly

## File organization

```
google-brand-deck/
├── SKILL.md                   # this file
├── scripts/
│   ├── theme.js               # palette, fonts, dimensions
│   ├── helpers.js             # all add* functions
│   └── starter.js             # blank build script template
└── references/
    ├── helpers-reference.md   # full API for every helper
    ├── css-mapping.md         # CSS feature → PPTX equivalent
    └── patterns.md            # all layout patterns + QA gotchas
```
