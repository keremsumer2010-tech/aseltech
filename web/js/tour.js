// Guided tour (spotlight walkthrough) shared by the atlas and the simulator.
// The page dims, one element stays lit, a card next to it explains it; Next / Back / Skip.
// Usage: GuidedTour.start(steps, {key: 'atlas'})   steps: [{el: '#id' | null, title, text}]
//        GuidedTour.auto(steps, {key})              starts only on the first visit (localStorage)
// Steps whose element is missing or hidden are skipped; el: null shows a centred card.
(function () {
  if (window.GuidedTour) return;

  const CSS = `
.gt-block{position:fixed;inset:0;z-index:10000;background:transparent}
.gt-hole{position:fixed;z-index:10001;pointer-events:none;border-radius:10px;
  box-shadow:0 0 0 200vmax rgba(6,12,24,.74);outline:2px solid rgba(255,255,255,.9);outline-offset:2px;
  transition:top .28s ease,left .28s ease,width .28s ease,height .28s ease}
.gt-hole.gt-none{outline:0;width:0!important;height:0!important;top:50%!important;left:50%!important}
.gt-tip{position:fixed;z-index:10002;width:min(340px,calc(100vw - 24px));background:#fff;color:#14202e;
  border-radius:12px;box-shadow:0 18px 50px rgba(0,0,0,.35);padding:16px 18px 14px;
  font:14px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;transition:top .28s ease,left .28s ease}
.gt-tip h3{margin:0 0 6px;font-size:16px;line-height:1.3;color:#0b3d91}
.gt-tip p{margin:0 0 12px}
.gt-row{display:flex;align-items:center;gap:8px}
.gt-count{font-size:12px;color:#5b6778;margin-right:auto}
.gt-tip button{font:inherit;font-size:13px;border-radius:8px;padding:6px 12px;cursor:pointer;border:1px solid #c9d2de;background:#fff;color:#14202e}
.gt-tip button.gt-next{background:#0b3d91;border-color:#0b3d91;color:#fff;font-weight:600}
.gt-tip button.gt-skip{border:0;background:none;color:#5b6778;padding:6px 4px;text-decoration:underline}
.gt-tip button:focus-visible{outline:2px solid #0b3d91;outline-offset:2px}
.gt-dots{display:flex;gap:4px;margin:0 0 10px}
.gt-dots i{width:6px;height:6px;border-radius:50%;background:#c9d2de}
.gt-dots i.on{background:#0b3d91}
@media (prefers-reduced-motion:reduce){.gt-hole,.gt-tip{transition:none}}`;

  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode: tour just shows again */ } }
  };

  function find(step) {
    if (!step.el) return null;
    const el = typeof step.el === 'function' ? step.el() : document.querySelector(step.el);
    if (!el || el.closest('[hidden]')) return null;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0 ? el : null;
  }

  let active = null;

  function start(allSteps, opts) {
    opts = opts || {};
    if (active) active.end(false);
    const steps = allSteps.filter(s => !s.el || find(s));
    if (!steps.length) return;

    if (!document.getElementById('gt-style')) {
      const st = document.createElement('style');
      st.id = 'gt-style';
      st.textContent = CSS;
      document.head.appendChild(st);
    }
    const block = document.createElement('div'); block.className = 'gt-block';
    const hole = document.createElement('div'); hole.className = 'gt-hole';
    const tip = document.createElement('div'); tip.className = 'gt-tip';
    tip.setAttribute('role', 'dialog'); tip.setAttribute('aria-modal', 'true'); tip.setAttribute('aria-live', 'polite');
    document.body.append(block, hole, tip);

    let i = 0, raf = 0;
    const prevFocus = document.activeElement;

    function place() {
      const step = steps[i];
      const el = find(step);
      const vw = window.innerWidth, vh = window.innerHeight, pad = 6, gap = 12, m = 12;
      const tw = tip.offsetWidth, th = tip.offsetHeight;
      const rr = el && el.getBoundingClientRect();
      const onScreen = rr && rr.bottom > 0 && rr.top < vh && rr.right > 0 && rr.left < vw;
      if (!el || !onScreen) { // nothing to light (or still scrolling to it): centred card
        hole.classList.add('gt-none');
        tip.style.left = Math.max(m, (vw - tw) / 2) + 'px';
        tip.style.top = Math.max(m, (vh - th) / 2) + 'px';
        return;
      }
      hole.classList.remove('gt-none');
      const r = el.getBoundingClientRect();
      const top = Math.max(r.top - pad, 4), left = Math.max(r.left - pad, 4);
      const bottom = Math.min(r.bottom + pad, vh - 4), right = Math.min(r.right + pad, vw - 4);
      Object.assign(hole.style, {top: top + 'px', left: left + 'px', width: (right - left) + 'px', height: (bottom - top) + 'px'});
      // Card: below, above, right, left of the lit area; otherwise pinned to the bottom of the screen.
      const cx = Math.min(Math.max(m, (left + right) / 2 - tw / 2), vw - tw - m);
      const cy = Math.min(Math.max(m, (top + bottom) / 2 - th / 2), vh - th - m);
      let x, y;
      if (vh - bottom >= th + gap + m) { x = cx; y = bottom + gap; }
      else if (top >= th + gap + m) { x = cx; y = top - gap - th; }
      else if (vw - right >= tw + gap + m) { x = right + gap; y = cy; }
      else if (left >= tw + gap + m) { x = left - gap - tw; y = cy; }
      else { x = (vw - tw) / 2; y = vh - th - m; }
      tip.style.left = Math.max(m, x) + 'px';
      tip.style.top = Math.max(m, y) + 'px';
    }

    function schedule() { cancelAnimationFrame(raf); raf = requestAnimationFrame(place); }

    function render() {
      const step = steps[i], last = i === steps.length - 1;
      tip.innerHTML = '';
      const dots = document.createElement('div'); dots.className = 'gt-dots';
      steps.forEach((_, k) => { const d = document.createElement('i'); if (k <= i) d.className = 'on'; dots.appendChild(d); });
      const h = document.createElement('h3'); h.textContent = step.title;
      const p = document.createElement('p'); p.innerHTML = step.text;
      const row = document.createElement('div'); row.className = 'gt-row';
      const count = document.createElement('span'); count.className = 'gt-count'; count.textContent = `${i + 1} / ${steps.length}`;
      const skip = button('Skip tour', 'gt-skip', () => end(true));
      const back = button('Back', 'gt-back', () => go(i - 1));
      const next = button(last ? 'Done' : 'Next', 'gt-next', () => (last ? end(true) : go(i + 1)));
      row.append(count);
      if (!last) row.append(skip);
      if (i > 0) row.append(back);
      row.append(next);
      tip.append(dots, h, p, row);
      const el = find(step);
      if (el) {
        const r = el.getBoundingClientRect();
        if (r.top < 60 || r.bottom > window.innerHeight - 40) {
          // Tall areas (e.g. a long list) scroll to their start, clear of a fixed site header.
          const tall = r.height > window.innerHeight * 0.7;
          const prev = el.style.scrollMarginTop;
          if (tall) el.style.scrollMarginTop = '80px';
          el.scrollIntoView({block: tall ? 'start' : 'center', behavior: 'smooth'});
          el.style.scrollMarginTop = prev;
        }
      }
      place();
      setTimeout(place, 350); // after smooth scroll settles
      next.focus({preventScroll: true});
    }

    function button(label, cls, fn) {
      const b = document.createElement('button');
      b.type = 'button'; b.className = cls; b.textContent = label;
      b.addEventListener('click', fn);
      return b;
    }

    function go(n) { if (n >= 0 && n < steps.length) { i = n; render(); } }

    // Capture phase on window: every key stops here while the tour is open, so page shortcuts
    // (Space / N / R in the simulator) cannot change anything underneath the tour.
    function onKey(e) {
      const k = e.key;
      e.stopImmediatePropagation();
      if ((k === 'Enter' || k === ' ') && tip.contains(e.target)) return; // native click on the focused card button
      if (k === 'Escape') end(true);
      else if (k === 'ArrowRight' || k === 'Enter') { if (i === steps.length - 1) end(true); else go(i + 1); }
      else if (k === 'ArrowLeft') go(i - 1);
      else if (k === 'Tab') { // keep focus inside the card
        const bs = [...tip.querySelectorAll('button')];
        const at = bs.indexOf(document.activeElement);
        (bs[(at + (e.shiftKey ? bs.length - 1 : 1)) % bs.length] || bs[0]).focus();
      } else if (k !== ' ' && !k.startsWith('Arrow') && k !== 'PageDown' && k !== 'PageUp') return;
      e.preventDefault();
    }

    function end(remember) {
      cancelAnimationFrame(raf);
      window.removeEventListener('keydown', onKey, true);
      window.removeEventListener('resize', schedule);
      window.removeEventListener('scroll', schedule, true);
      block.remove(); hole.remove(); tip.remove();
      if (remember && opts.key) store.set('gt-done-' + opts.key, '1');
      active = null;
      if (prevFocus && prevFocus.focus) prevFocus.focus({preventScroll: true});
      if (opts.onEnd) opts.onEnd();
    }

    window.addEventListener('keydown', onKey, true);
    window.addEventListener('resize', schedule);
    window.addEventListener('scroll', schedule, true);
    active = {end};
    render();
  }

  function auto(steps, opts) {
    if (opts && opts.key && store.get('gt-done-' + opts.key)) return;
    start(steps, opts);
  }

  window.GuidedTour = {start, auto, isActive: () => !!active};
})();
