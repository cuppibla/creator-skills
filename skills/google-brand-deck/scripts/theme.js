// Google Brand palette + typography + dimensions.
// Swap this entire file to retheme (e.g. y2k-dreamcore) without touching helpers.js.

const C = {
  // Brand
  blue:    "4285F4",
  blueDk:  "1A73E8",
  red:     "EA4335",
  redDk:   "C5221F",
  yellow:  "FBBC04",
  yellowDk:"E37400",
  yellowDkD:"F29900",
  green:   "34A853",
  greenDk: "1E8E3E",

  // Grays
  g800: "3C4043",
  g600: "5F6368",
  g200: "E8EAED",
  g100: "F1F3F4",
  g50:  "F8F9FA",
  white:"FFFFFF",

  // Code block
  codeBg: "3C4043",
  codeFg: "E8EAED",
  // Syntax colors
  kw: "8AB4F8",  // keywords (def, class, return, if, for)
  str: "81C995", // strings
  cm:  "9AA0A6", // comments
  fn:  "F28B82", // function names
  op:  "FDD663", // operators / numbers

  // Pill background tints (light) by accent color
  pillBlue:   "DDE8FD",
  pillGreen:  "DCEEDE",
  pillRed:    "FAD9D6",
  pillYellow: "FDEDC8",

  // Section divider lighter accent (used for section tag inside divider slides)
  tagOnBlue:   "C3D9FB",
  tagOnGreen:  "C8E6C9",
  tagOnRed:    "FAD9D6",
  tagOnYellow: "FDEDC8",
};

const FONT = "Google Sans";     // Falls back to Roboto in Slides
const MONO = "Roboto Mono";     // Closest universal monospace; "Google Sans Mono" is rare

// Slide dimensions (LAYOUT_WIDE — 16:9)
const SW = 13.333, SH = 7.5;

// Standard margins
const ML = 0.7, MR = 0.7;

module.exports = { C, FONT, MONO, SW, SH, ML, MR };
