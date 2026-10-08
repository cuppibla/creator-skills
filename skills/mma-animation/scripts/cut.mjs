#!/usr/bin/env node
/* ============================================================
   MMA clip cutter — slice an EXISTING video into b-roll clips.
   For videos that carry no scene metadata (e.g. Claude Design
   exports). Skill-generated animations don't need this: their
   clips are cut automatically at scene boundaries by render.mjs.

   node cut.mjs <video.mp4> --at 0:10,0:21,1:07 [options]
     --at <list>      cut points (M:SS, H:MM:SS or seconds),
                      comma-separated. N points → N+1 clips.
     --out <dir>      output dir (default: <video dir>/clips)
     --names <list>   comma-separated slugs → NN-slug.mp4
                      (default: plain NN.mp4)
     --crf <n>        x264 quality (default 15)
   Writes <out>/manifest.md with the clip ↔ time-range table.
   ============================================================ */
import { spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';

const argv = process.argv.slice(2);
const video = path.resolve(argv.find(a => !a.startsWith('--')) || '');
if (!existsSync(video)) { console.error(`No such file: ${video}`); process.exit(1); }
const opt = (n, d) => { const i = argv.indexOf(`--${n}`); return i >= 0 ? argv[i + 1] : d; };

const toSec = s => s.trim().split(':').reduce((acc, p) => acc * 60 + parseFloat(p), 0);
const fmt = t => `${Math.floor(t / 60)}:${(t % 60).toFixed(1).padStart(4, '0')}`;

const atArg = opt('at', null);
if (!atArg) { console.error('Missing --at 0:10,0:21,…'); process.exit(1); }
const cuts = atArg.split(',').map(toSec).sort((a, b) => a - b);

const probe = spawnSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', video]);
const total = parseFloat(probe.stdout.toString());
const CRF = opt('crf', '15');
const outDir = path.resolve(opt('out', path.join(path.dirname(video), 'clips')));
const names = opt('names', '').split(',').filter(Boolean);
mkdirSync(outDir, { recursive: true });

const bounds = [0, ...cuts, total];
const rows = [];
for (let i = 0; i < bounds.length - 1; i++) {
  const [a, b] = [bounds[i], bounds[i + 1]];
  const slug = names[i] ? `-${names[i]}` : '';
  const name = `${String(i + 1).padStart(2, '0')}${slug}.mp4`;
  const dest = path.join(outDir, name);
  if (existsSync(dest)) { console.error(`REFUSING to overwrite existing ${dest} — move it or pass a different --out`); process.exit(1); }
  const r = spawnSync('ffmpeg', ['-y', '-i', video, '-ss', a.toFixed(3), '-t', (b - a).toFixed(3),
    '-c:v', 'libx264', '-preset', 'medium', '-crf', CRF, '-pix_fmt', 'yuv420p',
    '-movflags', '+faststart', '-an', dest], { stdio: ['ignore', 'ignore', 'pipe'] });
  if (r.status !== 0) { console.error(`FAILED ${name}\n${r.stderr}`); process.exit(1); }
  console.log(`clip: ${path.relative(process.cwd(), dest)}  (${fmt(a)} → ${fmt(b)}, ${(b - a).toFixed(1)}s)`);
  rows.push(`| ${name} | ${fmt(a)} – ${fmt(b)} | ${(b - a).toFixed(1)}s |  |`);
}

writeFileSync(path.join(outDir, 'manifest.md'),
  `# Clips — ${path.basename(video)}\n\n| clip | range | dur | script lines |\n|---|---|---|---|\n${rows.join('\n')}\n`);
console.log(`manifest: ${path.join(outDir, 'manifest.md')}`);
