#!/usr/bin/env node
/* ============================================================
   MMA renderer — HTML timeline → MP4 (master + per-scene clips).

   node render.mjs <animation.html> [options]
     --out <file.mp4>   output path        (default: <html dir>/<Name>.mp4)
     --fps <n>          frames per second  (default 30)
     --scale <n>        deviceScaleFactor  (4 → 5120×2880, 2 → 2560×1440; default 4)
     --from <s> --to <s>  render a sub-range only
     --clips            also cut per-scene clips into <out dir>/clips/NN-id.mp4
                        and write clips/manifest.md (clip ↔ script lines,
                        from each scene's data-script attribute)
     --manifest-only    just (re)write clips/manifest.md and exit — no render
     --still <s>        just save one PNG frame at time s and exit
     --crf <n>          x264 quality (default 15)
     --recycle <n>      relaunch the Chrome page every n frames (default 60) —
                        caps tab memory so long 5K renders aren't OOM-killed
     --keep-frames      keep the intermediate PNG frame dir (default: delete)

   Frames are rendered to a temp PNG dir (<out>/.frames-<Name>/) and then
   encoded in a SEPARATE ffmpeg pass — so x264's 5K working set never runs
   concurrently with headless Chrome (that concurrency is what got the render
   tab OOM-killed under machine contention). The frame dir is also a resume
   point: a killed render, re-run, skips frames already on disk.
   Requires: npm install (puppeteer-core) in this directory,
   system Google Chrome, ffmpeg on PATH.
   ============================================================ */
import puppeteer from 'puppeteer-core';
import { spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, writeFileSync, readFileSync, statSync, rmSync } from 'node:fs';
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

// ---------- cooperative render queue ----------
// Several Claude sessions can be rendering episodes on this machine at the
// same time. Full video renders are CPU/RAM-heavy at 5K, so they take a
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

// ---------- browser (relaunchable — headless Chrome can be OOM-killed under
//            machine contention; the frame loop relaunches and retries) ----------
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function launchBrowser() {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: true,
    protocolTimeout: 180000,
    args: ['--force-device-scale-factor=' + SCALE, '--hide-scrollbars', '--force-color-profile=srgb',
           '--disable-dev-shm-usage'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: SCALE });
  await page.goto('file://' + htmlPath + '?render', { waitUntil: 'networkidle0', timeout: 120000 });
  await page.evaluate(() => document.fonts.ready);
  const stage = await page.$('.stage');
  return { browser, page, stage };
}

let { browser, page, stage } = await launchBrowser();
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

// ---------- single still ----------
if (has('still')) {
  const t = parseFloat(opt('still', '0'));
  await page.evaluate(tt => window.__mma.seek(tt), t);
  const png = OUT.replace(/\.mp4$/, '') + `-${t.toFixed(2)}s.png`;
  await stage.screenshot({ path: png });
  console.log('still:', png);
  await browser.close();
  process.exit(0);
}

// ---------- frame range ----------
const from = parseFloat(opt('from', '0'));
const to = parseFloat(opt('to', String(meta.duration)));
const f0 = Math.round(from * FPS);
const f1 = Math.round(to * FPS);

// ---------- render frames to disk, then encode (decoupled from Chrome) ----------
// Rather than pipe frames into a live ffmpeg, write each frame to a temp PNG dir
// and encode afterwards. That keeps x264's 5K lookahead working set from running
// concurrently with headless Chrome — the concurrency that got the render tab
// OOM-killed under machine contention. The dir also acts as a resume point:
// already-written frames are skipped, so a killed render just re-runs to finish.
const RECYCLE = parseInt(opt('recycle', '60'), 10);
const FRAMEDIR = path.join(path.dirname(OUT), `.frames-${path.basename(OUT, '.mp4')}`);
const stampFile = path.join(FRAMEDIR, '.stamp');
const stamp = `${htmlPath}|${statSync(htmlPath).mtimeMs}|scale=${SCALE}|fps=${FPS}|${f0}-${f1}`;
if (existsSync(FRAMEDIR)) {                       // wipe stale frames if source/params changed
  let prev = null; try { prev = readFileSync(stampFile, 'utf8'); } catch {}
  if (prev !== stamp) rmSync(FRAMEDIR, { recursive: true, force: true });
}
mkdirSync(FRAMEDIR, { recursive: true });
writeFileSync(stampFile, stamp);
const framePath = f => path.join(FRAMEDIR, `f${String(f).padStart(6, '0')}.png`);

