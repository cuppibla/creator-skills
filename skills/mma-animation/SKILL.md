---
name: mma-animation
description: Generate Annie's explainer animations (the MMA episode b-roll system) locally in one of seven themes — classic (light Claude-Design look, default), dark, blueprint (diagram/grid), pop (playful sticker), luxe (OLED glass), minimal (Notion editorial), industrial (Swiss brutalist) — from a video script. Authors a seekable HTML timeline and renders 5K MP4 master + per-scene clips + manifest. Use whenever Annie wants an animation/b-roll/动画 for a script or episode, names any of those theme words, or wants to re-render/extend/tweak an existing animation — even if she doesn't say "skill".
---

# MMA animation — script → styled animation → MP4

Recreates the visual system of the animations in
Annie's MMA episode b-roll (originally made in Claude Design,
exported at 5120×2880/30fps) entirely locally: HTML/CSS/JS with a
deterministic seekable timeline, rendered frame-perfect via headless Chrome.

## Themes

Four visual systems share the same engine, components, big type scale, and
output contract. Annie picks by name (default: classic). Sample stills for
all themes: render `--still` frames of a sample scene per theme (see step 1).

| theme | file | look |
|---|---|---|
| `classic` | (none — base mma.css) | her light Claude-Design look; pale blue-gray, tinted pills |
| `dark` | `assets/themes/theme-dark.css` | deep navy, glowing accents + neon waveform |
| `blueprint` | `assets/themes/theme-blueprint.css` | grid paper, line-drawn boxes, dashed borders, all-mono |
| `pop` | `assets/themes/theme-pop.css` | sticker style: chunky black outlines, hard offset shadows, flat color |
| `luxe` | `assets/themes/theme-luxe.css` | high-end "ethereal glass": OLED black, mesh-gradient orbs, hairline glass, Plus Jakarta Sans |
| `minimal` | `assets/themes/theme-minimal.css` | editorial Notion/Linear: warm off-white, exact pastels, 1px #EAEAEA, Instrument Serif headlines, black active step |
| `industrial` | `assets/themes/theme-industrial.css` | Swiss brutalist print: paper + carbon ink + aviation red only, zero radius, Archivo Black uppercase, [ bracketed ] kickers |

(luxe/minimal/industrial are adapted from github.com/leonxlnx/taste-skill —
soft-skill, minimalist-skill, brutalist-skill respectively. Their fonts are
bundled in assets/fonts: Plus Jakarta Sans, Instrument Serif, Archivo Black.)

To apply: copy the theme file into the animation folder and add
`<link rel="stylesheet" href="theme-<name>.css">` AFTER the mma.css link.
Classic = no theme link. Everything else in the workflow is identical.
If she doesn't specify a theme for a new episode, use classic; if she asks
"show me styles", render `--still` frames of a sample scene per theme.

## Workflow

1. **Read `references/style-guide.md` first** — tokens, color semantics,
   motion grammar, component recipes, script→scene mapping. Follow it
   exactly; the goal is indistinguishable-from-the-originals. Theme CSS
   only re-skins — never change sizes or layout per theme.

2. **Plan scenes from the script.** Annie's scripts use `[SECTION]` headers
   and `//` beat separators. One beat = one scene, each with: a slug id
   (becomes the clip filename), a 2–4 word mono kicker, one visual metaphor,
   a duration ≈ narration time + 1s. Show her the scene table (id, kicker,
   visual, duration) before building if the animation is long.

   **Every scene MUST carry `data-script="…"`** — the narration lines
   (verbatim, condensed to first…last line if long) that the beat covers.
   This is not optional: it is what makes the clip↔script manifest
   automatic, so Annie can pick b-roll clips by script line while editing.
   The renderer warns on scenes missing it.

3. **Scaffold.** Create the animation folder (default:
   `./animations/<slug>/` under the current project) and copy in the
   runtime so it's self-contained:
   `cp ~/.claude/skills/mma-animation/assets/{mma.css,engine.js,fonts.css,template.html} <dir>/ && cp -r ~/.claude/skills/mma-animation/assets/fonts <dir>/fonts`
   Rename template.html → index.html and author the scenes.
   Do NOT restyle components ad hoc — if a new component type is genuinely
   needed, add it to the copied mma.css following the token system (and
   consider back-porting it to the skill).

