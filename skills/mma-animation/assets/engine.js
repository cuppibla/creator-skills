/* ============================================================
   MMA timeline engine — deterministic, seekable.
   Everything on screen is a pure function of time t (seconds).

   Authoring contract (see style-guide.md):
   - <section class="scene" data-id="hook" data-dur="8"> … scenes play
     in document order; engine fades them in/out (0.35s) at boundaries.
   - Any element with data-at="1.2" enters at t=1.2s *relative to its
     scene*, using data-fx="rise|fade|pop|drop|slide-l|slide-r"
     (default rise) over data-fx-dur seconds (default 0.55).
   - A container with data-stagger="0.12" auto-cues its direct
     children starting at its own data-at, 0.12s apart.
   - data-loop="pulse|float" gets --lp (sawtooth 0..1) and --ls
     (sine −1..1) driven from absolute t; data-freq in Hz (default 0.55).
   - .wave elements are auto-filled with data-bars bars (default 28);
     bar heights are a deterministic function of (bar index, t).
   - .flow[data-step-times="a,b,c,d"] marks child .step elements
     .is-active in sequence at those scene-relative times (the last
     entry keeps the final step active until scene end).

   Renderer API: window.__mma = { duration, seek(t), scenes }
   Preview: opened without ?render → scrub bar, space = play/pause,
   ←/→ = ±1s (shift = ±1 frame), r = restart.
   ============================================================ */
