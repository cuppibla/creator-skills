"""The week-four diagrams in the Agent-Memory workshop style — the SPARSE set.

    python make_cream.py            writes c*.svg beside this file
    ./build_cream.sh                inlines the felt icons and renders PNGs (Chrome, 2×)

Rule (Annie, 2026-09-21): 字少 — big direction only. One idea per diagram, boxes
with a name and at most one short sub, arrows with one or two words, one bottom
line. The dense first cut is kept as make_cream_dense.py.
"""
from svgkit_cream import (Svg, INK, SUB, TAN, GREEN, GREEND, PURPLE, PURPLED, PURPLELT,
                          BLUE, BLUED, AMBER, AMBERD, TERRA, HEAD, KIND, PURPLEBG, AMBERBG,
                          GREENBG, CAVBG, CAVLN, CAVINK, FRAME, BOUND, TERRABG)


def line1(s, head, body=""):
    s.text(90, 862, head, size=26, fill=INK, weight=800)
    if body:
        s.text(90, 892, body, size=16, fill=SUB)


def strip(s, y, text, h=56):
    s.p.append(f'<rect x="90" y="{y}" width="1420" height="{h}" rx="16" fill="{CAVBG}" stroke="{CAVLN}" stroke-width="2"/>')
    s.text(800, y + h / 2 + 7, text, size=18, fill=CAVINK, anchor="middle", weight=700)


# ── the tower, six framings ─────────────────────────────────────────────────
FLOORS = [  # bottom → top
    ("desk", "the desk · the slip", "this visit", "session.state"),
    ("f1", "floor one · the books", "every visit, kept", "SqliteSessionService"),
    ("f2", "floor two · your drawer", "this visitor, every time", "the user: prefix"),
    ("f3", "floor three · the cards", "what was said, as facts", "Vertex AI Memory Bank"),
    ("f4", "floor four · the season", "everybody else's visits", "BigQuery"),
]
ACTS = {
    "agenda": (None, [], "TONIGHT", "Does she remember?", "what · how long · who for", "Four floors, four answers."),
    "act1": (["desk", "f1"], [], "ACT ONE · THE DESK", "Does she remember what you said a minute ago?",
             "tool_context.state[CASE] = case", "Nothing is remembered on its own. Code writes it."),
    "act2": (["f2"], ["desk", "f1"], "ACT TWO · YOUR DRAWER", "And a month from now?", 'CASE = "user:case"',
             "A session is one visit. A prefix is a lifetime."),
    "act3": (["f3"], ["desk", "f1", "f2"], "ACT THREE · THE CARDS", "Her form has four lines. Where does the rest go?",
             "found = await ctx.search_memory(query)", "Filed is not remembered."),
    "act4": (["f4"], ["desk", "f1", "f2", "f3"], "ACT FOUR · THE SEASON", "Has anybody else had this?",
             "MATCH (m:Mark)<-[:stamped]-(i:Item)<-[a:asked]-(v:Visitor)", "Other people's visits are a warehouse, not her memory."),
    "final": (["desk", "f1", "f2", "f3", "f4"], [], "EVERY FLOOR LIT", "A record is not a memory.",
              "what to keep · when to look", "Facts and preferences belong in different stores."),
}


def tower(which):
    lit, done, step, q, line, note = ACTS[which]
    s = Svg(); s.icon("desk")
    s.text(90, 96, "Who remembers what?" if which == "agenda" else "Where we are in the tower", size=46, fill=INK, weight=800)
    y0, fh, gap = 790, 96, 14
    for i, (key, name, holds, keep) in enumerate(FLOORS):
        y = y0 - i * (fh + gap) - fh
        is_lit = lit is not None and key in lit
        is_done = key in done or (which == "agenda")
        stroke = AMBER if is_lit else (TAN if not is_done else "#B0A490")
        fill = "#FDF6E8" if is_lit else "#FFFFFF"
        s.p.append(f'<rect x="90" y="{y}" width="640" height="{fh}" rx="20" fill="{fill}" stroke="{stroke}" stroke-width="{3.5 if is_lit else 2.5}"/>')
        s.text(120, y + 42, name, size=23, fill=INK if (is_lit or is_done) else TAN, weight=800)
        s.text(120, y + 72, holds, size=16, fill=SUB if (is_lit or is_done) else TAN)
        s.text(704, y + 58, keep, size=16, fill=AMBERD if is_lit else (SUB if is_done else TAN), mono=True, anchor="end", weight=700 if is_lit else None)
    s.p.append('<rect x="90" y="798" width="640" height="7" rx="3" fill="#2A2520"/>')
    s.text(800, 330, step, size=18, fill=SUB, mono=True, weight=700)
    words, cur, rows = q.split(), "", []
    for w in words:
        if len(cur) + len(w) > 28:
            rows.append(cur.strip()); cur = ""
        cur += w + " "
    rows.append(cur.strip())
    for i, r in enumerate(rows):
        s.text(800, 394 + i * 60, r, size=50, fill=INK, weight=800)
    yl = 394 + len(rows) * 60 + 6
    s.p.append(f'<rect x="800" y="{yl}" width="{min(720, 26 + len(line) * 11.5)}" height="52" rx="12" fill="{"#FDF6E8" if which != "agenda" else "#F5F3FB"}"/>')
    s.text(816, yl + 34, line, size=18, fill=AMBERD if which != "agenda" else PURPLED, mono=True, weight=700)
    s.text(800, yl + 96, note, size=20, fill=SUB)
    s.save(f"c0-tower-{which}.svg")


# ── c1 · the slip: written by a tool, read by the prompt ────────────────────
def c1_slip():
    s = Svg(); s.icon("notepad")
    s.title("The slip: written by a tool, read by the prompt")

    s.p.append('<rect x="90" y="230" width="430" height="300" rx="20" fill="#FFFFFF" stroke="#6E9A68" stroke-width="3.5"/>')
    s.text(116, 272, "the tool writes", size=18, fill=GREEND, mono=True, weight=700)
    s.text(116, 300, "write_down()", size=22, fill=INK, mono=True, weight=700)
    s.panel(116, 320, 378, 100, [("case[field] = value", "#F3EDE3"), ("tool_context.state[CASE] = case", "#F2C766")], size=15.5, lh=30)
    s.text(116, 462, "← the gold line is EDIT ONE", size=15, fill=SUB)
    s.arrow([(520, 380), (566, 380)], color="green", label="write", ly=364)

    s.store(570, 230, 460, 300, "session.state", "one dictionary", [
        "no:       k7f2", "item:     lantern", "mark:     q7", "symptom:  goes out at night"], row_h=38)
    s.arrow([(1030, 380), (1076, 380)], color="purple", label="read", ly=364)

    s.p.append('<rect x="1080" y="230" width="430" height="300" rx="20" fill="#8B7EC8"/>')
    s.text(1106, 272, "the instruction reads", size=18, fill="#FFFFFF", mono=True, weight=700)
    s.text(1106, 300, "house(ctx) · every turn", size=22, fill="#FFFFFF", mono=True, weight=700)
    s.p.append('<rect x="1106" y="320" width="378" height="130" rx="14" fill="#6B5FA8"/>')
    s.lines(1128, 352, [("THE SLIP —", "#EDE9F7"), ("  no: k7f2 · item: lantern", "#F2C766"), ("  mark: q7 · symptom: goes out…", "#F2C766")], size=15, lh=28)
    s.text(1106, 486, "so she knows the case", size=15, fill="#EDE9F7")

    strip(s, 620, 'before EDIT ONE: the tool says "written" — and state stays empty')
    line1(s, "State is written by code, never by the conversation.")
    s.save("c1-slip.svg")


# ── c2 · one file, two windows ──────────────────────────────────────────────
def c2_one_file():
    s = Svg(); s.icon("desk")
    s.title("One file, two windows")

    s.container(90, 210, 640, 220, "the Archive · :8440", "tab 3")
    s.box(120, 270, 580, 120, "Runner(…, session_service)", "SqliteSessionService(archive.db)", kind="ink", name_size=22, mono_sub=True)
    s.container(870, 210, 640, 220, "the workbench · adk web :8000", "tab 2")
    s.box(900, 270, 580, 120, "adk web", "--session_service_uri=sqlite:///archive.db", kind="ink", name_size=22, mono_sub=True)

    s.cylinder(800, 560, rx=130, ry=26, h=90)
    s.text(800, 616, "archive.db", size=24, fill=INK, mono=True, anchor="middle", weight=700)
    s.text(800, 690, "every event of every visit", size=16, fill=SUB, anchor="middle")
    s.arrow([(410, 430), (410, 500), (690, 500), (690, 532)], color="amber", label="writes every event", lx=550, ly=488, size=15)
    s.arrow([(1190, 430), (1190, 500), (910, 500), (910, 532)], color="amber", label="opens the same visit", lx=1050, ly=488, size=15)

    strip(s, 730, "Ctrl+C: the process dies. The visit doesn't — it was in the file.")
    line1(s, "Three slashes.", "sqlite:///archive.db is a file · sqlite://archive.db (two) silently means in-memory")
    s.save("c2-one-file.svg")