4. **Preview & iterate.** Open `index.html` in the Browser pane (plain
   file:// URL — no server needed). The HUD scrub bar appears automatically
   (hidden in render mode). Scrub through every cue; screenshot key moments
   to self-check against the style guide before rendering.

5. **Render.**
   ```
   node ~/.claude/skills/mma-animation/scripts/render.mjs <dir>/index.html --clips            # 5K master + per-scene clips
   node ".../render.mjs" index.html --scale 2                                                  # fast draft (2560×1440)
   node ".../render.mjs" index.html --still 3.5                                                # single PNG frame
   ```
   5K renders take ~1s/frame — quote Annie an ETA for long timelines and
   render drafts at `--scale 2` while iterating. Masters are named after
   the folder (CamelCase), clips land in `clips/NN-<sceneid>.mp4` —
   matching her existing `mma/assets/<episode>/` convention.

6. **Deliver — the output contract is always the same folder shape:**
   ```
   <slug>/
     index.html + mma.css/engine.js/fonts…   (editable source)
     <Name>.mp4                              (5K master)
     clips/NN-<sceneid>.mp4                  (one clip per script beat)
     clips/manifest.md                       (clip ↔ time range ↔ script lines)
   ```
   Report master path, duration, resolution, and show the manifest table.
   If it's for a real episode, offer to move outputs into
   the project's assets folder for that episode.

## Cutting clips from EXISTING videos (no scene metadata)

For videos not generated by this skill — e.g. old Claude Design exports —
use the standalone cutter (only here are timecodes ever needed):
```
node ~/.claude/skills/mma-animation/scripts/cut.mjs <video.mp4> --at 0:10,0:21,1:07 [--names hook,vad,tools] [--out <dir>]
```
N cut points → N+1 clips (`NN.mp4` / `NN-slug.mp4`) + a `manifest.md`
with time ranges (script-lines column left blank to fill in). It refuses
to overwrite existing clips — point `--out` elsewhere instead.

## Engine contract (what the HTML can use)

- `<section class="scene" data-id="slug" data-dur="7">` — scenes run in
  document order, 0.35s fade through bare background between them.
- `data-at="1.2"` + `data-fx="rise|fade|pop|drop|slide-l|slide-r"` on any
  element — scene-relative entrance cue (default rise, 0.55s).
- `data-stagger="0.12"` on a container — auto-cues its children.
- `data-loop="pulse"` (+ `data-freq`) — deterministic pulse via `--ls`.
- `.wave` auto-fills bars; `.flow[data-step-times="a,b,c"]` steps the
  purple active highlight through its `.step` children.
- Everything is a pure function of `t`: `window.__mma.seek(t)` — never
  use CSS animations/transitions or Math.random for motion; the renderer
  seeks frame by frame and live playback must match the render exactly.

## Requirements

ffmpeg + system Google Chrome + node ≥18. First run:
`cd ~/.claude/skills/mma-animation/scripts && npm install` (puppeteer-core only).

## Parallel sessions (IMPORTANT)

Annie often runs several Claude sessions rendering different episodes at
once. Full renders take a slot in a cooperative queue (`~/.mma-render-queue`,
max 2 concurrent) — a render printing `[queue] both render slots busy` is
waiting its turn, not stuck, and 5K renders slow to ~2–3 s/frame when two
run. **Never `pkill` `render.mjs` or headless Chrome** — puppeteer Chrome
processes are almost certainly a sibling session's active render, not a
leak. A killed render's slot self-reclaims after 5 min. Full context:
a `RENDER-COORDINATION.md` next to the animations if several renders share one machine. For long renders
under contention, prefer scene-aligned `--from/--to` chunks + ffmpeg
concat (`-c copy`) so an interruption only loses the current chunk.
