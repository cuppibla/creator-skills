---
name: cream-deck
description: Build Annie's 课件 decks and their diagrams in the Agent-Memory workshop's cream/felt system, and export them to PPTX with the talk track as speaker notes — sparse diagrams (字少, big direction only), felt corner icons, ink boxes, tan arrows, one bottom line, and the deck HTML with the workshop chrome (act tag, memory chip, page number). Use whenever Annie asks for 课件 / a deck / slides / diagrams for a lab, a workshop or the Agent 101 series, or says "按之前的风格" / "workshop 那套" / "米色" / "毛毡" — even if she doesn't say "skill". NOT for blog/white technical diagrams (use arch-diagram) and NOT for video b-roll animation (use mma-animation).
---

# cream-deck — Annie's 课件 system (workshop cream + felt)

The style source of truth is the Agent-Memory workshop deck; the fullest worked example is
week 4 of Agent 101 Live (56 slides, 29 diagrams, eight review passes — every rule below came
out of one of them). Both are bundled: `assets/example-index.html` is the week-4 deck and
`assets/example-make_cream.py` its 29 diagrams.

## The rules she gave (non-negotiable)

1. **字少 — big direction only.** She rejected dense diagrams three times ("太密了 根本看不清楚
   不需要这么细致 大方向OK就行了"). A diagram is boxes with a *name* and at most one short sub,
   arrows with one or two words, at most one cream strip, one bottom line. No note paragraphs,
   no 8-line code panels, no second line of small print. Same for slides: captions ≤ 12 words.
2. **No story-character names in 课件.** The lab may have Vesper / the elder; the deck says
   *the agent*, *you*, *the season*. Model boxes are `✦ agent` / `✦ model`. ("课件里能不要提
   elder吗 很奇怪 并没有方便理解").
3. **Read the code first, draw from the code.** Every box name is a name in the repo; every
   call shape is the installed package's (for ADK: read `.venv/lib/python3.*/site-packages/google/adk/...`,
   not docs). She asks "要符合事实的 code 情况".
4. **Teach the concept generically before the lab instance.** For a named concept (RAG, graph
   RAG, MATCH, a memory service) the deck needs an explicit "what X is" diagram first — three
   steps, generic — then the lab's wiring. Schema diagrams show keys AND cardinalities (she
   asked for the many-to-many). Ladder: why → what is it → take it apart → what each part
   replaced → diagram + code → tradeoff.
5. **One idea per diagram.** Title = the claim. If a second question appears, it is a second slide.
6. **Render → look at EVERY PNG at full 1600×900 → fix → look again — before showing her.**
   Thumbnail-only review shipped clipped labels, arrowheads under boxes and lines through text;
   she noticed ("你真的有仔细研究…吗 生成的图都不对"). Then screenshot every deck slide too.
7. **When she says a style is wrong, copy HER screenshot's system** (colours, chrome, icon slot),
   don't re-paint from a generic skill. This skill IS that system; use it as-is.

## The paint

| token | value | used for |
|---|---|---|
| bg / frame | `#FAF6F0` / `#F0EADD` | slide, containers (55% opacity) |
| ink / sub / tan | `#2A2520` / `#8A8378` / `#C9BCA9` | text, secondary text, default arrows and borders |
| green / greend | `#6E9A68` / `#4E7A48` | tools, writes, "good" |
| purple / purpled / purplebg | `#8B7EC8` / `#6B5FA8` / `#F5F3FB` | the model (`✦`, filled), reads, cloud containers |
| amber / amberd / amberbg | `#C08A2E` / `#9A6D20` / `#FDF6E8` | stores on disk, keys, "lit" |
| terra / terrabg | `#C96442` / `#FBEDE7` | failure, crosses, "before the edit" |
| caveat strip | `#FBF3E2` on `#E8D9B8`, text `#8A5A2B` | the one strip per diagram |

Layout grammar (1600×900): title 46px/800 at (90,96); optional sub 22px at y=140 (≤ 12 words,
must clear the icon at x≥1360); felt icon 150×150 rx26 at (1360,28); content between y=200 and
y=800; bottom line 26px/800 at y=862 (`line1`), optional 16px body under it; strip = 56px cream
band (`strip`). Boxes white, 3px stroke, rx20, name mono 700 + one sub. Arrows 3px with triangle
markers, colour = what flows (tan default · green tool/write · purple model/read · amber store).
Step circles ink r16 only on the main walk (≤ 5). Dashed rounded containers = process / cloud
boundaries with a mono tag top-left. Dark panel (`panel`) = code or a prompt, ≤ 2 lines (≤ 4 for
a query). Stores (`store`) = a frame with white rows, ≤ 3 rows.

Budget per diagram: ≤ 12 boxes · ≤ 60 words outside code · ≤ 1 strip · ≤ 1 step walk.

## Workflow

1. **Story plan first** (`week4-deck-story-plan.md` is the model): acts = the lab's ladder, each
   act opens on a "where we are" card, one line per slide saying what it shows. Review with her
   before drawing anything ("先别急着生成课件 我们一起理一下故事脉络").