# ── c3 · which drawer ───────────────────────────────────────────────────────
def c3_drawers():
    s = Svg(); s.icon("shelf")
    s.title("Which drawer?", "five characters decide how long the slip lives")

    s.box(90, 330, 300, 110, "write_down()", "state[CASE] = case", kind="green", name_size=22, mono_sub=True)
    s.arrow([(390, 365), (430, 365), (430, 285), (466, 285)])
    s.box(470, 240, 300, 90, 'CASE = "case"', "as shipped", kind="tan", name_size=21)
    s.arrow([(390, 405), (430, 405), (430, 485), (466, 485)], color="purple")
    s.box(470, 440, 300, 90, 'CASE = "user:case"', "EDIT TWO", kind="purple", name_size=21)
    s.arrow([(770, 285), (836, 285)])
    s.box(840, 240, 340, 90, "this visit", "gone at closing time", kind="ink", name_size=22)
    s.arrow([(770, 485), (836, 485)], color="purple")
    s.box(840, 440, 340, 90, "this visitor", "every visit after this", kind="purple", name_size=22)
    s.text(1010, 372, "🗓 a month later", size=15, fill=SUB, anchor="middle")
    s.cross(1010, 400, r=10)
    s.text(1010, 590, "✓ still there", size=15, fill=GREEND, anchor="middle", weight=700)

    s.text(1250, 262, "(none)", size=17, fill=INK, mono=True, weight=700); s.text(1350, 262, "this visit", size=17, fill=SUB)
    s.text(1250, 302, "user:", size=17, fill=PURPLED, mono=True, weight=700); s.text(1350, 302, "every visit", size=17, fill=SUB)
    s.text(1250, 342, "app:", size=17, fill=INK, mono=True, weight=700); s.text(1350, 342, "everyone", size=17, fill=SUB)
    s.text(1250, 382, "temp:", size=17, fill=INK, mono=True, weight=700); s.text(1350, 382, "this turn", size=17, fill=SUB)

    line1(s, "A session is one visit. A prefix is a lifetime.")
    s.save("c3-drawers.svg")


# ── c4 · two policies, one shelf ────────────────────────────────────────────
def c4_two_policies():
    s = Svg(); s.icon("jar")
    s.title("Two policies, one shelf", "what gets kept · when to look")

    s.store(1140, 200, 370, 250, "memory_service", "the shelf", ['"I read by it at night…"', '"I\'ve tried hanging it…"', '"it was a gift"'], row_h=36, size=14.5)

    s.text(90, 236, "CLOSING TIME", size=14, fill=GREEND, mono=True, weight=700)
    s.box(90, 250, 220, 90, "[close]", "🌙", kind="ink", name_size=22)
    s.arrow([(310, 295), (346, 295)])
    s.box(350, 250, 180, 90, "route()", kind="green", name_size=22)
    s.arrow([(530, 295), (566, 295)])
    s.box(570, 250, 260, 90, "file()", "the write policy", kind="green", name_size=22)
    s.arrow([(830, 295), (1136, 295)], color="green", label="add_events_to_memory", lx=983, ly=278, size=15)

    s.text(90, 436, "THE NEXT VISIT", size=14, fill=PURPLED, mono=True, weight=700)
    s.box(90, 450, 220, 90, "a question", kind="ink", name_size=22)
    s.arrow([(310, 495), (346, 495)])
    s.box(350, 450, 180, 90, "route()", kind="green", name_size=22)
    s.arrow([(530, 495), (566, 495)])
    s.box(570, 450, 260, 90, "recall()", "the recall policy", kind="green", name_size=22)
    s.arrow([(830, 495), (1136, 495)], color="purple", label="search_memory · EDIT THREE", lx=983, ly=478, size=15)
    s.cross(983, 520)
    s.text(983, 556, "before EDIT THREE: nobody looks", size=14, fill=TERRA, mono=True, anchor="middle")

    s.arrow([(700, 540), (700, 616)], color="purple")
    s.box(570, 620, 260, 90, "state[RECALLED]", kind="ink", name_size=22)
    s.arrow([(830, 665), (876, 665)])
    s.box(880, 620, 240, 90, "house(ctx)", "THE TOWER lines", kind="ink", name_size=22)
    s.arrow([(1120, 665), (1166, 665)])
    s.model(1170, 620, 340, 90, "agent", '"you tried hanging it higher"')

    line1(s, "Filed is not remembered.")
    s.save("c4-two-policies.svg")


# ── c22 · when memory is read and written ───────────────────────────────────
def c22_timeline():
    s = Svg(); s.icon("desk")
    s.title("When it is read, when it is written")

    cols = [(300, "an ask"), (720, "🌙 closing time"), (1140, "a month later · an ask")]
    s.p.append(f'<path d="M300 250 L1500 250" stroke="{TAN}" stroke-width="2.5" marker-end="url(#a)"/>')
    for i, (x, head) in enumerate(cols):
        s.step(x + 16, 250, i + 1)
        s.text(x + 44, 258, head, size=21, fill=INK, weight=800)

    def lane(y, name, col):
        s.p.append(f'<rect x="90" y="{y}" width="1420" height="140" rx="18" fill="{FRAME}" fill-opacity="0.55" stroke="{BOUND}" stroke-width="1.5"/>')
        s.text(116, y + 78, name, size=18, fill=col, mono=True, weight=800)

    def cell(x, y, kind, text):
        if kind == "-":
            s.text(x + 170, y + 40, "—", size=24, fill=TAN, anchor="middle"); return
        col, bg = (GREEND, GREENBG) if kind == "write" else (PURPLED, PURPLEBG)
        s.p.append(f'<rect x="{x}" y="{y}" width="340" height="64" rx="16" fill="{bg}" stroke="{col}" stroke-width="2.5"/>')
        s.text(x + 170, y + 40, text, size=19, fill=col, mono=True, anchor="middle", weight=700)

    lane(300, "STATE", AMBERD)
    cell(300, 338, "write", "write the slip · EDIT 1")
    cell(720, 338, "-", "")
    cell(1140, 338, "read", "read the drawer · EDIT 2")
    lane(480, "MEMORY", PURPLED)
    cell(300, 518, "read", "search · EDIT 3")
    cell(720, 518, "write", "file the whole day")
    cell(1140, 518, "read", "search · EDIT 3")

    s.text(300, 690, "green = a write", size=16, fill=GREEND, weight=700)
    s.text(480, 690, "purple = a read", size=16, fill=PURPLED, weight=700)
    line1(s, "State: every turn. Memory: written once at closing time, read once per question.")
    s.save("c22-timeline.svg")


# ── c23 · InMemoryMemoryService ─────────────────────────────────────────────
def c23_inmemory():
    s = Svg(); s.icon("shelf")
    s.title("InMemoryMemoryService", "a dict in this process · for prototyping")

    s.text(90, 206, "WRITE · closing time", size=15, fill=GREEND, mono=True, weight=700)
    s.panel(90, 220, 680, 56, [("await ctx.add_events_to_memory(events=ctx.session.events, …)", "#A8D5A2")], size=14.5, lh=22)
    s.arrow([(430, 276), (430, 316)], color="green")
    s.store(90, 320, 680, 260, "the day, as said", "every event, verbatim", [
        'user   · "My lantern goes out at night…"', 'agent  · "I\'ve written that down…"', 'user   · "I\'ve tried hanging it higher…"'], row_h=40, size=15)
    s.text(90, 626, "no model · nothing extracted · dies with the process", size=16, fill=TERRA)

    s.text(830, 206, "READ · every question", size=15, fill=PURPLED, mono=True, weight=700)
    s.panel(830, 220, 680, 56, [("found = await ctx.search_memory(query)", "#D9C8F0")], size=14.5, lh=22)
    s.arrow([(1170, 276), (1170, 316)], color="purple")
    s.box(830, 320, 680, 90, "count shared words", "every stored event, scored · top 10", kind="purple", name_size=24)
    s.arrow([(1170, 410), (1170, 450)], color="purple")
    s.store(830, 454, 680, 170, '"what have I already tried?"', "", [
        ('"I\'ve tried hanging it higher…"        i, tried → 2', GREEND), ('"I\'ve written that down…"              i → 1', TERRA)], row_h=36, size=14.5)
    s.text(830, 666, "her own sentences come back too", size=16, fill=SUB)

    line1(s, "Write stores the day as said. Read counts shared words.")
    s.save("c23-inmemory.svg")


