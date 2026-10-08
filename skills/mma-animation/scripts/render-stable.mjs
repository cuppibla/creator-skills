#!/usr/bin/env node
/* ============================================================
   MMA renderer (stable variant) — same CLI as render.mjs, plus:
     · --disable-gpu software rasterization (identical output —
       content is deterministic HTML/CSS — but immune to the
       GPU-process crashes seen when other headless Chromes and
       dev servers compete for VRAM)
     · automatic Chrome relaunch + frame retry if the tab dies
       mid-render (up to 10 recoveries per run)
   Use when render.mjs hits TargetCloseError on a busy machine.
   ============================================================ */
import puppeteer from 'puppeteer-core';
import { spawn, spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, writeFileSync, rmSync, statSync } from 'node:fs';
import path from 'node:path';
import os from 'node:os';

const CHROME = [
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
].find(existsSync);
if (!CHROME) { console.error('No Chrome found'); process.exit(1); }

// ---------- args ----------
const argv = process.argv.slice(2);
const htmlPath = path.resolve(argv.find(a => !a.startsWith('--')) || '');
if (!existsSync(htmlPath)) { console.error(`No such file: ${htmlPath}`); process.exit(1); }
const opt = (name, dflt) => {
  const i = argv.indexOf(`--${name}`);
  return i >= 0 ? argv[i + 1] : dflt;
};
const has = name => argv.includes(`--${name}`);

const FPS = parseInt(opt('fps', '30'), 10);
const SCALE = parseInt(opt('scale', '4'), 10);
const CRF = opt('crf', '15');
const defaultName = path.basename(path.dirname(htmlPath)).replace(/[-_ ]+(\w)/g, (_, c) => c.toUpperCase()).replace(/^\w/, c => c.toUpperCase());
const OUT = path.resolve(opt('out', path.join(path.dirname(htmlPath), `${defaultName}.mp4`)));

// ---------- cooperative render queue (same contract as render.mjs) ----------
// slot (max 2 concurrent, atomic mkdir under ~/.mma-render-queue) and wait
// politely when busy; --still and --manifest-only are quick and skip the
// queue. A slot whose heartbeat is >5 min old is presumed dead (killed
// render) and reclaimed. IMPORTANT for agents debugging a "slow" render:
// sibling render.mjs / headless-Chrome processes belong to OTHER sessions —
// never pkill them. See mma/RENDER-COORDINATION.md. --no-queue overrides.
const QUEUE_VERSION = 1;
const QDIR = path.join(os.homedir(), '.mma-render-queue');
let mySlot = null, hbTimer = null;
function releaseSlot() {
  if (hbTimer) clearInterval(hbTimer);
  if (mySlot) { try { rmSync(mySlot, { recursive: true, force: true }); } catch {} mySlot = null; }
}
if (!has('still') && !has('manifest-only') && !has('no-queue')) {
  const MAX_SLOTS = 2, STALE_MS = 5 * 60 * 1000;
  mkdirSync(QDIR, { recursive: true });
  const tryAcquire = () => {
    for (let i = 0; i < MAX_SLOTS; i++) {
      const slot = path.join(QDIR, `slot-${i}`);
      let occupied = true;
      try { statSync(slot); } catch { occupied = false; }
      if (!occupied) {
        try { mkdirSync(slot); } catch { continue; } // lost the race — next slot
        mySlot = slot;
        const beat = () => { try { writeFileSync(path.join(slot, 'hb.json'), JSON.stringify({ pid: process.pid, out: OUT, t: Date.now() })); } catch {} };
        beat();
        hbTimer = setInterval(beat, 30_000);
        hbTimer.unref();
        return true;
      }
      // occupied — reclaim only if its heartbeat went stale (dead render)
      try {
        const hb = statSync(path.join(slot, 'hb.json'));
        if (Date.now() - hb.mtimeMs > STALE_MS) rmSync(slot, { recursive: true, force: true });
      } catch {
        try { if (Date.now() - statSync(slot).mtimeMs > STALE_MS) rmSync(slot, { recursive: true, force: true }); } catch {}
      }
    }
    return false;
  };
  let polls = 0;
  while (!tryAcquire()) {
    if (polls === 0) console.log('[queue] both render slots busy — waiting for a sibling session\'s render to finish. This is normal; do NOT kill render.mjs or headless Chrome processes (they belong to other sessions). See mma/RENDER-COORDINATION.md');
    else if (polls % 8 === 0) console.log(`[queue] still waiting (~${Math.round(polls * 17 / 60)} min)`);
    polls++;
    await new Promise(r => setTimeout(r, 15_000 + (process.pid % 7) * 1000));
  }
  console.log(`[queue] acquired ${path.basename(mySlot)} (queue v${QUEUE_VERSION}, max ${MAX_SLOTS} concurrent renders)`);
  process.on('exit', releaseSlot);
  process.on('SIGINT', () => { releaseSlot(); process.exit(130); });
  process.on('SIGTERM', () => { releaseSlot(); process.exit(143); });
}