2. **Diagrams:** copy `assets/svgkit_cream.py` + `assets/build_cream.sh` into `<deck>/img/src/`,
   write `make_cream.py` there (start from `assets/example-make_cream.py` — 29 sparse patterns:
   tower/act cards, pipelines, two-column verbs, timelines, schema→graph, MATCH, RAG ladder,
   tables). Each function = one diagram, saved as `c<N>-<slug>.svg`. `./build_cream.sh` inlines
   the felt icons and renders `../c*.png` at 2×. Text width ≈ 0.6 × font-size per character —
   size boxes from that, then check the render anyway.
3. **Review every PNG at 1600×900** (resize the 2× PNG, Read it). Fix overflows, labels on
   arrows, subs under icons, arrowheads hidden by step circles. Repeat.
4. **Deck:** copy `assets/example-index.html` → `<deck>/index.html`, replace the `slides` array.
   Slide types: `title` · `scene` (art + one caption) · `cast` (three cards, ≤ 1 sentence each) ·
   `pains` (three quotes) · `image` (a full-bleed diagram PNG) · `shot` (screenshot + cap + ≤ 12-word
   sub; `tall:true` for portrait shots, `art:true` for paintings) · `code` (one card, ≤ 5 lines,
   kicker ≤ 10 words) · `line` (three big lines) · `cliff` (two cards) · `loop` · `lab`. Chrome:
   act tag bottom-left, memory chip top-centre (`mem`, ≤ 4 words), page number bottom-right.
   Tags `S1…` must be sequential (renumber with a regex after inserting).
5. **Screenshot every slide** with `assets/shoot_deck.py /abs/index.html OUT` and Read the grids.
6. **Serve:** `python3 -m http.server <port> --bind 127.0.0.1` in the deck folder; tell her the
   `127.0.0.1` URL (on her Mac another process may hold `[::1]:8477`, so `localhost` can land on a
   different deck). Never kill a port you did not open.
7. **PPTX, when she asks for one** (she asks for both an editable and a flat file). Copy
   `assets/{deckdata,extract_layout,build_pptx,verify_pptx}.py` into `<deck>/tools/`, then:

   ```bash
   python3 tools/extract_layout.py     # real geometry of every slide, out of the browser
   python3 tools/build_pptx.py         # <Deck>-editable.pptx and <Deck>-flat.pptx
   python3 tools/verify_pptx.py 1 12   # data check on all slides + re-draw those two
   ```

   `extract_layout.py` renders a copy of the deck in headless Chrome and reads back every box,
   text run and image with its exact position and computed style, so the editable PPTX lands
   where the HTML deck lands instead of re-implementing the CSS. `build_pptx.py` replays that
   into native text boxes and shapes, attaches each diagram's SVG to its PNG (PowerPoint:
   right-click → Convert to Shape), and writes the talk track into the speaker notes of both
   files. `verify_pptx.py` checks every source element is placed and every word is present,
   and can re-draw a slide from the PPTX under its browser screenshot for eyeballing.
   One CSS pixel = 7620 EMU = 0.6 pt, so a 1600×900 deck is exactly 13.333in × 7.5in.

8. Keep a README in the deck folder (slide map by act, diagram table "file · slide · the
   question it answers", re-render commands) and note the pass in her story plan.

## Assets

- `assets/svgkit_cream.py` — the paint: `Svg`, `title/text/lines`, `box/model/container/store/
  panel/note/cylinder/icon/arrow/step/cross`, `KIND` colours. `note()` exists but is off-budget;
  use `strip` (in the example make file) instead.
- `assets/build_cream.sh` — render script (Chrome 2×, icons from `assets/icons/`, `ICONS=` to override).
- `assets/example-make_cream.py` — the week-4 set, sparse: copy functions as patterns.
- `assets/example-index.html` — a complete working deck (56 slides) to start from.
- `assets/shoot_deck.py` — per-slide screenshots + 2×2 review grids.
- `assets/deckdata.py` · `assets/extract_layout.py` · `assets/build_pptx.py` · `assets/verify_pptx.py`
  — the PPTX pipeline (step 7).
- `assets/icons/icon-{bell,bike,cloud,desk,jar,notepad,polaroid,shelf,thread,warehouse}.png` — the
  felt corner icons (`s.icon("desk")`). New icons: Nano Banana in the same felt register
  (see `Topics/agent-memory-workshop/slide-diagrams/icons/gen_icons.py`).

## Gotchas

- Headless Chrome hangs on the second launch if you pass `--user-data-dir`; launch it bare, one
  slide per process, absolute `file://` path.
- `title(t, sub)` draws the sub at full width — keep it short or it runs under the icon.
- Emoji in SVG text render fine in Chrome; keep them out of mono labels wider than the box.
- Dense first cuts of every diagram are in `week4-deck/img/src/make_cream_dense.py` — the
  before/after of rule 1, if you need to see what "too dense" looked like.
- The extractor's copy of the deck lives in `build/`, so it needs a `<base href>` back at the
  deck root or no image loads and every picture comes out the wrong size.
- Wait for `document.images` to decode before measuring; a `.shot` frame sizes itself from the
  image's natural size.
- `RGBColor` is a tuple subclass: `"#%s" % color.rgb` raises. Use `"#" + str(color.rgb)`.
- Keynote is not a reliable way to check a generated PPTX — it front-documents whatever it
  restored on launch. Verify with `verify_pptx.py` instead, and leave her apps alone.