# ── c24 · Memory Bank ───────────────────────────────────────────────────────
def c24_bank():
    s = Svg(); s.icon("cloud")
    s.title("Memory Bank — the same two lines", "VertexAiMemoryBankService · a Vertex AI Agent Engine")

    s.text(90, 206, "WRITE · closing time · the same file()", size=15, fill=GREEND, mono=True, weight=700)
    s.panel(90, 220, 680, 56, [("await ctx.add_events_to_memory(events=ctx.session.events, custom_metadata=FILING)", "#A8D5A2")], size=13.5, lh=22)
    s.arrow([(430, 276), (430, 316)], color="green", label="FILING: wait_for_completion · allowed_topics", lx=600, ly=302, size=13)
    s.box(90, 320, 680, 110, "memories.generate", "a model extracts facts under the topics, merges them, waits", kind="purple", name_size=24)
    s.arrow([(430, 430), (430, 470)], color="purple")
    s.store(90, 474, 680, 170, "facts", "scope (app_name, user_id)", [
        "has tried hanging the lantern higher", "does not want a replacement — a gift"], row_h=36, size=15)

    s.text(830, 206, "READ · every question · the same recall()", size=15, fill=PURPLED, mono=True, weight=700)
    s.panel(830, 220, 680, 56, [("found = await ctx.search_memory(query)", "#D9C8F0")], size=14.5, lh=22)
    s.arrow([(1170, 276), (1170, 316)], color="purple", label="by meaning", lx=1250, ly=302, size=13)
    s.box(830, 320, 680, 110, "memories.retrieve", "the facts closest to the question — no word has to match", kind="purple", name_size=24)
    s.arrow([(1170, 430), (1170, 470)], color="purple")
    s.store(830, 474, 680, 170, '"what have I already tried?"', "", [
        ("has tried hanging the lantern higher", GREEND), ("does not want a replacement — a gift", GREEND)], row_h=36, size=15)

    strip(s, 690, "no delete verb in ADK — the app calls memories.delete itself (🔥 forget me)")
    line1(s, "Same two lines. Write extracts facts; read finds them by meaning.")
    s.save("c24-bank.svg")


# ── c8 · word overlap ───────────────────────────────────────────────────────
def c8_overlap():
    s = Svg(); s.icon("shelf")
    s.title("What word overlap does to a question")

    s.box(90, 240, 400, 100, "What's the weather like today?", "nothing to do with lanterns", kind="ink", name_size=19)
    s.arrow([(490, 290), (546, 290)])
    s.box(550, 240, 280, 100, "search_memory", "shared words", kind="green", name_size=22)
    s.arrow([(830, 290), (886, 290)])
    s.store(890, 210, 620, 300, "the shelf", "every card, scored", [
        "read by the lantern at night     the, it → 2", "tried hanging it higher          it → 1",
        "it was a gift                    it → 1", ("…six more                        → 1", SUB)], row_h=38, size=15)
    s.arrow([(1200, 510), (1200, 566)])
    s.text(1216, 543, "top ten, whatever they are", size=15, fill=SUB, mono=True)
    s.panel(890, 570, 620, 90, [("THE TOWER — what it handed you:", "#B0A490"), ("  · 9 cards, none about the weather", "#F0A58A")], size=15, lh=28)
    s.arrow([(1200, 660), (1200, 706)])
    s.model(1050, 710, 300, 80, "agent", "807 tokens of nothing")

    s.text(90, 420, "Memory Bank, same question:", size=18, fill=PURPLED, weight=700)
    s.text(90, 452, "0 cards — it matches meaning, not words", size=18, fill=SUB)
    line1(s, "Recall is not free.")
    s.save("c8-overlap.svg")


# ── c5 · same slot, two homes ───────────────────────────────────────────────
def c5_two_homes():
    s = Svg(); s.icon("cloud")
    s.title("Same slot, two homes")

    s.container(90, 200, 700, 420, "the Archive · :8440", "archive/service.py")
    s.box(120, 256, 640, 90, "Runner(…, memory_service=…)", "one slot", kind="ink", name_size=22)
    s.arrow([(270, 346), (270, 406)], label="chapter 3", lx=330, ly=382, size=15)
    s.box(120, 410, 300, 170, "InMemoryMemoryService", "a dict in this process", "dies with the process", kind="tan", name_size=18)
    s.arrow([(600, 346), (600, 406)], color="purple", label="chapter 4 · .env", lx=680, ly=382, size=15)
    s.box(440, 410, 320, 170, "VertexAiMemoryBankService", "project · location", "agent_engine_id", kind="purple", name_size=18, mono_sub=True)
    s.arrow([(760, 495), (856, 495)], color="purple", label="HTTPS", ly=479, size=14)

    s.container(830, 200, 680, 420, "Google Cloud · Vertex AI Agent Engine", kind="cloud")
    s.store(860, 256, 620, 324, "Memory Bank", "scope (app_name, user_id)", [
        "generate   ← add_events_to_memory", "retrieve   ← search_memory", ("delete     ← the app, not ADK", SUB)], row_h=44, kind="purple", size=16)

    strip(s, 680, "the two lines you wrote do not change by a character")
    line1(s, "Where the archive lives is a deployment decision.")
    s.save("c5-two-homes.svg")


# ── c7 · what she actually read ─────────────────────────────────────────────
def c7_prompt():
    s = Svg(); s.icon("notepad")
    s.title("What she actually read this turn")

    s.store(90, 220, 330, 140, "session.state", "the slip", ["case: {no, item, mark, symptom}"], row_h=40, size=14)
    s.store(90, 400, 330, 140, "state[RECALLED]", "what recall() found", ["· I have tried hanging it higher"], row_h=40, size=14)
    s.arrow([(420, 290), (455, 290), (455, 350), (486, 350)], step=1, sx=455, sy=320)
    s.arrow([(420, 470), (455, 470), (455, 410), (486, 410)], step=2, sx=455, sy=440)
    s.box(490, 320, 240, 120, "house(ctx)", "builds the prompt", kind="ink", name_size=22)
    s.arrow([(730, 380), (786, 380)], step=3, sx=758, sy=380)
    s.panel(790, 220, 420, 320, [("THE SLIP —", "#B0A490"), ("  no: k7f2 · item: lantern", "#D9C8F0"), ("  mark: q7 · symptom: goes out at night", "#D9C8F0"), ("", INK),
                                 ("THE TOWER —", "#B0A490"), ("  · I have tried hanging it higher", "#A8D5A2"), ("", INK),
                                 ("(if it isn't written, say so)", "#8A8378")], size=15, lh=30)
    s.arrow([(1210, 380), (1266, 380)], step=4, sx=1238, sy=380)
    s.model(1270, 320, 240, 120, "gemini", "sees exactly this")
    s.arrow([(1390, 440), (1390, 486)], color="amber")
    s.box(1270, 490, 240, 80, "822 tokens", "usage_metadata", kind="amber", name_size=22)

    line1(s, "Nothing is in the prompt by accident.")
    s.save("c7-prompt.svg")


# ── c6 · a day goes in, facts come out ──────────────────────────────────────
def c6_distill():
    s = Svg(); s.icon("cloud")
    s.title("A day goes in. Facts come out.")

    s.store(90, 200, 360, 280, "the day", "session.events", [
        '"I read by it at night…"', '"I\'ve tried hanging it higher…"', '"I don\'t want a new one — a gift"', ('"I had soup for lunch"', SUB)], row_h=36, size=14.5)
    s.arrow([(450, 340), (516, 340)], color="green", step=1, sx=483, sy=340)
    s.box(520, 290, 250, 100, "allowed_topics", "USER_PREFERENCES", "LANTERN_CONTEXT", kind="purple", name_size=20, mono_sub=True)
    s.cross(645, 430)
    s.text(645, 466, "soup: no topic — never kept", size=14, fill=TERRA, mono=True, anchor="middle")
    s.arrow([(770, 340), (836, 340)], color="purple", step=2, sx=803, sy=340)
    s.model(840, 290, 300, 100, "extraction", "a model inside Memory Bank")
    s.arrow([(1140, 340), (1176, 340)], step=3, sx=1158, sy=340)
    s.store(1180, 200, 330, 280, "facts", "scope (app_name, user_id)", [
        "reads by the lantern at night", "has tried hanging it higher", "does not want a replacement"], row_h=36, size=14.5)

    s.box(90, 560, 360, 90, "a month later", '"Actually — I want a new one now."', kind="ink", name_size=20)
    s.arrow([(450, 605), (516, 605)], color="purple", step=4, sx=483, sy=605)
    s.model(520, 555, 300, 100, "consolidation", "revises — no twin card")
    s.arrow([(820, 605), (1176, 605)], color="purple", step=5, sx=998, sy=605)
    s.box(1180, 555, 330, 100, "the card, revised", '"has now decided to get a replacement"', kind="purple", name_size=19)

    strip(s, 700, 'ttl: "2592000s" — how long is a separate decision · forgetting is the app\'s: memories.delete')
    line1(s, "What may be kept is decided at write time, by topics.")
    s.save("c6-distill.svg")


