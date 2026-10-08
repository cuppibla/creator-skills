# Long-Form Playbook — 8–15 min 深度教学

For Annie's tech tutorials (ADK / Gemini / MCP / agents). The enemy of long-form is the **sag**: a strong open, then a flat middle where viewers leave. Everything here fights the sag.

## The core model: YouTube is a satisfaction-prediction engine

The algorithm predicts whether a viewer will be satisfied, and its strongest signal is how long *previous* viewers watched. Dense, structured, actionable教学 is exactly what holds — but only if the structure gives a reason to keep watching through *each* section. A 10-min video holding 60% to the end reads as high-confidence; one losing 70% in 30s gets dropped. So: structure per-segment, not just overall.

Binge bonus: evergreen series (not news) build a binge library. Annie's series format (`multimodal-agents-cookbook`, the 12-episode arc, etc.) is ideal — each episode should end pointing at the next so watch sessions chain.

## Three teaching-arc templates — pick by video intent

### Template A — The Question Arc (best for "how does X work / why does X matter")
The whole video is one withheld answer. Open the loop in the hook, close it at the climax.

```
[0:00–0:15]  HOOK — pose the question as tension, not as a topic.
             "Your agent forgets everything between turns. Here's the fix
              nobody shows you." (NOT "Today we'll talk about memory.")
[0:15–0:45]  STAKES + PROMISE — why this matters + what they'll have by the end.
             Plant the open loop: "by the end you'll have X running."
[0:45–...]   SEGMENT 1..N — each segment opens a mini-loop, delivers a payoff,
             and hands off to the next. (See "Segment loop" below.)
[~climax]    THE ANSWER — the thing the hook promised. Don't deliver it early.
[last 30s]   RECAP in one breath → CLIFFHANGER to the next video.
```

### Template B — The Build Arc (best for "let's build X" tutorials)
The artifact is the spine. Show the finished result first (the "after"), then build to it.

```
[0:00–0:20]  COLD OPEN — show the working result. "This voice agent remembers
             you across sessions. 12 minutes, let's build it."
[0:20–0:50]  THE PLAN — 3–4 named milestones on screen. This is the open-loop
             map; each milestone is a loop that closes when you hit it.
[per milestone]  Build → hit a wall → solve it → working checkpoint.
             The wall is the retention device. No wall = no tension.
[last beat]  Run the finished thing again → "next episode we add X."
```

### Template C — The Listicle/Format Arc (best for "N things / N mistakes / N patterns")
Each item is a self-contained loop. Front-load the most surprising item, not the most obvious.

```
[0:00–0:15]  HOOK — the count + a contrarian frame. "7 agent patterns —
             #4 is the one breaking your production app."
[0:15–0:30]  Why listen to you + what changes if they apply these.
[per item]   Name it → why it matters → concrete example → micro-payoff.
             Keep items ~60–120s. Order by curiosity, not by difficulty.
[close]      The meta-takeaway → next video.
```

## The segment loop (the unit that kills the sag)

Every 60–150s segment is its own mini-video:

```
OPEN a curiosity gap  →  "The naive way to do this fails. Watch."
DELIVER the content    →  teach / build / show
CLOSE with a payoff    →  "...and that's why it works."
HAND OFF               →  "But that creates a new problem — which is segment 2."
```

Close each loop within 1–3 beats. Don't leave a gap open for 4 minutes — viewers disengage from frustration, not curiosity. The hand-off is what prevents the dead-air drop between segments.

## 节奏 — the oscillation pattern (Fireship-style)

Pacing is not "fast everywhere." It's **calm → burst → calm**, like conversation. Sustained intensity exhausts; sustained calm bores.

- **Baseline:** talking-head / screen-share pacing, one cut every **15–25s**.
- **Every 2–3 minutes:** a **burst** — 5–10 quick cuts (zoom, meme, reaction, code-highlight, B-roll, scene change) lasting 5–10s.
- Then **return to calm.** The contrast itself is what holds attention.
- Avoid the **spike-and-drop**: huge energy in the intro, then a cliff into a monotone tutorial. Bridge the intro energy into segment 1 — don't let the floor fall out at 0:45.

Other 节奏 levers for教学:
- **Density** — Fireship's whole thing. Cut "ums", restated sentences, throat-clearing. Every line earns its place. Read the script aloud; if a sentence doesn't add a fact, a loop, or a laugh, delete it.
- **"Why it works / how it evolved"** — the highest-praised教学 move: don't just show *how*, show *why this and not the old way*. That contrast is itself a retention device.
- **Signposts** — plant forward references: "this next part is the bit everyone gets wrong." Cheap, effective, keeps the viewer leaning forward.

## Cut points (卡点) in long-form

卡点 here = the edit/beat where attention could snap. Mark them and make each one *earn* the next stretch:
- **Section transitions** — title card / chapter marker + a one-line open loop for the next section. Never transition silently.
- **The wall moment** (Build arc) — the bug, the error, the "wait, that didn't work." This is the most important teaching beat and the strongest 卡点. Lean into it; don't edit it out to look smooth.
- **Pre-answer pause** — right before the climax payoff, a half-beat of "here's the thing nobody tells you." Earns the reveal.
- **CTA placement** — one mid-roll engagement prompt max ("drop your stack in the comments"), phrased so it doesn't break momentum. Don't stack 3 CTAs.

## Don'ts (long-form)

- Don't put the searched-for answer in the first 2 minutes. Tease, then earn it.
- Don't open with "Hi everyone, in today's video..." — that's setup, not a hook.
- Don't let any 90s stretch pass without an open loop, a 卡点, or a visual change.
- Don't end on "thanks for watching" — end on a cliffhanger that points to the next video.
- Don't fake-pace with flashy transitions over dead content; viewers feel the emptiness.
