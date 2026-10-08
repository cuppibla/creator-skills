// Helper library for Google Brand decks.
// Usage: require this AFTER creating `pres = new pptxgen()` and pass `pres` into createHelpers().
//
//   const pptxgen = require("pptxgenjs");
//   const { C, FONT, MONO, SW, SH, ML, MR } = require("./theme.js");
//   const pres = new pptxgen();
//   pres.layout = "LAYOUT_WIDE";
//   const H = require("./helpers.js")(pres, { C, FONT, MONO, SW, SH, ML, MR });
//
// Then use H.addGlass(slide, {...}), H.addGoogleBar(slide, y), etc.

module.exports = function createHelpers(pres, theme) {
  const { C, FONT, MONO, SW, SH, ML, MR } = theme;

  // ---------- Google four-color top bar ----------
  // Pass `width` to center it (used on title slides). Default spans the content area.
  function addGoogleBar(slide, y = 0.42, width) {
    const w = width || (SW - ML - MR);
    const x = width ? (SW - width) / 2 : ML;
    const each = w / 4, h = 0.07;
    slide.addShape(pres.shapes.RECTANGLE, { x,                y, w: each, h, fill: { color: C.blue   }, line: { type: "none" } });
    slide.addShape(pres.shapes.RECTANGLE, { x: x + each,      y, w: each, h, fill: { color: C.red    }, line: { type: "none" } });
    slide.addShape(pres.shapes.RECTANGLE, { x: x + each * 2,  y, w: each, h, fill: { color: C.yellow }, line: { type: "none" } });
    slide.addShape(pres.shapes.RECTANGLE, { x: x + each * 3,  y, w: each, h, fill: { color: C.green  }, line: { type: "none" } });
  }

  // ---------- Section tag (small uppercase, letter-spaced) ----------
  function addSectionTag(slide, text, x, y, color = C.blue) {
    slide.addText(text, {
      x, y, w: 8, h: 0.3,
      fontFace: FONT, fontSize: 11, bold: true, color, charSpacing: 4, margin: 0,
    });
  }

  // ---------- Slide number (bottom-right) ----------
  function addSlideNum(slide, num, color = C.g600) {
    slide.addText(num, {
      x: SW - 1.2, y: SH - 0.45, w: 1.0, h: 0.3,
      fontFace: FONT, fontSize: 10, color, align: "right", margin: 0,
    });
  }

  // ---------- Standard slide header (used on most content slides) ----------
  // Adds: google bar at top, section tag, h2 title, optional caption.
  function addSlideHeader(slide, sectionTag, title, caption, tagColor = C.blue) {
    slide.background = { color: C.white };
    addGoogleBar(slide, 0.42);
    addSectionTag(slide, sectionTag, ML, 0.7, tagColor);
    slide.addText(title, {
      x: ML, y: 1.0, w: SW - ML - MR, h: 0.75,
      fontFace: FONT, fontSize: 30, bold: true, color: C.g800, margin: 0,
    });
    if (caption) {
      slide.addText(caption, {
        x: ML, y: 1.75, w: SW - ML - MR, h: 0.4,
        fontFace: FONT, fontSize: 15, color: C.g600, margin: 0,
      });
    }
  }

  // ---------- "Glass" tinted card ----------
  // tint: 'blue' | 'green' | 'yellow' | 'red' | 'plain' | 'gray'
  // PPTX has no backdrop-filter; this is the closest faithful interpretation.
  function addGlass(slide, opts) {
    const { x, y, w, h, tint = "blue" } = opts;
    const tints = {
      plain:  { fill: "FFFFFF", border: "E8EAED", trans: 0 },
      gray:   { fill: "F8F9FA", border: "E8EAED", trans: 0 },
      blue:   { fill: "4285F4", border: "4285F4", trans: 92 }, // 8% tint
      green:  { fill: "34A853", border: "34A853", trans: 92 },
      yellow: { fill: "FBBC04", border: "FBBC04", trans: 92 },
      red:    { fill: "EA4335", border: "EA4335", trans: 92 },
    };
    const t = tints[tint] || tints.blue;
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x, y, w, h,
      fill: { color: t.fill, transparency: t.trans },
      line: { color: t.border, width: 0.75, transparency: 75 },
      rectRadius: 0.12,
      shadow: { type: "outer", color: "000000", blur: 8, offset: 1, angle: 90, opacity: 0.05 },
    });
  }

  // ---------- Code block (dark rounded rect + syntax-colored monospace runs) ----------
  // `lines` is a 2D array. Each line is an array of segments. Each segment is { t: "text", c?: hex, size?: pt }.
  // Use the C.kw / C.str / C.cm / C.fn / C.op palette for syntax colors.
  function addCodeBlock(slide, x, y, w, h, lines) {
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x, y, w, h,
      fill: { color: C.codeBg }, line: { type: "none" },
      rectRadius: 0.1,
    });
    const runs = [];
    lines.forEach((line, lineIdx) => {
      line.forEach((seg, segIdx) => {
        const isEOL = segIdx === line.length - 1 && lineIdx !== lines.length - 1;
        runs.push({
          text: seg.t,
          options: {
            fontFace: MONO,
            fontSize: seg.size || 11,
            color: seg.c || C.codeFg,
            breakLine: isEOL,
          },
        });
      });
    });
    slide.addText(runs, {
      x: x + 0.18, y: y + 0.15, w: w - 0.36, h: h - 0.3,
      valign: "top", margin: 0, paraSpaceAfter: 0,
    });
  }

  // ---------- Pill (rounded label) ----------
  function addPill(slide, x, y, w, text, bg, fg, fontSize = 11) {
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x, y, w, h: 0.32,
      fill: { color: bg }, line: { type: "none" },
      rectRadius: 0.16,
    });
    slide.addText(text, {
      x, y, w, h: 0.32,
      fontFace: FONT, fontSize, bold: true, color: fg, align: "center", valign: "middle", margin: 0,
    });
  }

  // ---------- Bullet list with colored dots ----------
  // items: [{ dot?: hex, text: string | richTextRuns[] }]
  function addBulletList(slide, items, x, y, w, h, opts = {}) {
    const fontSize = opts.fontSize || 13;
    const lineH = opts.lineH || 0.34;
    const defaultDot = opts.defaultDot || C.blue;
    items.forEach((item, i) => {
      const cy = y + i * lineH;
      slide.addShape(pres.shapes.OVAL, {
        x: x, y: cy + 0.12, w: 0.13, h: 0.13,
        fill: { color: item.dot || defaultDot },
        line: { type: "none" },
      });
      const runs = Array.isArray(item.text)
        ? item.text
        : [{ text: item.text, options: { fontFace: FONT, fontSize, color: C.g800 } }];
      slide.addText(runs, {
        x: x + 0.25, y: cy, w: w - 0.25, h: lineH,
        valign: "middle", margin: 0,
      });
    });
  }

  // ---------- Quote (italic with colored left accent bar) ----------
  function addQuote(slide, text, x, y, w, h = 0.85, accent = C.blue) {
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 0.06, h,
      fill: { color: accent }, line: { type: "none" },
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: x + 0.06, y, w: w - 0.06, h,
      fill: { color: C.g50 }, line: { type: "none" },
    });
    slide.addText(text, {
      x: x + 0.3, y, w: w - 0.45, h,
      fontFace: FONT, fontSize: 14, italic: true, color: C.g800, valign: "middle", margin: 0,
    });
  }

  // ---------- Section divider (full-bleed colored slide) ----------
  // opts: { tag, line1, line2, subtitle, slideNum, bgColor, bgColorDk, tagColor? }
  function addSectionDividerCustom(slide, opts) {
    const { tag, line1, line2, subtitle, slideNum, bgColor, bgColorDk, tagColor = C.tagOnBlue } = opts;
    slide.background = { color: bgColor };
    // Subtle two-tone via darker overlay on the right
    slide.addShape(pres.shapes.RECTANGLE, {
      x: SW * 0.5, y: 0, w: SW * 0.5, h: SH,
      fill: { color: bgColorDk, transparency: 50 }, line: { type: "none" },
    });
    addSectionTag(slide, tag, ML, 2.3, tagColor);
    slide.addText([
      { text: line1, options: { breakLine: true } },
      { text: line2 },
    ], {
      x: ML, y: 2.7, w: SW - ML - MR, h: 2.0,
      fontFace: FONT, fontSize: 40, bold: true, color: C.white, margin: 0,
    });
    if (subtitle) {
      slide.addText(subtitle, {
        x: ML, y: 5.1, w: SW - ML - MR, h: 0.5,
        fontFace: FONT, fontSize: 19, color: C.white, margin: 0,
      });
    }
    addSlideNum(slide, slideNum, tagColor);
  }

  // ---------- Flow step (single labeled glass card in a vertical chain) ----------
  function addFlowStep(slide, opts) {
    const { x, y, w, h = 0.62, tint = "blue", number, label, sublabel } = opts;
    addGlass(slide, { x, y, w, h, tint });
    const runs = [
      ...(number ? [{ text: number + " ", options: { fontFace: FONT, fontSize: 14, bold: true, color: C.g800 } }] : []),
      { text: label, options: { fontFace: FONT, fontSize: 13, color: C.g800 } },
    ];
    if (sublabel) {
      runs.push({ text: "  " + sublabel, options: { fontFace: FONT, fontSize: 12, color: C.g600 } });
    }
    slide.addText(runs, {
      x: x + 0.2, y, w: w - 0.4, h,
      align: "center", valign: "middle", margin: 0,
    });
  }

  // ---------- Flow connector (small vertical line between flow steps) ----------
  function addFlowConnector(slide, x, y, height = 0.18, color) {
    slide.addShape(pres.shapes.RECTANGLE, {
      x: x - 0.01, y, w: 0.02, h: height,
      fill: { color: color || C.g600 },
      line: { type: "none" },
    });
  }

  // ---------- Horizontal arrow (right-pointing, with shaft + triangular arrowhead) ----------
  // Useful for flow diagrams. Place a text label above using a separate addText call.
  function addArrowRight(slide, x, y, len = 0.8, color = C.g600) {
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y: y + 0.06, w: len - 0.1, h: 0.025,
      fill: { color }, line: { type: "none" },
    });
    slide.addShape(pres.shapes.RIGHT_TRIANGLE, {
      x: x + len - 0.15, y: y - 0.02, w: 0.18, h: 0.2,
      fill: { color }, line: { type: "none" },
      rotate: 90,
    });
  }

  // ---------- "Live Demo" style badge (rounded pill with colored dot + text) ----------
  function addBadge(slide, x, y, w, h, text, color) {
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x, y, w, h,
      fill: { color, transparency: 88 },
      line: { type: "none" },
      rectRadius: 0.17,
    });
    slide.addShape(pres.shapes.OVAL, {
      x: x + 0.15, y: y + h/2 - 0.07, w: 0.14, h: 0.14,
      fill: { color }, line: { type: "none" },
    });
    slide.addText(text, {
      x: x + 0.35, y, w: w - 0.4, h,
      fontFace: FONT, fontSize: 11, bold: true, color, charSpacing: 2,
      align: "left", valign: "middle", margin: 0,
    });
  }

  return {
    addGoogleBar, addSectionTag, addSlideNum, addSlideHeader,
    addGlass, addCodeBlock, addPill, addBulletList, addQuote,
    addSectionDividerCustom, addFlowStep, addFlowConnector,
    addArrowRight, addBadge,
  };
};