# ── c9 · how floor four is wired ────────────────────────────────────────────
def c9_season():
    s = Svg(); s.icon("warehouse")
    s.title("How floor four is wired", "two fixed statements · the model fills in one mark")

    s.container(90, 190, 530, 630, "floor four", "archive/season/")
    s.box(120, 240, 470, 70, '"[season] a lantern that keeps dying at night"', kind="ink", name_size=15)
    s.arrow([(355, 310), (355, 346)], step=1, sx=387, sy=328)
    s.model(120, 350, 470, 90, "agent", "tools: season_search · season_known_issue")
    s.arrow([(355, 440), (355, 476)], label="where to look", lx=470, ly=464, size=14, step=2, sx=387, sy=458)
    s.box(120, 480, 470, 70, "season_search(text)", "what sounds alike", kind="green", name_size=21)
    s.arrow([(355, 550), (355, 586)], label="take the mark", lx=470, ly=574, size=14, step=5, sx=387, sy=568)
    s.box(120, 590, 470, 70, "season_known_issue(mark)", "what is connected", kind="green", name_size=21)
    s.arrow([(355, 660), (355, 706)], step=8, sx=387, sy=683)
    s.box(120, 710, 470, 70, "the answer, with the path", kind="ink", name_size=19)

    s.container(660, 190, 850, 630, "BigQuery · dataset archive", "scripts/season.sh")
    s.box(690, 240, 790, 70, "visitors · items · asks · fixes · seasons · marks", kind="tan", name_size=19)
    s.model(690, 350, 380, 70, "embedder", "gemini-embedding-001")
    s.arrow([(1070, 385), (1106, 385)], color="purple")
    s.box(1110, 350, 370, 70, "ask_embeddings", "every ask, embedded in place", kind="amber", name_size=19)
    s.box(690, 480, 380, 70, "VECTOR_SEARCH", "by meaning · top 5", kind="green", name_size=21)
    s.arrow([(1110, 515), (1074, 515)], color="amber")
    s.box(1110, 480, 370, 70, "ask_embeddings", "the vectors it searches", kind="amber", name_size=19)
    s.box(690, 590, 380, 70, "GRAPH_TABLE · MATCH", "one fixed walk", kind="green", name_size=21)
    s.arrow([(1110, 625), (1074, 625)], color="amber")
    s.box(1110, 590, 370, 70, "PROPERTY GRAPH", "over the tables · zero copy", kind="amber", name_size=19)
    s.text(1085, 740, "the model's mark → @mark · the SQL and the GQL never change", size=15, fill=SUB, anchor="middle")

    s.arrow([(590, 500), (686, 500)], color="green", label="the text", ly=486, size=13, step=3)
    s.arrow([(686, 532), (594, 532)], color="purple", dashed=True, label="5 matches · all q7", ly=556, size=13, step=4)
    s.arrow([(590, 610), (686, 610)], color="green", label="mark = q7", ly=596, size=13, step=6)
    s.arrow([(686, 642), (594, 642)], color="purple", dashed=True, label="31 rows + the fix", ly=666, size=13, step=7)
    line1(s, "Two fixed statements. The model fills in one parameter.")
    s.save("c9-season.svg")


# ── c11 · the warehouse ─────────────────────────────────────────────────────
def c11_warehouse():
    s = Svg(); s.icon("warehouse")
    s.title("One store, both shapes", "the meaning is generated next to the rows")

    s.container(90, 200, 1420, 250, "BigQuery · dataset archive")
    for i, n in enumerate(["visitors", "items", "asks", "fixes", "seasons"]):
        s.box(120 + i * 170, 262, 150, 60, n, kind="tan", name_size=19)
    s.arrow([(535, 322), (535, 362)], color="purple", label="ML.GENERATE_EMBEDDING", lx=700, ly=350, size=13)
    s.model(410, 366, 250, 64, "embedder", "")
    s.arrow([(660, 398), (716, 398)], color="purple")
    s.box(720, 366, 250, 64, "ask_embeddings", kind="amber", name_size=19)
    s.text(1010, 292, "structured — rows and keys · a join walks what was recorded", size=15, fill=INK)
    s.text(1010, 384, "unstructured — sentences as vectors · a search walks meaning", size=15, fill=PURPLED)
    s.text(1010, 408, "34 rows × 3072 numbers, beside the rows they came from", size=13.5, fill=SUB)

    s.text(90, 500, "ONCE · generate the meaning in place", size=14, fill=INK, mono=True, weight=700)
    s.panel(90, 514, 700, 130, [("CREATE MODEL archive.embedder REMOTE WITH CONNECTION `US.vertex_conn`", "#D9C8F0"),
                                ("CREATE TABLE archive.ask_embeddings AS", "#F3EDE3"),
                                ("  SELECT … FROM ML.GENERATE_EMBEDDING(MODEL archive.embedder, …)", "#A8D5A2")], size=14, lh=32)
    s.text(810, 500, "EVERY QUESTION · search by meaning", size=14, fill=PURPLED, mono=True, weight=700)
    s.panel(810, 514, 700, 130, [('VECTOR_SEARCH(TABLE archive.ask_embeddings, "embedding",', "#F3EDE3"),
                                 ('  (SELECT … "the flame keeps dying once the sun is down"), top_k => 3)', "#F2C766"),
                                 ('→ "it keeps cutting out after dark…"   0.648', "#A8D5A2")], size=14, lh=32)
    line1(s, "The meaning lives next to the rows.", "no export, no pipeline, no second database")
    s.save("c11-warehouse.svg")


# ── c12 · they were a graph already ─────────────────────────────────────────
def c12_graph():
    s = Svg(); s.icon("warehouse")
    s.title("They were a graph already")

    nodes = [(90, "Visitor", "visitors", "ink"), (470, "Item", "items", "ink"), (850, "Mark", "marks", "purple"), (1230, "Fix", "fixes", "green")]
    for x, n, k, kind in nodes:
        s.box(x, 230, 280, 110, n, k, kind=kind, name_size=28)
    for x0, lbl, tbl in [(370, "asked", "asks"), (750, "stamped", "items"), (1130, "fixed", "fixes")]:
        s.arrow([(x0, 285), (x0 + 96, 285)], color="purple", label=lbl, ly=268, size=17)
        s.text(x0 + 48, 314, tbl, size=13, fill=SUB, anchor="middle", mono=True)

    s.arrow([(990, 340), (990, 400), (230, 400), (230, 344)], dashed=True, color="amber")
    s.text(610, 390, "one MATCH, walked backwards along the arrows", size=14, fill=AMBERD, anchor="middle", mono=True, weight=700)
    s.panel(300, 430, 1000, 60, [("MATCH (m:Mark)<-[:stamped]-(i:Item)<-[a:asked]-(v:Visitor)", "#F2C766")], size=16, lh=26)
    s.text(230, 470, "31 of them", size=20, fill=INK, anchor="middle", weight=800)

    strip(s, 560, "CREATE PROPERTY GRAPH names which columns are keys and which are arrows — not one row moves")
    strip(s, 640, "marks was the one table nobody shipped: SELECT DISTINCT mark FROM items")
    line1(s, "Nobody built a graph. The keys were the arrows.")
    s.save("c12-graph.svg")