// ---------- browser (relaunchable) ----------
let browser, page, stage;
async function launch() {
  if (browser) { try { await browser.close(); } catch {} }
  browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: true,
    args: ['--force-device-scale-factor=' + SCALE, '--hide-scrollbars',
           '--force-color-profile=srgb', '--disable-gpu', '--disable-dev-shm-usage'],
  });
  page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: SCALE });
  await page.goto('file://' + htmlPath + '?render', { waitUntil: 'networkidle0' });
  await page.evaluate(() => document.fonts.ready);
  stage = await page.$('.stage');
}
await launch();
const meta = await page.evaluate(() => ({ duration: window.__mma.duration, scenes: window.__mma.scenes }));
console.log(`timeline: ${meta.duration.toFixed(2)}s, ${meta.scenes.length} scenes ->`, meta.scenes.map(s => s.id).join(', '));

// ---------- clip manifest (clip ↔ script lines) ----------
const fmtT = t => `${Math.floor(t / 60)}:${(t % 60).toFixed(1).padStart(4, '0')}`;
function writeManifest() {
  const clipDir = path.join(path.dirname(OUT), 'clips');
  mkdirSync(clipDir, { recursive: true });
  const rows = meta.scenes.map((s, i) =>
    `| ${String(i + 1).padStart(2, '0')}-${s.id}.mp4 | ${fmtT(s.start)} – ${fmtT(s.start + s.dur)} | ${s.dur.toFixed(1)}s | ${(s.script || '⚠ missing data-script').replace(/\|/g, '/')} |`);
  writeFileSync(path.join(clipDir, 'manifest.md'),
    `# Clips — ${path.basename(OUT)}\n\n| clip | range | dur | script lines |\n|---|---|---|---|\n${rows.join('\n')}\n`);
  console.log(`manifest: ${path.join(clipDir, 'manifest.md')}`);
  const missing = meta.scenes.filter(s => !s.script);
  if (missing.length) console.warn(`⚠ scenes missing data-script: ${missing.map(s => s.id).join(', ')}`);
}

if (has('manifest-only')) {
  writeManifest();
  await browser.close();
  process.exit(0);
}

// ---------- one frame, with crash recovery ----------
let recoveries = 0;
async function grabFrame(t) {
  for (;;) {
    try {
      await page.evaluate(tt => window.__mma.seek(tt), t);
      return await stage.screenshot({ type: 'png' });
    } catch (e) {
      if (++recoveries > 10) throw e;
      console.error(`\nChrome died at t=${t.toFixed(2)}s (${e.constructor.name}) — relaunching (${recoveries}/10)`);
      await launch();
    }
  }
}

// ---------- single still ----------
if (has('still')) {
  const t = parseFloat(opt('still', '0'));
  const buf = await grabFrame(t);
  const png = OUT.replace(/\.mp4$/, '') + `-${t.toFixed(2)}s.png`;
  writeFileSync(png, buf);
  console.log('still:', png);
  await browser.close();
  process.exit(0);
}

// ---------- frame range ----------
const from = parseFloat(opt('from', '0'));
const to = parseFloat(opt('to', String(meta.duration)));
const f0 = Math.round(from * FPS);
const f1 = Math.round(to * FPS);

// ---------- ffmpeg pipe ----------
const ff = spawn('ffmpeg', [
  '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
  '-c:v', 'libx264', '-preset', 'medium', '-crf', CRF,
  '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT,
], { stdio: ['pipe', 'ignore', 'inherit'] });

const t0 = Date.now();
for (let f = f0; f < f1; f++) {
  const t = f / FPS;
  const buf = await grabFrame(t);
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  if ((f - f0) % (FPS * 2) === 0) {
    const done = f - f0, total = f1 - f0;
    const rate = done / ((Date.now() - t0) / 1000) || 1;
    process.stdout.write(`\r${done}/${total} frames (${(rate).toFixed(1)} fps, eta ${((total - done) / rate).toFixed(0)}s) `);
  }
}
ff.stdin.end();
await new Promise(r => ff.on('close', r));
await browser.close();
console.log(`\nmaster: ${OUT}`);

// ---------- per-scene clips ----------
if (has('clips')) {
  const clipDir = path.join(path.dirname(OUT), 'clips');
  mkdirSync(clipDir, { recursive: true });
  meta.scenes.forEach((s, i) => {
    const name = `${String(i + 1).padStart(2, '0')}-${s.id}.mp4`;
    const args = ['-y', '-i', OUT, '-ss', s.start.toFixed(3), '-t', s.dur.toFixed(3),
      '-c:v', 'libx264', '-preset', 'medium', '-crf', CRF, '-pix_fmt', 'yuv420p',
      '-movflags', '+faststart', path.join(clipDir, name)];
    const r = spawnSync('ffmpeg', args, { stdio: ['ignore', 'ignore', 'pipe'] });
    console.log(r.status === 0 ? `clip:   clips/${name}` : `FAILED: ${name}\n${r.stderr}`);
  });
  writeManifest();
}
