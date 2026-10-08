---
name: arch-diagram
description: Draw Annie's clean white-background technical diagrams (architecture, system design, flow chart, workflow graph, loop) as hand-authored SVG rendered to PNG — the adk2-blog house style. Use whenever Annie asks for an architecture diagram, system diagram, flowchart, workflow 图, 架构图, 清晰的图, or wants dark/ugly/AI-generated diagrams redone in her blog style — even if she doesn't say "skill". NOT for felt/storybook art (that's Nano Banana) and NOT for data charts (use dataviz).
---

# arch-diagram — Annie's technical diagram house style

White background, minimal, purple-gradient LLM nodes. The style tokens below were extracted
from the shipped blog diagrams; `assets/template.svg` carries all of them.
Copy `assets/template.svg` from this skill as the starting skeleton.

## The non-negotiable workflow

1. **Read the code first.** Every box name, port, env var, file name, and edge must exist in the
   repo. Before drawing, write the node list + edge list as plain text and check each item against
   the source. A diagram invented from memory is worse than no diagram.
2. **One diagram = one question.** The title IS the claim ("The flywheel: book → judge → rewrite →
   book again"), the sub explains the mechanism in one line. If a second question appears, that's a
   second diagram.
3. **Compose before styling** (this is what separates a diagram from 一堆方块):
   - **Flow has a direction.** Left→right = time/data flow. Top→bottom = layers. Return/feedback
     edges loop back *underneath*. A reader should be able to trace one concrete scenario without
     instructions.
   - **Number the walk.** The main scenario gets ① ② ③ … step circles on its arrows (5–7 steps max).
     An architecture diagram with unlabeled or missing arrows is a parts list.
   - **Every arrow says what flows** (`POST /run`, `SSE: history + live`, `score + whys`). Solid =
     synchronous request/call. Dashed = async / stream / state write / suspend-resume.
   - **Boundaries are containers.** Dashed rounded rects grouping by *process boundary* (browser /
     server / cloud project), each with a mono header tag naming the tech and port
     (`broadcast.py · FastAPI :8323`). Never float boxes in space.
   - **Detail budget:** ≤ ~7 elements per container, ≤ ~20 per diagram. Secondary detail goes in
     small mono sublabels inside a box — never a new box. Overflow → split into another diagram.
4. **Author SVG by hand** (never Mermaid, never image-gen for these — image-gen can't hold dense
   labels; Mermaid can't hold this layout language).
5. **Render → look → fix.** Render PNG at 2× and actually Read the image. Check: clipped/overflowing
   text, overlapping boxes, arrowheads landing on borders (not inside boxes), orphan boxes with no
   edges, serpentine arrows pointing the right way, legend matching what's actually drawn. Iterate
   until clean.

## Style tokens (exact)

- Canvas: width 1600, height to fit (800–1050). Background `#FFFFFF`.
- Title: 34px bold `#0F172A` at x=70. Sub: 20px `#64748B` right below.
- Fonts: `-apple-system, "SF Pro Text", "Helvetica Neue", Arial` for prose;
  `"SF Mono", Menlo, Consolas` for anything code-flavored (node names, paths, labels).
- **Node taxonomy — locked, never recolor:**
  - LLM / agent / model call → rounded rect, gradient `#6366F1 → #8B5CF6`, white mono label with
    `✦` prefix.
  - Deterministic judge / pure function → white rect, `#10B981` 2px border, `#047857` label.
  - Plain function / infra → white rect, `#94A3B8` border, `#0F172A` label.
  - Decision → diamond `#FFFBEB` fill, `#F59E0B` 2px stroke, `#92400E` mono label.
  - Human / suspend (HITL, RequestInput) → amber like decision, `⏸` marker.
  - Terminal success → `#ECFDF5` fill, `#10B981` border (`✓ SHIP`-style).
  - Data artifact (file, dataset, evalset) → white rect, `#F59E0B` border, small dog-ear optional.
- Arrows: `#94A3B8` 2px, triangle marker. Colored only when the edge is the star: purple `#8B5CF6`
  return/feedback edge, green `#10B981` success exit — always with a bold colored label.
- Step circles: 15px-radius circle, `#0F172A` fill, white 14px bold number.
- Containers: `#F8FAFC` at 60% opacity, `#94A3B8` 2px dashed, rx 18; mono header tag `#334155`.
- Amber caveat strip (optional, bottom): `#FFFBEB` fill, `#FDE68A` border; bold `#92400E` first
  line, `#B45309` second line. One caveat only — the thing worth remembering.
- Legend row above the strip when >2 node kinds appear: small swatch + 14px label per kind.

## Text fits or it doesn't ship

Approx widths: 13px mono ≈ 7.8px/char · 14px mono ≈ 8.4 · 15px mono ≈ 9.0 · 16px sans ≈ 8.2.
Budget every label against its box width before writing it; wrap with manual `<tspan>` lines
(≤ 2 sublabel lines per box). If it doesn't fit, shorten the words, not the font.

## Render pipeline

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --force-device-scale-factor=2 --window-size=1600,<H> \
  --screenshot=out.png "file:///abs/path/diagram.svg"
```

`<H>` must equal the SVG height attribute. Keep the `.svg` source next to the shipped `.png`
(`img/src/` in a lab repo) so the next edit is a text edit, not a redraw.