# ── c13 · the same walk, written twice ──────────────────────────────────────
def c13_gql_sql():
    s = Svg(); s.icon("warehouse")
    s.title("The same walk, written twice")

    s.text(560, 200, "GQL · one MATCH", size=18, fill=PURPLED, mono=True, anchor="middle", weight=700)
    s.text(1195, 200, "SQL · three joins", size=18, fill=AMBERD, mono=True, anchor="middle", weight=700)
    rows = [("the walk", ["MATCH (m:Mark)<-[:stamped]-(i:Item)", "      <-[a:asked]-(v:Visitor)"],
             ["FROM asks a", "JOIN items i    ON i.id = a.item_id", "JOIN visitors v ON v.id = a.visitor_id"]),
            ("maybe missing", ["OPTIONAL MATCH (m)-[:fixed]->(f:Fix)"], ["LEFT JOIN fixes f ON f.mark = i.mark"]),
            ("the parameter", ["WHERE m.mark = @mark"], ["WHERE i.mark = @mark"])]
    y = 216
    for head, g, q in rows:
        h = 34 + 28 * max(len(g), len(q))
        s.text(90, y + h / 2 + 6, head, size=15, fill=SUB, mono=True)
        s.p.append(f'<rect x="290" y="{y}" width="540" height="{h}" rx="14" fill="{PURPLEBG}" stroke="{PURPLE}" stroke-width="2.5"/>')
        s.p.append(f'<rect x="880" y="{y}" width="630" height="{h}" rx="14" fill="{AMBERBG}" stroke="{AMBER}" stroke-width="2.5"/>')
        s.text(855, y + h / 2 + 12, "=", size=34, fill=TAN, anchor="middle", weight=800)
        s.lines(314, y + 34, [(t, PURPLED) for t in g], size=16, lh=28)
        s.lines(904, y + 34, [(t, AMBERD) for t in q], size=16, lh=28)
        y += h + 16
    s.text(90, y + 60, "31", size=64, fill=INK, weight=800)
    s.text(180, y + 60, "rows either way — only one of them can be handed back as the reason", size=20, fill=INK)
    line1(s, "A distance cannot be walked again by anyone. A path can.")
    s.save("c13-gql-sql.svg")


# ── c10 · everything ────────────────────────────────────────────────────────
def c10_everything():
    s = Svg(); s.icon("desk")
    s.title("Everything you built — and what you can swap")

    s.container(90, 200, 300, 170, "the browser", "tab 3")
    s.box(120, 256, 240, 90, "site/ · :3440", "the tower, drawn", kind="ink", name_size=19)
    s.arrow([(360, 300), (436, 300)], label="SSE", ly=284, size=14)

    s.container(440, 200, 560, 430, "the Archive · :8440", "archive/service.py")
    s.box(470, 256, 500, 80, "Runner(…, session_service, memory_service)", kind="ink", name_size=17)
    s.box(470, 380, 120, 56, "route()", kind="green", name_size=18)
    s.arrow([(590, 408), (636, 408)])
    s.box(640, 380, 120, 56, "recall()", kind="green", name_size=18)
    s.arrow([(760, 408), (796, 408)])
    s.model(800, 380, 130, 56, "agent")
    s.arrow([(530, 436), (530, 490), (636, 490)])
    s.box(640, 462, 120, 56, "file()", kind="green", name_size=18)
    s.arrow([(760, 490), (796, 490)])
    s.box(800, 462, 130, 56, "goodnight()", kind="ink", name_size=15)
    s.arrow([(530, 490), (530, 572), (636, 572)])
    s.model(640, 544, 130, 56, "agent", "floor four")

    s.box(1040, 256, 470, 80, "archive.db", "SqliteSessionService", kind="amber", name_size=22)
    s.arrow([(970, 282), (1036, 282)], color="amber")
    s.container(1040, 360, 470, 120, "Vertex AI Agent Engine", kind="cloud")
    s.box(1070, 410, 410, 56, "Memory Bank", kind="purple", name_size=20)
    s.arrow([(970, 310), (1010, 310), (1010, 438), (1066, 438)], color="purple")
    s.container(1040, 510, 470, 120, "BigQuery · dataset archive")
    s.box(1070, 560, 410, 56, "ask_embeddings · season_graph", kind="amber", name_size=17)
    s.arrow([(770, 572), (1000, 572), (1000, 588), (1066, 588)], color="green")

    s.container(90, 660, 910, 120, "the workbench · adk web :8000", "tab 2")
    s.box(120, 712, 850, 56, "adk web — the same file, the same tower", kind="ink", name_size=17)
    s.arrow([(970, 740), (1018, 740), (1018, 312), (1036, 312)], color="amber", dashed=True)
    s.arrow([(970, 756), (1028, 756), (1028, 458), (1066, 458)], color="purple", dashed=True)
    s.text(1040, 700, "swap any box:", size=16, fill=GREEND, weight=800)
    s.text(1040, 726, "sqlite → Postgres · in-process → Memory Bank", size=15, fill=SUB)
    s.text(1040, 750, "the three lines you wrote do not change", size=15, fill=SUB)
    line1(s, "The UI is a client of the memory architecture, never its owner.")
    s.save("c10-everything.svg")


# ── c14 · what each floor replaced ──────────────────────────────────────────
def c14_replaced():
    s = Svg(); s.icon("desk")
    s.title("What each floor replaced")

    for x, h in [(90, "floor"), (400, "ADK 2"), (800, "what you would build instead"), (1180, "what it costs")]:
        s.text(x + 16, 206, h.upper(), size=13, fill=SUB, mono=True, weight=700)
    rows = [("the desk", "session.state + SqliteSessionService", "a dict, pickled yourself", "the model can't read it"),
            ("floor two", "the user: prefix", "a users table, a join per turn", "key placement, forever"),
            ("floor three", "add_events_to_memory + search_memory", "a cron dump + the model deciding", "nothing distills"),
            ("the tower", "Memory Bank + allowed_topics", "vector store + extraction + consolidation", "three services to run"),
            ("floor four", "VECTOR_SEARCH + one GQL MATCH", "export, embed, a graph DB, a sync", "the data leaves")]
    y = 222
    for f, a, b, c in rows:
        s.p.append(f'<rect x="90" y="{y}" width="1420" height="96" rx="16" fill="#FFFFFF" stroke="{TAN}" stroke-width="2"/>')
        s.text(106, y + 56, f, size=20, fill=INK, weight=800)
        s.p.append(f'<rect x="400" y="{y + 14}" width="380" height="68" rx="12" fill="{GREENBG}"/>')
        s.text(416, y + 56, a, size=15, fill=GREEND, mono=True, weight=700)
        s.text(816, y + 56, b, size=16, fill=INK)
        s.text(1196, y + 56, c, size=16, fill=TERRA)
        y += 108
    line1(s, "Not that the right column is impossible — that it is yours forever.")
    s.save("c14-replaced.svg")


# ── c15 · three questions ───────────────────────────────────────────────────
def c15_three_questions():
    s = Svg(); s.icon("jar")
    s.title("Three questions. Stop at the first yes.")

    rows = [(1, "Will it still matter tomorrow?", "NO →", "keep nothing", "tan"),
            (2, "Can a function check it?", "YES →", "the drawer — a verifiable fact", "amber"),
            (3, "Otherwise.", "→", "the tower — an unverifiable preference", "purple")]
    y = 220
    for n, q, yes, land, tone in rows:
        stroke, col, subcol, fill = KIND[tone]
        s.p.append(f'<rect x="90" y="{y}" width="1420" height="130" rx="20" fill="#FFFFFF" stroke="{TAN}" stroke-width="2.5"/>')
        s.step(130, y + 65, n)
        s.text(170, y + 75, q, size=30, fill=INK, weight=800)
        s.text(866, y + 73, yes, size=20, fill=col if tone != "tan" else SUB, mono=True, anchor="middle", weight=700)
        s.p.append(f'<rect x="930" y="{y + 24}" width="556" height="82" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>')
        s.text(1208, y + 74, land, size=20, fill=col if tone != "tan" else INK, mono=True, anchor="middle", weight=700)
        y += 150
    strip(s, 700, "a record is not a memory — a record plus two decisions: what to keep, and when to look")
    line1(s, "Facts and preferences belong in different stores.")
    s.save("c15-three-questions.svg")


