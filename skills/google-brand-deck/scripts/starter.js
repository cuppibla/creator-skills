// Starter template — copy theme.js and helpers.js next to this file, then extend.
//
// Workflow:
//   1. Edit `outFile` below to your deck's name
//   2. Add each slide as its own block at the bottom
//   3. Run: NODE_PATH=$(npm root -g) node build.js
//   4. Convert to PDF for QA: soffice --headless --convert-to pdf output.pptx
//   5. Inspect with: pdftoppm -jpeg -r 90 output.pdf slide
//   6. Fix issues, repeat

const pptxgen = require("pptxgenjs");
const { C, FONT, MONO, SW, SH, ML, MR } = require("./theme.js");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title  = "TITLE_HERE";
pres.author = "Annie";

const H = require("./helpers.js")(pres, { C, FONT, MONO, SW, SH, ML, MR });

const outFile = "/home/claude/output.pptx";

// ============================================================
// SLIDE 1 — Title (example)
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: "F0F4FF" };
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: SW, h: SH,
    fill: { color: "FFFFFF", transparency: 40 }, line: { type: "none" },
  });

  H.addGoogleBar(s, 1.5, 3.5);

  s.addText("Your Deck Title", {
    x: ML, y: 2.0, w: SW - ML - MR, h: 1.0,
    fontFace: FONT, fontSize: 50, bold: true, color: C.blueDk,
    align: "center", margin: 0,
  });

  s.addText("Optional subtitle that explains what this deck covers", {
    x: ML, y: 3.4, w: SW - ML - MR, h: 0.8,
    fontFace: FONT, fontSize: 22, color: C.g600,
    align: "center", margin: 0,
  });

  // Pills
  const pillY = 5.0;
  const pillW = 1.4, pillGap = 0.2;
  const totalW = 4 * pillW + 3 * pillGap;
  const startX = (SW - totalW) / 2;
  const pills = [
    { text: "Tag One",   bg: C.pillBlue,   fg: C.blue },
    { text: "Tag Two",   bg: C.pillGreen,  fg: C.green },
    { text: "Tag Three", bg: C.pillRed,    fg: C.red },
    { text: "Tag Four",  bg: C.pillYellow, fg: C.yellowDk },
  ];
  pills.forEach((p, i) => {
    H.addPill(s, startX + i * (pillW + pillGap), pillY, pillW, p.text, p.bg, p.fg, 12);
  });

  H.addSlideNum(s, "0");
}

// ============================================================
// SLIDE 2 — Section divider (example)
// ============================================================
{
  const s = pres.addSlide();
  H.addSectionDividerCustom(s, {
    tag: "SECTION 1 · 0:00 – 10:00",
    line1: "Section Title —",
    line2: "Subtitle on Second Line",
    subtitle: "Optional one-line description below",
    slideNum: "S1",
    bgColor: C.blue,
    bgColorDk: C.blueDk,
    tagColor: C.tagOnBlue,
  });
}

// ============================================================
// SLIDE 3 — Content slide with 2x2 glass grid (example)
// ============================================================
{
  const s = pres.addSlide();
  H.addSlideHeader(s, "SECTION 1 · TOPIC", "Slide Title Here", "Optional caption that explains what this slide shows");

  const ly = 2.4;
  const colW = (SW - ML - MR - 0.3) / 2;
  const cardH = 2.1;
  const gap = 0.25;

  const cards = [
    { tint: "blue",   color: C.blue,     title: "First Concept",  body: "Description of the first concept." },
    { tint: "green",  color: C.green,    title: "Second Concept", body: "Description of the second concept." },
    { tint: "yellow", color: C.yellowDk, title: "Third Concept",  body: "Description of the third concept." },
    { tint: "red",    color: C.red,      title: "Fourth Concept", body: "Description of the fourth concept." },
  ];

  cards.forEach((c, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = ML + col * (colW + 0.3);
    const y = ly + row * (cardH + gap);
    H.addGlass(s, { x, y, w: colW, h: cardH, tint: c.tint });
    s.addText(c.title, {
      x: x + 0.3, y: y + 0.3, w: colW - 0.6, h: 0.5,
      fontFace: FONT, fontSize: 20, bold: true, color: c.color, margin: 0,
    });
    s.addText(c.body, {
      x: x + 0.3, y: y + 0.85, w: colW - 0.6, h: cardH - 1.0,
      fontFace: FONT, fontSize: 14, color: C.g800, margin: 0, valign: "top",
    });
  });

  H.addSlideNum(s, "1-A");
}

// ============================================================
// WRITE THE FILE
// ============================================================
pres.writeFile({ fileName: outFile })
  .then(name => console.log("WROTE:", name));
