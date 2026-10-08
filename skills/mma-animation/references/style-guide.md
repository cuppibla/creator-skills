# MMA explainer style guide

Reverse-engineered from Annie's Claude-Design episode animations
(`~/Documents/video_editing/mma/assets/*/*.mp4`, 5120×2880 @ 30fps).
Every new animation must be indistinguishable in style from those.

## The look in one paragraph

Pale blue-gray canvas (`#ECF2F6`), enormous whitespace, ONE idea per scene.
A letter-spaced mono kicker pill floats top-center and names the scene.
Content sits centered in the upper two-thirds. Vocabulary: outlined tinted
pills, white cards with soft cool shadows, glowing gradient orbs (the
agent/model as a character), blue waveforms, step-flows with amber arrows
where the active step fills **purple** and glows. Rounded extra-bold Nunito
for words, JetBrains Mono for anything technical. Calm, springy, friendly.

## Color semantics (use them consistently)

| Color | Token | Meaning in the system |
|---|---|---|
| Blue `#1670EC` | `--blue` | primary/system/structure; browser, DB, headers, waveform |
| Green `#3DA35F` | `--green` | user side, input, mic-up, "fn" markers, success |
| Amber `#F6A500` | `--amber` | flow/motion: arrows, sequence energy, warm kickers |
| Purple `#7860FD` | `--purple` | THE model / active state / decision — the star color. Active steps fill solid purple + glow |
| Ink `#2F3947` | `--ink` | headlines; use sparingly, most text is colored |
| Muted `#5C6673` | `--muted` | captions under diagrams |

Tints (`--blue-tint` etc.) fill pills/chips; solid accents are borders/text.

## Typography

- Words: **Nunito** 800–900 (variable font bundled). Headlines 56px, step
  boxes 40px, pills 34px, captions 30px (all at 1280×720 CSS canvas).
  (Scale bumped twice on 2026-07-22 — Annie found smaller sizes unreadable
  in edit. NEVER shrink text to fit; simplify or stack the layout instead.
  Captions and chips are the elements she flagged — keep them ≥30px/20px.)
- Technical: **JetBrains Mono** 700. Kickers 24px UPPERCASE ls 0.22em;
  chips 20px ls 0.18em; code/fn names 34px; table/speech 24–28px.
- Horizontal groups of pills/cards use `class="row"` (wraps + centers when
  wide) — never a fixed-width inline flex that can overflow the canvas.
  Max ~2 pills per row at these sizes; 3 short ones can fit — verify with
  a still. Prefer stacking vertically when labels are long.
- Never use plain sentences on screen — short labels only (2–6 words).
  The narration carries the sentences; the animation carries the metaphor.

## Layout rules

- Canvas 1280×720 CSS px. Render at `--scale 4` → 5120×2880 (matches masters).
- Kicker at top 36px, centered, ALWAYS present, names the scene's idea.
- Content centered horizontally, vertically biased UP (content area ends
  96px from top); bottom third mostly empty.
- Max ~3 visual groups per scene. If a beat needs more, split the scene.
- Left/right split for comparisons (exact vs fuzzy, TTS vs Live).

## Motion grammar

- Scene = one script beat (her scripts separate beats with `//` and
  sections with `[BRACKETS]`). Scene length ≈ narration time + 1s pad
  (typ. 5–10s). Scenes fade in/out 0.35s through the bare background —
  the videos show a blank canvas flash between scenes; that's intentional.
- Entrances: `rise` (default, 26px up-fade), `pop` (scale w/ overshoot —
  orbs, emphasis), `fade`, `slide-l/slide-r` (for left/right comparisons).
  Duration 0.55s. Stagger sibling items 0.10–0.15s (`data-stagger`).
- Cue elements to land WITH the narration line, not before.
- Loops: orb `pulse` (freq 0.55Hz), waveform always moving. Subtle —
  ±2.5% scale on the orb.