(function () {
  const XFADE = 0.35;
  const RENDER = new URLSearchParams(location.search).has('render');
  if (RENDER) document.body.classList.add('render');

  // ---------- easing ----------
  const easeOutCubic = u => 1 - Math.pow(1 - u, 3);
  const easeOutBack = u => { const c = 1.70158; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
  const clamp01 = u => Math.max(0, Math.min(1, u));

  // ---------- collect scenes ----------
  const sceneEls = Array.from(document.querySelectorAll('.scene'));
  let acc = 0;
  const scenes = sceneEls.map(el => {
    const dur = parseFloat(el.dataset.dur || '6');
    const s = { el, id: el.dataset.id || `scene${acc}`, start: acc, dur };
    acc += dur;
    return s;
  });
  const DURATION = acc;

  // ---------- expand staggers into data-at ----------
  document.querySelectorAll('[data-stagger]').forEach(box => {
    const step = parseFloat(box.dataset.stagger);
    let t = parseFloat(box.dataset.at || '0');
    Array.from(box.children).forEach(child => {
      if (!child.dataset.at) child.dataset.at = String(t);
      if (!child.dataset.fx) child.dataset.fx = box.dataset.fx || 'rise';
      t += step;
    });
    // container itself just holds layout — make it always-visible
    delete box.dataset.at;
    if (box.dataset.fx) delete box.dataset.fx;
  });

  // ---------- build waveform bars ----------
  document.querySelectorAll('.wave').forEach(w => {
    const n = parseInt(w.dataset.bars || '28', 10);
    for (let i = 0; i < n; i++) w.appendChild(document.createElement('i'));
  });

  // ---------- per-scene element index ----------
  scenes.forEach(s => {
    s.cues = Array.from(s.el.querySelectorAll('[data-at]')).map(el => ({
      el,
      at: parseFloat(el.dataset.at),
      dur: parseFloat(el.dataset.fxDur || '0.55'),
      fx: el.dataset.fx || 'rise',
    }));
    s.loops = Array.from(s.el.querySelectorAll('[data-loop]'));
    s.waves = Array.from(s.el.querySelectorAll('.wave'));
    s.flows = Array.from(s.el.querySelectorAll('[data-step-times]')).map(f => ({
      el: f,
      times: f.dataset.stepTimes.split(',').map(Number),
      steps: Array.from(f.querySelectorAll('.step')),
    }));
  });

  // ---------- seek ----------
  function seek(t) {
    t = Math.max(0, Math.min(DURATION, t));
    for (const s of scenes) {
      const tl = t - s.start; // scene-local time
      const live = tl >= -0.0001 && tl < s.dur;
      s.el.classList.toggle('is-live', live);
      if (!live) { s.el.style.opacity = 0; continue; }

      // scene fade in/out
      const fadeIn = s.start === 0 ? 1 : clamp01(tl / XFADE);
      const fadeOut = s.start + s.dur >= DURATION - 0.001 ? 1 : clamp01((s.dur - tl) / XFADE);
      s.el.style.opacity = Math.min(fadeIn, fadeOut);

      // element cues
      for (const c of s.cues) {
        const u = clamp01((tl - c.at) / c.dur);
        const on = u > 0;
        c.el.classList.toggle('is-in', on);
        if (on) {
          const p = c.fx === 'pop' ? easeOutBack(u) : easeOutCubic(u);
          c.el.style.setProperty('--p', p.toFixed(4));
        }
      }

      // loops (absolute t → deterministic phase)
      for (const el of s.loops) {
        const f = parseFloat(el.dataset.freq || '0.55');
        el.style.setProperty('--lp', ((t * f) % 1).toFixed(4));
        el.style.setProperty('--ls', Math.sin(t * f * 2 * Math.PI).toFixed(4));
      }

      // waveform: deterministic pseudo-noise per (bar, t)
      for (const w of s.waves) {
        const bars = w.children;
        const speed = parseFloat(w.dataset.speed || '1');
        for (let i = 0; i < bars.length; i++) {
          const h = 0.5
            + 0.32 * Math.sin(i * 1.7 + t * 5.1 * speed)
            + 0.18 * Math.sin(i * 3.1 - t * 7.7 * speed + 1.3);
          bars[i].style.setProperty('--h', clamp01(h).toFixed(3));
        }
      }

      // step highlight
      for (const f of s.flows) {
        let active = -1;
        f.times.forEach((ft, i) => { if (tl >= ft) active = i; });
        f.steps.forEach((st, i) => st.classList.toggle('is-active', i === active));
      }
    }
  }

  window.__mma = {
    duration: DURATION,
    seek,
    scenes: scenes.map(s => ({ id: s.id, start: s.start, dur: s.dur, script: s.el.dataset.script || '' })),
  };

  seek(0);
  if (RENDER) return;

  // ---------- preview HUD ----------
  const hud = document.createElement('div');
  hud.id = 'mma-hud';
  hud.innerHTML = `<button id="mma-play">▶</button>
    <input type="range" min="0" max="${DURATION}" step="0.0333" value="0">
    <span id="mma-time">0.00 / ${DURATION.toFixed(2)}s</span>`;
  document.body.appendChild(hud);
  const range = hud.querySelector('input');
  const btn = hud.querySelector('#mma-play');
  const timeEl = hud.querySelector('#mma-time');

  let playing = false, t0 = 0, wall0 = 0, cur = 0;
  function show(t) {
    cur = Math.max(0, Math.min(DURATION, t));
    seek(cur);
    range.value = cur;
    timeEl.textContent = `${cur.toFixed(2)} / ${DURATION.toFixed(2)}s`;
  }
  function tick(now) {
    if (!playing) return;
    const t = t0 + (now - wall0) / 1000;
    if (t >= DURATION) { playing = false; btn.textContent = '▶'; show(DURATION); return; }
    show(t);
    requestAnimationFrame(tick);
  }
  function toggle() {
    playing = !playing;
    btn.textContent = playing ? '❚❚' : '▶';
    if (playing) {
      t0 = cur >= DURATION - 0.02 ? 0 : cur;
      wall0 = performance.now();
      requestAnimationFrame(tick);
    }
  }
  btn.addEventListener('click', toggle);
  range.addEventListener('input', () => { playing = false; btn.textContent = '▶'; show(parseFloat(range.value)); });
  document.addEventListener('keydown', e => {
    if (e.code === 'Space') { e.preventDefault(); toggle(); }
    if (e.code === 'ArrowRight') show(cur + (e.shiftKey ? 1 / 30 : 1));
    if (e.code === 'ArrowLeft') show(cur - (e.shiftKey ? 1 / 30 : 1));
    if (e.key === 'r') { playing = false; btn.textContent = '▶'; show(0); }
  });
})();
