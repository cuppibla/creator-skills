---
name: plain-script
description: Write a presentation / teaching script that a 16-year-old can follow (深入浅出) for one of Annie's decks, labs or talks — one idea per slide, the real term said first and explained straight (no analogy-first), the app's visual mapped in passing, question before the answer, spoken sentences, every term explained on first use, seconds per slide. Use whenever Annie asks for a presentation script / 讲稿 / 演讲稿 / 逐字稿 / talk track for a deck, or says "16岁小孩能懂" / "深入浅出" / "讲得简单点" / "小白也能懂" — even if she doesn't say "skill". For the final read-aloud polish hand the result to teleprompter-polish; for retention restructuring use script-doctor.
---

# plain-script — a script a 16-year-old can follow

The deck says *what*; the script says *why it matters* in words a smart 16-year-old already
owns. The test at every line: would a 16-year-old with no programming background nod, or
reach for a dictionary? A reach means bridge it, replace it, or cut it.

## Inputs (read them, don't remember them)

1. The deck itself — the `slides` array (titles, chips, which diagram is on screen) and the PNGs.
2. The code the slides are about (the lab repo). A script must never say something the code
   doesn't do. When in doubt, read the file the slide names.
3. Her story plan for the deck (`*-story-plan.md`), so the acts and the one-line 口号 per act match.

## The recipe

1. **One sentence per slide, first.** Before writing any script, write the slide's single idea
   as one plain sentence. If you cannot, the slide is wrong — say so instead of scripting it.
2. **Say the real thing, straight.** Name the term first, then say what it does in plain words:
   "This is session state. It's a dictionary the agent keeps for one conversation." Do NOT lead
   with an analogy and reveal the term afterwards — she found analogy-first confusing ("你的比喻
   反而非常confusing 直接说不好吗"). Plain words means short, concrete, mechanism-level: what
   writes it, what reads it, when, and what breaks without it.
3. **Map the app's picture in passing, never instead of the term.** Her labs have a story world
   (the tower: slip / books / drawer / cards / floor four). When that picture is on screen, add
   ONE short sentence after the real explanation — "on screen, that's the slip on the desk" — and
   put the mapping in its own column. Give the whole mapping once, on the agenda slide, as a
   table (on screen · the real thing). If the picture isn't on screen, say nothing about it.
   Every slide = SAY IT STRAIGHT (term + mechanism) → SO WHAT (what breaks / what you can now do)
   → ON SCREEN (one sentence, only if the app is showing). For a Chinese audience: 中文解释 +
   (English term), never the term alone.
4. **Question before answer at every act boundary.** Open each act with a question the audience
   has felt in real life ("你昨天跟客服说过的话，今天她还记得吗？"), not with a definition.
5. **Show the failure, then the fix.** Her labs run it broken → write the line → watch it light;
   the script follows that order. The term is still said the moment the thing is on screen.
6. **Language rules:** ≤ 18 words per sentence · one verb per sentence · say numbers as words
   unless they are on screen · no "basically / essentially / obviously / simply" · no "it" twice in
   a row (name the thing) · a comma is a breath · contractions are fine · address "you".
7. **The 16-year-old gate (mandatory table):** list every technical term the script uses —
   term · first slide · how it was said. Any term without a plain explanation gets one or gets cut.
8. **Callbacks:** each act has one 口号 (e.g. "filed is not remembered"); say it on the act's
   first slide and again on its last, word for word.
9. **Timing:** ~130 spoken words per minute; 40–70 words per slide; write the seconds next to
   each slide and total them. A 56-slide deck ≈ 40–45 minutes.
10. **Format:** one table per act — `Slide | Say | On screen | Sec` — each spoken sentence on its
    own line inside "Say", the app mapping (or —) in "On screen"; then the terms table; then a
    short "cuts" note (what the deck says that the script deliberately skips). Plain weight only
    (no bold CJK); English table headers.
11. **Then** hand the script to `teleprompter-polish` for the read-aloud pass. Do not skip the
    gate to get there faster.

## The reference output

The week-4 Archive script (private vault) — all 56 slides of the
week-4 Archive deck in this voice (she approved the directness after rejecting an analogy-first
draft). Two slides, to hear it:

| Slide | Say | On screen | Sec |
|---|---|---|---|
| 12 · EDIT ONE | The whole edit is one line.<br>tool_context.state[CASE] = case — write the dictionary into session state.<br>Without it, case is a local variable. It dies when the function returns.<br>State is written by code, never by the conversation.<br>The model can say "I've written that down" all day. Unless code writes state, nothing is written. | — | 30 |
| 24 · Two policies, one shelf | For the agent to remember what you said, two separate things must happen.<br>Something has to write to the memory service. And something has to search it later.<br>The write policy: at closing time, the file node sends the whole session's events to the memory service. One call: add_events_to_memory.<br>The recall policy: before the agent answers, a recall node searches the memory service with your question. One call: search_memory. That's the line you'll write.<br>Two decisions: what to keep, and when to look. ADK gives you the two verbs. It doesn't make either decision. | the memory service is the shelf on floor three | 50 |

## What this is not

- Not a 人设文 / persona piece — those are harvested from her own speech, never written
  (`feedback-persona-scripts-must-be-harvested`). This skill is for tutorial / explainer scripts only.
- Not a retention pass. Hooks and 卡点 hang on the teaching spine (why → what → take it apart →
  what each part replaced → diagram + code → tradeoff); they never reorder it.