- Step-flows: highlight steps sequentially (`data-step-times`), ~0.8s per
  step; the purple fill + glow does the storytelling.
- End of animation: hold the final state ~1s (add pad to last scene).

## Component recipes (copy-paste)

Kicker: `<div class="kicker kicker--amber" data-at="0.2" data-fx="drop">TWO JOBS · ONE LOOP</div>`

Pill row:
```html
<div style="display:flex; gap:22px" data-stagger="0.35" data-at="0.6">
  <div class="pill pill--green">↑ send mic audio up</div>
  <div class="pill">↓ receive voice back</div>
</div>
```

Flow with stepping highlight:
```html
<div class="flow" data-step-times="3.2,4.0,4.8,5.6" data-stagger="0.12" data-at="2.0">
  <div class="step step--blue">Open</div><div class="arrow">→</div>
  <div class="step step--green">Send</div><div class="arrow">→</div>
  <div class="step step--blue">Receive</div><div class="arrow">→</div>
  <div class="step step--amber">Play</div>
</div>
```
(arrows inherit the stagger; that's fine — they trickle in left to right)

Orb + waveform (the voice agent):
```html
<div class="orb-wrap" data-loop="pulse" data-at="0.8" data-fx="pop">
  <div class="orb__halo"></div><div class="orb"></div>
</div>
<div class="wave" data-bars="30" data-at="1.4" data-fx="fade"></div>
```

Card with chip: `<div class="card" data-at="1.0"><span class="chip chip--purple">DECIDES</span><div class="card__title">Gemini Live</div></div>`

Tool row: `<div class="fn-chip" data-at="1.2"><span class="fn">fn</span><span class="name">play_playlist()</span></div>`

Caption under a diagram: `<div class="caption" data-at="2.6">running independently, at the same time</div>`

## Big-type mode + metaphor components

The house system for one-idea beats (calibrated on
`animations/ep2-new-classic/partone-adkvoice-roadmap` — read that file
before authoring a new big-type piece; it is the reference).

Type: `.mega` = the big statement WORD, **96px** — `--xl` 120px for a hero
word or a 2–3 char numeral, `--sm` 78px for a long word or a two-line
statement. Max ~12 chars per line; break with `<br>`, never shrink to fit.
`.numeral` = a giant chapter numeral 01/02/03 (250px, `--ring` 150px).
`.mega-sub` (40px) puts a phrase under the word; `.mega-emoji` is 112px.
Colors via `--blue/green/amber/purple/red/faint`.
(`.giant`/`.giant--sm` are the OLD names for `.mega`/`.mega--sm`, kept as
aliases at the same sizes; prefer `.mega` in new work.)

SIZE IS CALIBRATED — **96 / 120 / 78**, set by Annie on 2026-09-09 after
stepping down twice from 130 → 112 → 96 ("大的字可以再小一点"). She had
earlier rejected 165–300px words as "too big". Big and obvious, NOT filling
the frame; the belt/diagram must stay the hero, the word is the caption.

Never let a beat be *only* a big word. Each one pairs the word with a
metaphor component that shows the mechanism:

| component | shows |
|---|---|
| `.lane` (`--green`) | a labelled open audio line: ↑/↕ glyph + label + live wave |
| `.strike-wrap` + `.strike` | a red sweep cancelling the old way (width driven by `--p`) |
| `.cutrow` + `.cutline` + `.wave--dim` | a sentence cut in half — live bars, red cut, dead bars |
| `.blocks` + `.blk` | pieces snapping into a stack (column-reverse: DOM = bottom→top) |
| `.ring-wrap` + `.ring` (`--sm`) | a turning dashed ring — the loop, or a spinning record |
| `.duplex` / `.pipe` / `.belt` | two endpoints, packets moving BOTH ways at once |
| `.shatter` | a word knocked out of line, per-letter `--r` / `--y` |
| `.onair` | the broadcast lamp — a pulsing red dot, plants "live" |
| `.fn-chip` | a tool call as the proof that the agent can act |
| `.conveyor` | **the belt** — moving tread, turning end pulleys, a masked lane of `.plates` that step exactly one slot (`--sp`) per loop so it tiles seamlessly. `--slim`/`--sushi`/`--xl`/`--rev`/`--green`/`--purple`. Put `data-loop="pulse"` + `data-freq` on the `.conveyor` itself: one `--lp` drives tread, pulleys and cargo together, off ABSOLUTE t — so the belt never resets between scenes and consecutive clips butt seamlessly |
| `.chunk` | one discrete packet riding the belt (mini bar-chart). `--green/--purple/--sm` |
| `.wave--belt` | the opposite of packets: ONE unbroken waveform on the belt — use it the moment the point is "continuous, no message boundary" |
| `.belt-end` / `.duo` | the endpoints either side of a belt; `.duo` is the 3-column grid that keeps two stacked lanes aligned |
| `.plaque` | a mono API name-plate (`LiveRequestQueue`, `send_realtime()`); `--green`/`--sm`, `.plaque-pin` is the ↓ that nails it to the belt |
| `.ptt` | a push-to-talk button shown held **down** (`--down`) — "hold the talk button" |
| `.boundary` | a dashed message divider stamped with a red ✕ — "there is no clean boundary" |
| `.part` + `.part__tile` (`--green/--amber/--purple/--ghost/--mini`) | an ability/part as a big emoji in a tinted square; `.parts` rows them, `.rig` wires a hub tile to a row of three (the agent + its abilities) |
| `.callrow` + `.ringing` | 📞 → 🔧 — the agent literally CALLS a tool; `.ringing` rocks the phone on `--ls` |
| `.beltstage` + `.overbelt` | a slot hanging over the belt lane so a `.fn-chip` can DROP onto a flowing conversation mid-stream (ep3 "acts mid-conversation") |
| `.djbtn` (`--blue/--amber/--off/--sm`) + `.djrow` / `.djslot` | a big round pressable DJ-deck button (▶ ⏭ ⏸ as inline SVG); `--off` + `.djbtn__x` is the locked state with a red ✕ stamped on. Swap lit→locked inside a `.djslot` (lit `data-fx="vanish"`, locked `pop` at the same cue) — "it cannot press this" (ep3 part three) |
| `.menucard` + `.mitem` / `.mslot` | a diner MENU card (dashed-rule mono header) you hand the model; items are `--sm` buttons + a label that is ghost "······" until its `.mval` pops — "a menu of abilities" |
| `.talk` + `.bubble` | the model tile + a speech bubble holding a `.mega` word — "on its own it can only produce words" |
| `.codecard` + `.cline` (`--blue/--green/--amber/--purple`) | key = value definition lines that light up one at a time (`.cval` cue); the agent definition, or a function's name / description / when-to-use |
| `.morph` + `.morph__arrow` | 3-column grid: menu item → amber arrow → `.fn-chip` — "each action is a function" |
| `.checkpoint` + `.conveyor--gate` + `.gate` | **the checkpoint** (ep3 rule two, `before_tool_callback`): 🧠 tile · belt · 🔧 tile with a hanging stop-arm gate over the lane. `--a` 0 = shut / 1 = open; cue it with `data-fx="shut"` / `"open"` on the `.gate` itself (lamp flips red↔green with the arm); `.gate--open` is the static open state; `.gate__badge` perches an emoji on it (👀 watching, ✋ catching) |
| `.rider` (+ `--stop`) | a `.fn-chip--sm` riding the gate lane. `data-fx="arrive"` slides it INTO its spot from `--tx` behind (a call reaching the gate), `"depart"` slides an already-visible one away (let through), `"go"` appears and moves (a `.result` heading back to the model = negative `--tx`, or a pass-through from `--x:-330px`). `.rider--stop` rests its right edge just short of the arm whatever the chip width |
| `.logbar` + `.logslot` / `.logpill` | "one place": a single LOG strip; ghost pills (`--ghost`, `vanish`) swap for values (`pop`) as calls pass the gate |

Scenes are SHORT: 3–4s for a single line, 6–9s for a multi-line beat.
One narration line = one scene = one clip, so the b-roll cuts on the script.

`data-fx="vanish"` is the only EXIT cue: visible from scene start, fades
and shrinks away at its `data-at`. With `.swap` / `.swap__item` it lets one
spot hold a sequence of words.

## Script → scene mapping

Her script format: `[SECTION NAMES]` in brackets, beats separated by `//`
or blank lines, one takeaway per part. Mapping:

1. Each **beat** (a few narration lines making one point) = one scene.
2. Scene `data-id` = short slug (`hook`, `theloop`, `vad`, `recap`) —
   these become the clip filenames `NN-id.mp4`, matching her existing
   `assets/<episode>/clips/` convention.
3. The kicker text = the beat's idea in 2–4 mono words
   ("LIVE DEMO", "TWO JOBS · ONE LOOP", "TOOLS · SHE CAN ACT").
4. Takeaway beats: 2–3 stacked pills restating the part's points.
5. Recap: re-show the episode's key diagrams compressed.

## Added by ep3 tenth-part (2026-09-16) — checkpoint + browser components

| component | shows |
|---|---|
| `.browser` + `.browser__bar/__url/__page/__line` | a browser window the agent drives; `.wbtn` (`--down`) is a big web button, `.winput` + `.typed` (stagger-cued `<i>` chars) + `.caret` is a field being typed into, `.progress` + `.progress__fill[data-fx="fill"]` a loading bar, `.cursor` the pointer (`data-fx="glide"` flies it onto the target, `.ripple[data-fx="ripple"]` is the click) |
| `.gate` (inside `.conveyor`, or `.gatebox` solo) | **the CHECKPOINT** — a boom barrier on the belt: `.gate__post/__hinge/__arm/__signwrap`; `.gate__arm[data-fx="lift"]` swings up; `.gate--flag` hangs the sign off the post so a lifted arm never crosses it; `.gate__hand` ✋ |
| `.rider` | the tool call riding the belt: `data-fx="ride-in"` parks it 12px short of the arm; a nested `[data-fx="ride-out"]` wrapper sends it on through; `.peek` 🔍 / `.stamp` ✅ sit above it |
| `.checklist` + `.check` (`__box/__num/__ghost`) | a checklist card of empty boxes |
| `.blk--lbl`, `.readout`, `.say`, `.wave--sm`, `.fn-chip .tail`, `.part--x` | labelled policy block, a mono `0.00s ✓` readout, what the user said in a bubble, a small wave in a bubble, policy emoji on a tool chip, a red ✕ over a part tile |

Custom fx contract used there: `lift`, `fill`, `ride-out` are visible at rest (like `vanish`);
`glide`, `ripple`, `ride-in` are hidden until cued. Sizes are the calibrated ones — do not shrink.

## Added by ep3 real-code pass (2026-09-17) — the editor card

| component | shows |
|---|---|
| `.editor` + `.editor__bar/__dots/__tab` + `.editor__body` > `.eline[data-n]` | **REAL CODE** as a light VS Code–style screenshot: tab = the real file path, gutter = the real line numbers (`data-n=""` on a wrapped continuation line), tokens `.kw .fn .str .doc .num .ty .cm .fold`(⋯ = folded region). One `.eline` per source line, `white-space: pre`, ONE line of HTML each. `data-stagger` on the body types the lines in. `.spot`/`.veil` on an `.eline`, an `.egroup` (a wrapped pair) or an inline `.tok`. `.tok .over` = an old value overlaid on the new one (put the FINAL text in flow so the card is sized for it, the old value in `.over`, vanish/pop both at the same cue); `.eline--grow` = a continuation line that grows in when the fix makes the line longer. `--new` green glow = "the function we just added"; `--dark` = IDE dark. Code is 26px (the one sub-30px exception — a real line of Python must fit): ≤ ~60 chars per line, wrap like an editor, fold what the beat isn't about. Use it wherever the narration says "on screen"; keep `.codecard` for concept beats. Source of truth for ep3: `~/Documents/Demo/live-dj/genai_sdk/tools.py`, `live-dj-adk/backend/{tools,agent}.py`, `live-dj-adk-recording/backend/{tools,policy}.py`. |
| `.cline--in` | an indented line inside a `.codecard` (the block under an `if:`) |
| `.quote--wrap` | a real (long) description sentence pulled out big, wrapping to two lines |


## Added by ep4 (2026-09-19) — the browser-control agent

Built for `animations/ep4-new-classic` ("Give Your AI Agent Real Hands"): a live
voice agent driving a real Chrome through CDP. The episode's whole argument is
**snapshots, not a video stream**, so the polaroid is the through-line — it
appears in 11 scenes and every other component is staged around it.

| component | shows |
|---|---|
| `.polaroid` (`--sm`) + `.polaroid__page` / `__cap` | THE SNAPSHOT — a framed mini page. `.flash` + `data-fx="flash"` is the shutter blowing out over a `.browser`; `data-fx="fly"` (with `--fx`/`--fy`) sends the polaroid from the page into the model's hands. **`.browser` sets `overflow:hidden`, so a flying polaroid must be anchored to `.content`, not nested in the browser.** |
| `.filmstrip` (inside `.conveyor__lane`) + `.rec` / `.rec__dot` | the anti-pattern: frames streaming nonstop into the model, and the 📹 REC lamp that names the guess before it gets crossed out |
| `.shotframe` + `.crosshair` (`.ch-v/.ch-h/.ch-dot`, `--cx`/`--cy`) + `.coord` (`--green`) | clicking by coordinates: dashed lines converging on a button, then `x = 412` / `y = 287` |
| `.flow--loop` + `.flow__return` | a `.flow` that returns to its first step — look·think·act·look again |
| `.token` | a server-side action token plaque (dashed purple) |
| `.tuckwrap` + `.tucked` + `data-fx="tuck"` | fire-and-forget: a chip dropping BEHIND the belt while the wave keeps flowing on top. **Named `.tucked` because the base sheet already owns `.behind` as a dim backdrop layer.** |
| `.hands` / `.hand` (`--l`/`--r`) / `.hand__tool` | the agent's real hands either side of the orb — the episode title card |
| `.wall` (`--wx`, inside `.conveyor`) | dead air drawn: the belt runs into a brick wall |
| `.toggle` + `b.is-on` (`.is-on--green`) | a two-state answer switch (⚡ ACTION ↔ ⏳ READ) |
| `.rulebook` + `.rule` / `.rule__ghost` / `.rule__txt` | a rule card that starts as empty ghost lines and writes itself one line per beat |
| `.stampwrap` + `.stamp-big` + `data-fx="stamp"` / `"bounce"` | a stamp that LANDS on a chip, or one that bounces off and falls away (the ⚡ that will not stick to a read tool) |
| `.eyes` + `data-fx="look"` (`--lx`) | the model opens its eyes and turns them toward the browser |
| `.ghostslot` | a dotted empty slot waiting to be filled |
| `.rstation` (`--t/--r/--b/--l`, `--purple/--green/--amber`) | stations placed around a `.ring-wrap` — a loop made of stops |
| `.dasharrow`, `.plumb`, `.seltag`, `.drawline` + `data-fx="draw"`, `.browser--mini` | a dashed arrow between two things · dim grey plumbing · a mono selector tag stuck to a web button (`#search-btn`) · a dashed line that draws itself · a small browser that sits beside a tool chip |

Also back-filled the base `.spot` / `.veil` rules — the sheet previously shipped
only their positional overrides inside the editor section, so a `.spot` on an
`.eline` rendered as nothing.