# ── c16 · what RAG is ───────────────────────────────────────────────────────
def c16_rag():
    s = Svg(); s.icon("warehouse")
    s.title("What RAG is", "the model never saw your data — fetch the rows that matter, put them in the prompt")

    s.box(80, 290, 350, 100, '"a lantern that keeps dying at night"', "the question", kind="ink", name_size=14)
    s.arrow([(430, 340), (456, 340)])
    s.container(460, 220, 440, 300, "1 · RETRIEVE")
    s.store(490, 274, 170, 200, "your data", "in BigQuery", ["asks", "items", "fixes"], row_h=28, size=14)
    s.arrow([(660, 374), (706, 374)], color="amber")
    s.box(710, 320, 160, 100, "top-k rows", kind="amber", name_size=20)
    s.arrow([(900, 340), (946, 340)], color="amber")
    s.text(950, 250, "2 · AUGMENT", size=15, fill=HEAD, mono=True, weight=700)
    s.panel(950, 264, 300, 190, [("THE SEASON —", "#B0A490"), ("· goes out an hour after…", "#A8D5A2"), ("· keeps cutting out after…", "#A8D5A2"),
                                 ("· …3 more", "#A8D5A2"), ("", INK), ("the question", "#F2C766")], size=14.5, lh=26)
    s.arrow([(1250, 340), (1296, 340)], color="purple")
    s.text(1300, 250, "3 · GENERATE", size=15, fill=HEAD, mono=True, weight=700)
    s.model(1300, 264, 210, 90, "model")
    s.arrow([(1405, 354), (1405, 396)], color="purple")
    s.box(1300, 400, 210, 90, "the answer", "grounded in rows", kind="ink", name_size=20)

    strip(s, 600, "two ways to choose the rows — by MEANING (what sounds alike) · by CONNECTION (what is attached)")
    s.text(90, 700, "floor three was already this shape: recall() fetched cards, then the model answered", size=17, fill=SUB)
    line1(s, "RAG is a prompt with evidence in it.")
    s.save("c16-rag.svg")


# ── c19 · retrieval by meaning ──────────────────────────────────────────────
def c19_meaning():
    import math, random
    s = Svg(); s.icon("warehouse")
    s.title("Retrieval by meaning", "every sentence becomes a point — the nearest points win")

    s.text(90, 206, "ONCE", size=15, fill=HEAD, mono=True, weight=700)
    s.store(90, 220, 340, 200, "asks.said", "34 sentences", ['"it goes out an hour after…"', '"mine dies when the wind…"'], row_h=34, size=14)
    s.arrow([(260, 420), (260, 466)], color="purple")
    s.model(90, 470, 340, 70, "embedder", "3072 numbers each")
    s.arrow([(260, 540), (260, 586)], color="purple")
    s.box(90, 590, 340, 64, "ask_embeddings", "a point beside every row", kind="amber", name_size=19)
    s.arrow([(430, 622), (466, 622)], color="amber")

    s.p.append(f'<rect x="470" y="220" width="560" height="434" rx="20" fill="#FFFFFF" stroke="{TAN}" stroke-width="2.5"/>')
    qx, qy = 750, 440
    near = [(715, 420), (785, 415), (730, 476), (777, 472), (705, 460)]
    rng = random.Random(7); far = []
    while len(far) < 26:
        a, r = rng.uniform(0, 2 * math.pi), rng.uniform(78, 135)
        x, y = qx + r * math.cos(a), qy + r * math.sin(a)
        if (500 < x < 1000 and 250 < y < 620) and all(math.hypot(x - fx, y - fy) > 16 for fx, fy in far):
            far.append((round(x), round(y)))
    for x, y in far:
        s.p.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{PURPLE}" fill-opacity="0.55"/>')
    s.p.append(f'<circle cx="{qx}" cy="{qy}" r="62" fill="{AMBERBG}" fill-opacity="0.6" stroke="{AMBER}" stroke-width="2" stroke-dasharray="7 5"/>')
    for x, y in near:
        s.p.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{PURPLE}"/>')
    s.p.append(f'<circle cx="{qx}" cy="{qy}" r="9" fill="{AMBER}" stroke="#FFFFFF" stroke-width="2.5"/>')
    s.text(820, 436, "the question", size=13, fill=AMBERD, mono=True, weight=700)
    s.text(820, 454, "the 5 nearest", size=13, fill=AMBERD, mono=True, weight=700)
    s.text(750, 636, "3072 dimensions, drawn as two", size=13, fill=SUB, anchor="middle")

    s.text(1070, 206, "EVERY QUESTION", size=15, fill=HEAD, mono=True, weight=700)
    s.box(1070, 220, 440, 70, '"a lantern that keeps dying at night"', kind="ink", name_size=15)
    s.arrow([(1290, 290), (1290, 326)], color="purple")
    s.model(1070, 330, 440, 60, "embedder", "the same space")
    s.arrow([(1070, 360), (1034, 360)], color="amber")
    s.arrow([(1290, 390), (1290, 426)], color="purple")
    s.store(1070, 430, 440, 224, "VECTOR_SEARCH · top 5", "how near", [
        "goes out an hour after…    0.648", "keeps cutting out after…   0.671", "the flame sits low…        0.690"], row_h=32, size=14)

    strip(s, 700, "not one word in common — near in meaning, not in spelling · but a distance is not a link")
    line1(s, "By meaning: the nearest points win.")
    s.save("c19-meaning.svg")


# ── c20 · five tables, one graph ────────────────────────────────────────────
def c20_tables():
    s = Svg(); s.icon("warehouse")
    s.title("Five tables — and how they connect", "a row that is a thing → a node · a row that points at two rows → an edge")

    def tbl(x, y, w, name, cols):
        h = 40 + len(cols) * 24 + 10
        s.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#FFFFFF" stroke="{TAN}" stroke-width="2.5"/>')
        s.p.append(f'<path d="M{x} {y + 40} L{x + w} {y + 40}" stroke="{TAN}" stroke-width="2"/>')
        s.text(x + 16, y + 27, name, size=16, fill=INK, mono=True, weight=700)
        for i, (c, kind) in enumerate(cols):
            col = {"key": INK, "fk": PURPLED, "col": SUB, "keyfk": PURPLED}[kind]
            lab = {"key": c + "  · key", "fk": c + "  →", "col": c, "keyfk": c + "  · key →"}[kind]
            s.text(x + 16, y + 40 + (i + 1) * 24 - 6, lab, size=13.5, fill=col, mono=True, weight=700 if kind != "col" else None)

    s.text(90, 206, "THE TABLES", size=14, fill=HEAD, mono=True, weight=700)
    tbl(90, 236, 180, "visitors", [("id", "key"), ("name", "col")])
    tbl(330, 214, 220, "asks", [("id", "key"), ("visitor_id", "fk"), ("item_id", "fk"), ("said", "col")])
    tbl(610, 236, 180, "items", [("id", "key"), ("kind", "col"), ("mark", "fk")])
    tbl(610, 430, 180, "marks", [("mark", "key")])
    tbl(330, 430, 220, "fixes", [("mark", "keyfk"), ("what", "col")])

    def link(a, b, la, lb, pa, pb):
        s.p.append(f'<path d="M{a[0]} {a[1]} L{b[0]} {b[1]}" stroke="{PURPLE}" stroke-width="2.5" fill="none"/>')
        s.text(pa[0], pa[1], la, size=13, fill=PURPLED, mono=True, weight=700, anchor="middle")
        s.text(pb[0], pb[1], lb, size=13, fill=PURPLED, mono=True, weight=700, anchor="middle")
    link((270, 289), (330, 297), "1", "n", (282, 280), (320, 314))
    link((550, 315), (610, 289), "n", "1", (560, 332), (600, 280))
    link((700, 358), (700, 430), "n", "1", (716, 376), (716, 424))
    link((550, 483), (610, 483), "0..1", "1", (566, 504), (600, 474))
    s.text(90, 580, "visitors ↔ items: many-to-many, through asks", size=16, fill=INK)
    s.text(90, 608, "items → marks: many-to-one · 31 items are stamped q7", size=16, fill=INK)
    s.text(90, 636, "marks → fixes: one, or none", size=16, fill=INK)

    s.text(870, 206, "THE SAME THING, AS A GRAPH", size=14, fill=HEAD, mono=True, weight=700)
    s.box(870, 250, 150, 70, "Visitor", "visitors", kind="ink", name_size=19)
    s.arrow([(1020, 285), (1076, 285)], color="purple", label="asked", ly=270, size=14)
    s.text(1048, 312, "asks", size=12, fill=SUB, mono=True, anchor="middle")
    s.box(1080, 250, 150, 70, "Item", "items", kind="ink", name_size=19)
    s.arrow([(1230, 285), (1286, 285)], color="purple", label="stamped", ly=270, size=14)
    s.text(1258, 312, "items", size=12, fill=SUB, mono=True, anchor="middle")
    s.box(1290, 250, 150, 70, "Mark", "marks", kind="purple", name_size=19)
    s.arrow([(1365, 320), (1365, 396)], color="green", label="fixed", lx=1400, ly=362, size=14)
    s.box(1290, 400, 150, 70, "Fix", "fixes", kind="green", name_size=19)
    s.text(870, 380, "asks points at a visitor and an item → an edge", size=15, fill=SUB)
    s.text(870, 404, "items points at itself and a mark → node and edge", size=15, fill=SUB)

    s.text(870, 540, "TWO REAL ROWS", size=14, fill=HEAD, mono=True, weight=700)
    for name, y in [("Rusty", 590), ("Pip", 650)]:
        s.p.append(f'<circle cx="898" cy="{y}" r="22" fill="#FFFFFF" stroke="{INK}" stroke-width="2.5"/>')
        s.text(898, y + 4, name, size=11, fill=INK, mono=True, anchor="middle", weight=700)
        s.arrow([(920, y), (976, y)])
        s.p.append(f'<rect x="980" y="{y - 14}" width="100" height="28" rx="9" fill="#FFFFFF" stroke="{TAN}" stroke-width="2"/>')
        s.text(1030, y + 4, "lantern", size=11, fill=INK, mono=True, anchor="middle")
    s.arrow([(1080, 590), (1162, 612)], color="purple")
    s.arrow([(1080, 650), (1162, 628)], color="purple")
    s.p.append(f'<circle cx="1190" cy="620" r="30" fill="{PURPLE}"/>')
    s.text(1190, 626, "q7", size=16, fill="#FFFFFF", mono=True, anchor="middle", weight=700)
    s.arrow([(1220, 620), (1296, 620)], color="green")
    s.box(1300, 590, 210, 60, "the fix", kind="green", name_size=17)

    line1(s, "A thing is a node. A row that points at two rows is an edge.")
    s.save("c20-tables.svg")