const t0 = Date.now();
let sinceFresh = 0, done = 0;
for (let f = f0; f < f1; f++) {
  const file = framePath(f);
  if (existsSync(file) && statSync(file).size > 0) { done++; continue; }   // resume: skip done frames
  if (sinceFresh >= RECYCLE) {                    // recycle the page to cap tab memory
    try { await browser.close(); } catch {}
    ({ browser, page, stage } = await launchBrowser());
    sinceFresh = 0;
  }
  // seek + screenshot, relaunching Chrome if it was OOM-killed mid-render
  for (let attempt = 0; ; attempt++) {
    try {
      await page.evaluate(tt => window.__mma.seek(tt), f / FPS);
      await stage.screenshot({ path: file });
      break;
    } catch (e) {
      if (attempt >= 8) { console.error(`\nframe ${f} failed after ${attempt} relaunches: ${e.message}`); process.exit(2); }
      process.stderr.write(`\n[frame ${f}] Chrome crash (${String(e.message).slice(0, 50)}) — relaunching\n`);
      try { await browser.close(); } catch {}
      await sleep(2000 + attempt * 1500);
      try { ({ browser, page, stage } = await launchBrowser()); }
      catch (e2) { process.stderr.write(`  relaunch failed: ${String(e2.message).slice(0, 50)}\n`); await sleep(4000); }
      sinceFresh = 0;
    }
  }
  sinceFresh++; done++;
  if (done % (FPS * 2) === 0) {
    const total = f1 - f0;
    const rate = done / ((Date.now() - t0) / 1000) || 1;
    process.stdout.write(`\r${done}/${total} frames (${(rate).toFixed(1)} fps, eta ${((total - done) / rate).toFixed(0)}s) `);
  }
}
try { await browser.close(); } catch {}
process.stdout.write('\n');

// all frames on disk (Chrome now closed) — encode in one ffmpeg pass
for (let f = f0; f < f1; f++) {
  if (!existsSync(framePath(f)) || statSync(framePath(f)).size === 0) {
    console.error(`missing frame ${f} — aborting encode`); process.exit(2);
  }
}
const enc = spawnSync('ffmpeg', [
  '-nostdin', '-y', '-framerate', String(FPS),
  '-start_number', String(f0), '-i', path.join(FRAMEDIR, 'f%06d.png'),
  '-frames:v', String(f1 - f0),                   // exact range, ignore any stale extra frames
  '-c:v', 'libx264', '-preset', 'medium', '-crf', CRF,
  '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT,
], { stdio: ['ignore', 'ignore', 'inherit'] });
if (enc.status !== 0) { console.error('ffmpeg encode failed'); process.exit(1); }
if (!has('keep-frames')) rmSync(FRAMEDIR, { recursive: true, force: true });
console.log(`master: ${OUT}`);

// ---------- per-scene clips ----------
if (has('clips')) {
  const clipDir = path.join(path.dirname(OUT), 'clips');
  mkdirSync(clipDir, { recursive: true });
  meta.scenes.forEach((s, i) => {
    const name = `${String(i + 1).padStart(2, '0')}-${s.id}.mp4`;
    // -nostdin: never let ffmpeg consume the parent's stdin (defensive — if
    // this loop is ever driven from a shell heredoc, ffmpeg would otherwise
    // swallow the remaining lines and desync the loop).
    const args = ['-nostdin', '-y', '-i', OUT, '-ss', s.start.toFixed(3), '-t', s.dur.toFixed(3),
      '-c:v', 'libx264', '-preset', 'medium', '-crf', CRF, '-pix_fmt', 'yuv420p',
      '-movflags', '+faststart', path.join(clipDir, name)];
    const r = spawnSync('ffmpeg', args, { stdio: ['ignore', 'ignore', 'pipe'] });
    console.log(r.status === 0 ? `clip:   clips/${name}` : `FAILED: ${name}\n${r.stderr}`);
  });
  writeManifest();
}