# ── c21 · what a MATCH does ─────────────────────────────────────────────────
def c21_match():
    import math
    s = Svg(); s.icon("warehouse")
    s.title("What a MATCH does", "draw a shape, pin one key — every place it fits is one row")

    s.text(90, 206, "THE SHAPE", size=14, fill=HEAD, mono=True, weight=700)
    s.p.append(f'<circle cx="150" cy="300" r="34" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>')
    s.text(150, 305, "Visitor", size=12, fill=INK, mono=True, anchor="middle", weight=700)
    s.arrow([(184, 300), (276, 300)], color="purple", label="asked", ly=288, size=12)
    s.box(280, 276, 100, 48, "Item", kind="ink", name_size=15)
    s.arrow([(380, 300), (462, 300)], color="purple", label="stamped", ly=288, size=12)
    s.p.append(f'<circle cx="500" cy="300" r="40" fill="none" stroke="{AMBER}" stroke-width="2.5" stroke-dasharray="6 4"/>')
    s.p.append(f'<circle cx="500" cy="300" r="34" fill="{PURPLE}"/>')
    s.text(500, 297, "Mark", size=12, fill="#FFFFFF", mono=True, anchor="middle", weight=700)
    s.text(500, 315, "= q7", size=13, fill="#F2C766", mono=True, anchor="middle", weight=700)
    s.text(556, 304, "← the key you pin", size=12, fill=AMBERD, mono=True)
    s.arrow([(500, 342), (500, 396)], color="green", dashed=True)
    s.text(514, 374, "fixed · optional", size=11, fill=GREEND, mono=True)
    s.box(450, 400, 100, 48, "Fix", kind="green", name_size=15)
    s.panel(90, 480, 470, 120, [("MATCH (m:Mark)<-[:stamped]-(i:Item)", "#F2C766"), ("      <-[a:asked]-(v:Visitor)", "#F2C766"),
                                ("WHERE m.mark = @mark", "#F3EDE3"), ("OPTIONAL MATCH (m)-[:fixed]->(f:Fix)", "#A8D5A2")], size=13.5, lh=24)
    s.text(90, 640, "read it right to left — the walk runs against the arrows", size=15, fill=SUB)

    s.text(600, 206, "EVERY PLACE IT FITS", size=14, fill=HEAD, mono=True, weight=700)
    hx, hy, hr = 930, 390, 30
    for name, y in [("Rusty", 262), ("Clover", 326), ("Pip", 390), ("Tansy", 454), ("Wick", 518)]:
        s.p.append(f'<rect x="636" y="{y - 22}" width="216" height="44" rx="12" fill="{AMBERBG}" fill-opacity="0.7" stroke="{AMBER}" stroke-width="1.5" stroke-dasharray="5 4"/>')
        s.p.append(f'<circle cx="660" cy="{y}" r="18" fill="#FFFFFF" stroke="{INK}" stroke-width="2.5"/>')
        s.text(660, y + 4, name, size=9.5, fill=INK, mono=True, anchor="middle", weight=700)
        s.arrow([(678, y), (756, y)])
        s.p.append(f'<rect x="760" y="{y - 13}" width="80" height="26" rx="8" fill="#FFFFFF" stroke="{TAN}" stroke-width="2"/>')
        s.text(800, y + 4, "lantern", size=11, fill=INK, mono=True, anchor="middle")
        dx, dy = hx - 840, hy - y; d = math.hypot(dx, dy)
        s.arrow([(840, y), (round(hx - dx / d * (hr + 4)), round(hy - dy / d * (hr + 4)))], color="purple")
    s.p.append(f'<circle cx="{hx}" cy="{hy}" r="{hr}" fill="{PURPLE}"/>')
    s.text(hx, hy + 6, "q7", size=16, fill="#FFFFFF", mono=True, anchor="middle", weight=700)
    s.text(744, 566, "…26 more", size=12, fill=SUB, mono=True, anchor="middle")
    s.text(1000, 400, "fits: 31", size=20, fill=AMBERD, mono=True, weight=800)
    s.arrow([(951, 369), (990, 292)], color="green")
    s.box(990, 246, 66, 42, "Fix", kind="green", name_size=14)
    y = 640
    s.p.append(f'<circle cx="660" cy="{y}" r="18" fill="#FFFFFF" stroke="{TAN}" stroke-width="2.5"/>')
    s.arrow([(678, y), (756, y)])
    s.p.append(f'<rect x="760" y="{y - 13}" width="80" height="26" rx="8" fill="#FFFFFF" stroke="{TAN}" stroke-width="2"/>')
    s.text(800, y + 4, "kettle", size=11, fill=SUB, mono=True, anchor="middle")
    s.arrow([(840, y), (908, y)])
    s.p.append(f'<circle cx="930" cy="{y}" r="18" fill="#FFFFFF" stroke="{TAN}" stroke-width="2.5"/>')
    s.text(930, y + 4, "b2", size=11, fill=SUB, mono=True, anchor="middle", weight=700)
    s.cross(974, y, r=10)
    s.text(992, y + 4, "no fit", size=11, fill=TERRA, mono=True)

    s.text(1100, 206, "ONE ROW PER FIT", size=14, fill=HEAD, mono=True, weight=700)
    s.store(1100, 220, 410, 260, "31 rows", "who · said · fix", [
        "Rusty   goes out an hour after…", "Clover  mine dies when the wind…", ("…29 more", SUB), ("every row: the fix", GREEND)], row_h=30, size=13)
    s.text(1100, 526, "OPTIONAL MATCH = LEFT JOIN, in graph", size=14, fill=PURPLED, mono=True, weight=700)
    s.text(1100, 552, "each row is a chain of keys: v → i → q7 → fix", size=14, fill=SUB)
    line1(s, "Draw the shape once. Every fit is a row — and the path comes free.")
    s.save("c21-match.svg")


# ── c18 · what graph RAG is ─────────────────────────────────────────────────
def c18_graph_rag():
    s = Svg(); s.icon("warehouse")
    s.title("What graph RAG is", "the same three steps — only the retriever walks a graph")

    s.text(90, 216, "VECTOR RAG · by meaning", size=15, fill=PURPLED, mono=True, weight=700)
    s.box(90, 236, 250, 70, "the question", kind="ink", name_size=17)
    s.arrow([(340, 271), (376, 271)])
    s.model(380, 236, 150, 70, "embed")
    s.arrow([(530, 271), (566, 271)], color="purple")
    s.box(570, 236, 190, 70, "5 nearest rows", kind="amber", name_size=16)
    s.arrow([(760, 271), (796, 271)], color="amber")
    s.panel(800, 220, 310, 102, [("prompt:", "#B0A490"), ("· 5 sentences that", "#F3EDE3"), ("  resemble the question", "#F3EDE3")], size=14, lh=24)
    s.arrow([(1110, 271), (1146, 271)], color="purple")
    s.model(1150, 236, 150, 70, "model")
    s.arrow([(1300, 271), (1336, 271)], color="purple")
    s.box(1340, 236, 170, 70, "answer", "from lookalikes", kind="ink", name_size=17)
    s.text(90, 352, "five sentences that sound alike — no link between them, no cause", size=15, fill=SUB)
    s.p.append(f'<path d="M90 384 L1510 384" stroke="{TAN}" stroke-width="2" stroke-dasharray="8 6"/>')

    s.text(90, 424, "GRAPH RAG · by connection", size=15, fill=GREEND, mono=True, weight=700)
    s.box(90, 444, 250, 70, "the question", kind="ink", name_size=17)
    s.arrow([(340, 479), (376, 479)])
    s.box(380, 444, 150, 70, "a key", "mark q7", kind="purple", name_size=16)
    s.arrow([(530, 479), (566, 479)], color="purple")
    s.box(570, 444, 190, 70, "MATCH · walk", "31 rows + the fix", kind="green", name_size=16)
    s.arrow([(760, 479), (796, 479)], color="green")
    s.panel(800, 416, 310, 126, [("prompt:", "#B0A490"), ("· 31 visits · 10 things said", "#A8D5A2"), ("· the fix, and who found it", "#A8D5A2"), ("· path: q7 → 31 → 10 → fix", "#F2C766")], size=14, lh=24)
    s.arrow([(1110, 479), (1146, 479)], color="purple")
    s.model(1150, 444, 150, 70, "model")
    s.arrow([(1300, 479), (1336, 479)], color="purple")
    s.box(1340, 444, 170, 70, "answer", "with the path", kind="ink", name_size=17)
    s.text(90, 572, "everything attached to one key — the rows and the edges between them; the path is the citation", size=15, fill=SUB)

    strip(s, 660, "in this lab: vector search finds the mark (where to look) → one MATCH walks from it (what is attached)")
    line1(s, "Graph RAG = RAG whose retriever walks edges.")
    s.save("c18-graph-rag.svg")


# ── c25 · graph RAG, the whole process in the lab ───────────────────────────
def c25_graph_rag_process():
    import math
    s = Svg(); s.icon("warehouse")
    s.title("Graph RAG, in the lab", "one question · two retrievals · one answer that carries its path")

    def node(cx, cy, r, name, sub="", kind="ink", dim=False):
        stroke = {"ink": INK, "purple": PURPLE, "green": GREEN, "amber": AMBER, "tan": TAN}[kind]
        fill = {"ink": "#FFFFFF", "purple": PURPLE, "green": "#FFFFFF", "amber": AMBERBG, "tan": "#FFFFFF"}[kind]
        if dim:
            stroke, fill = TAN, "#FFFFFF"
        s.p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')
        col = "#FFFFFF" if kind == "purple" and not dim else (TAN if dim else INK)
        subcol = "#EDE9F7" if kind == "purple" and not dim else (TAN if dim else SUB)
        s.text(cx, cy + (4 if not sub else -2), name, size=13 if r <= 32 else 14, fill=col, mono=True, anchor="middle", weight=700)
        if sub:
            s.text(cx, cy + 16, sub, size=11, fill=subcol, mono=True, anchor="middle")

    def edge(a, b, ra, rb, color="tan", label="", dashed=False, bold=False):
        dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy)
        p1 = (round(a[0] + dx / d * ra), round(a[1] + dy / d * ra))
        p2 = (round(b[0] - dx / d * (rb + 4)), round(b[1] - dy / d * (rb + 4)))
        s.arrow([p1, p2], color=color, dashed=dashed, label=label, ly=(p1[1] + p2[1]) / 2 - 8, size=12)
        if bold:
            col = {"amber": AMBER, "green": GREEN, "purple": PURPLE, "tan": TAN}[color]
            s.p.append(f'<path d="M{p1[0]} {p1[1]} L{p2[0]} {p2[1]}" stroke="{col}" stroke-width="7" stroke-opacity="0.35" fill="none"/>')

    # ── top row · the question, embedded, searched ───────────────────────
    s.box(90, 246, 300, 96, '"a lantern that keeps', '  dying at night"', kind="ink", name_size=15, mono_sub=True)
    s.text(240, 362, "the question", size=13, fill=SUB, anchor="middle")
    s.arrow([(390, 294), (436, 294)])

    s.container(440, 180, 790, 190, "1 · SEMANTIC SEARCH", "VECTOR_SEARCH · top 5")
    s.model(470, 246, 210, 96, "embedder", "gemini-embedding-001")
    s.arrow([(680, 294), (716, 294)], color="purple")
    s.box(720, 246, 220, 96, "[0.1, 0.8, −0.2 …]", "3,072 numbers", kind="purple", name_size=15)
    s.arrow([(940, 294), (976, 294)], color="purple")
    s.box(980, 246, 220, 96, "5 nearest asks", "every one · mark q7", kind="amber", name_size=17)

    # ── bottom left · the graph, walked ──────────────────────────────────
    s.container(90, 400, 900, 400, "2 · GRAPH TRAVERSAL")
    # the hand-off into the graph — after the container, so its translucent fill does not wash the pill
    s.arrow([(1090, 342), (1090, 384), (620, 384), (620, 420)], color="purple", dashed=True)
    s.p.append(f'<rect x="684" y="424" width="150" height="30" rx="15" fill="{PURPLED}"/>')
    s.text(759, 444, "semantic match", size=12, fill="#FFFFFF", mono=True, anchor="middle", weight=700)

    M = (620, 480)
    items = [(470, 596), (620, 596), (770, 596)]
    visitors = [(470, 712, "Rusty"), (620, 712, "Pip"), (770, 712, "Clover")]
    # a part of the graph the walk never touches
    node(230, 480, 34, "b2", "mark", dim=True)
    node(230, 596, 30, "kettle", "", dim=True)
    node(230, 712, 30, "Someone", "", dim=True)
    edge((230, 596), (230, 480), 30, 34, color="tan")
    edge((230, 712), (230, 596), 30, 30, color="tan")
    s.text(230, 764, "not q7 · not walked", size=11, fill=TAN, mono=True, anchor="middle")
    # the walk
    for it in items:
        node(it[0], it[1], 32, "lantern")
        edge(it, M, 32, 44, color="amber", bold=True)
    for vx, vy, nm in visitors:
        node(vx, vy, 32, nm)
        edge((vx, vy), (vx, 596), 32, 32, color="amber", bold=True)
    s.text(548, 560, "stamped", size=11, fill=AMBERD, mono=True, anchor="end")
    s.text(596, 658, "asked", size=11, fill=AMBERD, mono=True, anchor="end")
    s.p.append(f'<circle cx="{M[0]}" cy="{M[1]}" r="52" fill="none" stroke="{AMBER}" stroke-width="2.5" stroke-dasharray="7 5"/>')
    node(M[0], M[1], 44, "q7", "mark", kind="purple")
    s.box(818, 450, 164, 60, "the fix", "wicks too shallow", kind="green", name_size=14)
    edge(M, (818, 480), 44, 0, color="green", label="fixed")
    s.text(880, 716, "…31 items", size=13, fill=AMBERD, mono=True, anchor="middle", weight=700)
    s.text(880, 736, "31 visitors", size=13, fill=AMBERD, mono=True, anchor="middle", weight=700)
    s.text(340, 782, "MATCH (m:Mark)<-[:stamped]-(i:Item)<-[a:asked]-(v:Visitor)  ·  the model filled in q7", size=12, fill=SUB, mono=True)

    # ── right · what the model read, what it said ────────────────────────
    s.arrow([(990, 596), (1076, 596)], color="green", label="rows + path", lx=1033, ly=580, size=12)
    s.text(1080, 404, "LLM CONTEXT", size=14, fill=HEAD, mono=True, weight=700)
    s.panel(1080, 416, 430, 250, [("THE SEASON — what the", "#B0A490"), ("warehouse handed you:", "#B0A490"),
                                  ("mark q7 · 31 visits", "#F2C766"), ("10 different things said", "#D9C8F0"),
                                  ("fix: wicks dipped too", "#A8D5A2"), ("     shallow · day 62", "#A8D5A2"),
                                  ("path: q7 → 31 → 10 → fix", "#F2C766")], size=15, lh=28)
    s.arrow([(1295, 666), (1295, 702)], color="purple")
    s.box(1080, 706, 430, 84, "Thirty-one had this: wicks dipped too shallow.", "the last line is the path · q7 → 31 → 10 → fix", kind="ink", name_size=14)

    line1(s, "Similar finds where to look. Connected finds what is attached — and the path is the citation.")
    s.save("c25-graph-rag-process.svg")


if __name__ == "__main__":
    for w in ACTS:
        tower(w)
    for fn in (c1_slip, c2_one_file, c3_drawers, c4_two_policies, c5_two_homes, c6_distill, c7_prompt, c8_overlap,
               c9_season, c10_everything, c11_warehouse, c12_graph, c13_gql_sql, c14_replaced, c15_three_questions,
               c16_rag, c18_graph_rag, c19_meaning, c20_tables, c21_match, c22_timeline, c23_inmemory, c24_bank, c25_graph_rag_process):
        fn(); print("  ·", fn.__name__)
