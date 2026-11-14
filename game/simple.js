// Valley Under Pressure, simple version: one basin, one slider, 10 years, one click per year.
// Illustrative model. The only real number is the NISAR 2026 measurement, read from summary.json:
// a normal dry summer is tuned so that it sinks the ground by NISAR's vertical estimate.
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const SITE = window.SITE || '../';
  document.querySelectorAll('[data-site]').forEach(a => { a.href = SITE + a.dataset.site; });

  /* ---------- model (all values illustrative except the NISAR target) ---------- */
  const YEARS = 10;
  const H0 = -48;          // starting groundwater level, m below the surface
  const HP0 = -56;         // lowest level the clay has "seen" before the game
  const WELL = -100;       // bottom of the farm wells, m
  const SE = 0.3;          // cm of springy (recoverable) sinking per m of water drop
  let SV = 1.625;         // cm of permanent sinking per m below the lowest-ever level (re-tuned from NISAR below)
  const PUMP = [0.6, 1, 1.5];
  const PUMP_TXT = [
    'Farms earn less, but the water can refill.',
    'Farms earn as usual. In dry years the water slowly drops.',
    'Farms earn more, but the water drops fast.'];
  const PUMP_NAME = ['Save water', 'Normal', 'Pump hard'];
  const INCOME = [80, 110, 140];                         // $ million per year at each pumping level
  const YEAR = {wet: {summer: 9, winter: 11, label: 'Wet year'}, dry: {summer: 12, winter: 5, label: 'Dry year'}};

  let S;      // game state
  let view;   // what the picture shows right now
  let nisar = null;

  function newGame(){
    S = {year: 1, type: 'dry', h: H0, hp: HP0, perm: 0, income: 0, dry: false, flags: {}};
    view = {h: H0, hp: HP0, perm: 0, total: 0, dry: false};
  }
  const total = s => s.perm + SE * (H0 - s.h);   // permanent + springy part (negative = ground lifted a little)

  function playYear(level){
    const t = YEAR[S.type], p = PUMP[level];
    const before = {perm: S.perm, h: S.h, hp: S.hp};
    // summer: pumping lowers the water; below the lowest-ever level the clay is squeezed for good
    const h1 = S.h - t.summer * p;
    const newPerm = h1 < S.hp ? SV * (S.hp - h1) : 0;
    S.perm += newPerm; S.hp = Math.min(S.hp, h1); S.h = h1;
    const dry = h1 < WELL;
    const summer = {h: S.h, hp: S.hp, perm: S.perm, total: total(S), dry};
    // winter: rain and rivers refill part of it; only the springy part of the sinking comes back
    S.h = Math.min(H0 + 4, S.h + t.winter);
    // income
    let inc = INCOME[level] * (S.type === 'dry' ? 0.9 : 1);
    if (dry) inc *= 0.6;
    inc *= 1 - Math.min(50, S.perm) / 200;               // a tilted canal delivers less water
    S.income += inc; S.dry = dry;
    return {summer, winter: {h: S.h, hp: S.hp, perm: S.perm, total: total(S), dry}, newPerm, before, dry, level, type: S.type};
  }

  /* ---------- picture ---------- */
  const NS = 'http://www.w3.org/2000/svg';
  const svg = $('scene');
  const W = 600, SURF = 72, K = 0.42;
  const shape = x => 0.3 + 0.7 * Math.exp(-(((x - 250) / 170) ** 2));    // sinking bowl, deepest under the farms
  const depthY = h => 120 + (-h - 48) * 2.05;
  const el = (tag, attrs, parent = svg) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); parent.appendChild(e); return e; };
  const txt = (x, y, s, attrs = {}) => { const e = el('text', Object.assign({x, y, 'font-size': 12, fill: '#3f4a5a'}, attrs)); e.textContent = s; return e; };

  function draw(v){
    svg.querySelectorAll(':scope > :not(title)').forEach(n => n.remove());
    const drop = Math.max(-8, Math.min(78, v.total * K));
    const permPx = Math.min(50, v.perm * K);
    const ys = x => SURF + drop * shape(x);
    const xs = []; for (let x = 0; x <= W; x += 10) xs.push(x);
    const line = f => xs.map(x => `${x},${f(x).toFixed(1)}`).join(' ');

    el('rect', {x: 0, y: 0, width: W, height: 330, fill: '#f3f5f8'});
    // underground: sand, clay (gets thinner where it is squeezed), deep sand
    const clayTop = x => 236 + permPx * shape(x);
    const yw = depthY(v.h);
    el('polygon', {points: `${line(ys)} ${W},330 0,330`, fill: '#efe6d2'});
    // groundwater: wet sand below the water table, then the clay layer on top of it
    el('rect', {x: 0, y: yw, width: W, height: 330 - yw, fill: '#d3e3f3'});
    el('polygon', {points: `${line(clayTop)} ${W},292 0,292`, fill: '#b9926a'});
    el('line', {x1: 0, x2: W, y1: yw, y2: yw, stroke: '#0b3d91', 'stroke-width': 2.2});
    // lowest level ever
    const yp = depthY(v.hp);
    el('line', {x1: 0, x2: W, y1: yp, y2: yp, stroke: '#c8321f', 'stroke-width': 1.4, 'stroke-dasharray': '6 5'});
    // starting ground level
    if (drop > 3) {
      el('line', {x1: 0, x2: W, y1: SURF, y2: SURF, stroke: '#667385', 'stroke-width': 1, 'stroke-dasharray': '3 4'});
      txt(W - 8, SURF - 6, 'Ground level at the start', {'font-size': 11, fill: '#667385', 'text-anchor': 'end'});
    }
    el('polyline', {points: line(ys), fill: 'none', stroke: '#6b5a3e', 'stroke-width': 2});

    // farm: crops + barn
    const cropC = v.dry ? '#b08a3e' : '#1f7a35';
    for (let x = 18; x < 200; x += 13) { const y = ys(x); el('path', {d: `M${x} ${y} l-3 -9 M${x} ${y} l0 -11 M${x} ${y} l3 -9`, stroke: cropC, 'stroke-width': 1.6, 'stroke-linecap': 'round', fill: 'none'}); }
    const bx = 214, by = ys(bx);
    el('rect', {x: bx, y: by - 22, width: 30, height: 22, fill: '#c8321f'});
    el('path', {d: `M${bx - 3} ${by - 22} L${bx + 15} ${by - 34} L${bx + 33} ${by - 22} Z`, fill: '#8f2416'});
    el('rect', {x: bx + 11, y: by - 11, width: 8, height: 11, fill: '#fff'});
    txt(96, ys(96) - 18, 'Farms', {'font-weight': 600, fill: '#1a1f29'});

    // well
    const wx = 330, wy = ys(wx), wb = depthY(WELL);
    el('line', {x1: wx, x2: wx, y1: wy, y2: wb, stroke: v.dry ? '#c8321f' : '#3f4a5a', 'stroke-width': 3, 'stroke-dasharray': v.dry ? '5 4' : 'none'});
    el('rect', {x: wx - 9, y: wy - 16, width: 18, height: 16, rx: 2, fill: '#3f4a5a'});
    el('path', {d: `M${wx + 9} ${wy - 11} h10 v6`, stroke: '#3f4a5a', 'stroke-width': 3, fill: 'none'});
    txt(wx - 14, wy - 22, v.dry ? 'Well (dry)' : 'Well', {'font-weight': 600, fill: v.dry ? '#c8321f' : '#1a1f29'});

    // canal: follows the ground; when one bank sinks more, the water can only fill up to the lower bank
    const c0 = 430, c1 = 510, yl = ys(c0), yr = ys(c1);
    const chan = `${c0},${yl} ${c0 + 12},${ys(c0 + 12) + 16} ${c1 - 12},${ys(c1 - 12) + 16} ${c1},${yr}`;
    el('polygon', {points: chan, fill: '#d9cfb8', stroke: '#6b5a3e', 'stroke-width': 1.5});
    const wl = Math.max(yl, yr) + 2;
    const clip = el('clipPath', {id: 'cw'}, el('defs', {}));
    el('rect', {x: c0, y: wl, width: c1 - c0, height: 60}, clip);
    el('polygon', {points: chan, fill: '#4393c3', 'clip-path': 'url(#cw)'});
    txt((c0 + c1) / 2, Math.max(yl, yr) + 34, 'Canal', {'font-weight': 600, fill: '#1a1f29', 'text-anchor': 'middle'});

    // labels underground
    txt(W - 8, yw - 6, 'Groundwater', {'text-anchor': 'end', fill: '#0b3d91', 'font-weight': 600});
    txt(W - 8, yp + 14, 'Lowest level ever', {'text-anchor': 'end', fill: '#c8321f', 'font-size': 11});
    txt(8, clayTop(8) + 18, 'Clay (squeezed clay does not spring back)', {fill: '#3b2a16', 'font-size': 11});
  }

  // animate summer (down) then winter (partly back); instant when the user prefers less motion
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function tween(a, b, ms){
    return new Promise(res => {
      if (still) { view = b; draw(view); return res(); }
      const t0 = performance.now();
      let done = false;
      const finish = () => { if (done) return; done = true; view = b; draw(view); res(); };
      const step = () => {
        if (done) return;
        const k = Math.min(1, (performance.now() - t0) / ms), e = k < .5 ? 2 * k * k : 1 - (-2 * k + 2) ** 2 / 2;
        if (k >= 1) return finish();
        view = {h: a.h + (b.h - a.h) * e, hp: a.hp + (b.hp - a.hp) * e, perm: a.perm + (b.perm - a.perm) * e, total: a.total + (b.total - a.total) * e, dry: k > .5 ? b.dry : a.dry};
        draw(view);
        requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
      setTimeout(finish, ms + 80);   // hidden tabs pause animation frames: still finish the year
    });
  }

  /* ---------- screens and controls ---------- */
  const fmt$ = v => '$' + Math.round(v).toLocaleString('en-US');
  const show = id => ['scrStart', 'scrPlay', 'scrEnd'].forEach(s => { $(s).hidden = s !== id; });
  const pump = $('pump');

  function setPump(v){
    pump.value = v; pump.setAttribute('aria-valuetext', PUMP_NAME[v]);
    document.querySelectorAll('.vp-stops button').forEach(b => b.classList.toggle('on', +b.dataset.v === +v));
    const m = $('pumpMeaning'); m.textContent = PUMP_TXT[v]; m.classList.toggle('hard', +v === 2);
  }
  pump.addEventListener('input', () => setPump(+pump.value));
  document.querySelectorAll('.vp-stops button').forEach(b => b.addEventListener('click', () => { setPump(+b.dataset.v); pump.focus(); }));

  const ICON = {
    wet: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 15a4 4 0 1 1 .8-7.9A5 5 0 0 1 17.6 9 3.5 3.5 0 0 1 17 16H7z"/><path d="M8 19l-1 2M12 19l-1 2M16 19l-1 2"/></svg>',
    dry: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'};
  function header(){
    $('yearLbl').textContent = 'Year ' + Math.min(S.year, YEARS);
    const c = $('yearType'); c.className = 'vp-chip ' + S.type;
    c.innerHTML = ICON[S.type] + YEAR[S.type].label;
  }
  function stats(){
    $('stIncome').textContent = fmt$(S.income);
    $('stSunk').textContent = Math.max(0, total(S)).toFixed(1);
    $('stPerm').textContent = S.perm.toFixed(1);
  }
  function alert(msg, good){
    const a = $('alert');
    if (!msg) { a.hidden = true; return; }
    a.textContent = msg; a.classList.toggle('good', !!good); a.hidden = false;
    a.style.animation = 'none'; void a.offsetWidth; a.style.animation = '';
  }
  function message(r){
    const f = S.flags;
    if (r.newPerm > 0 && !f.perm) { f.perm = 1; return ['Water fell below its lowest level ever — this sinking is now permanent.']; }
    if (r.dry && !f.dry) { f.dry = 1; return ['The water dropped below the wells. Some farms ran dry and lost part of their harvest.']; }
    if (S.perm >= 20 && !f.canal) { f.canal = 1; return ['The ground sank unevenly: the canal now tilts and carries less water.']; }
    if (r.newPerm === 0 && S.perm > 0 && S.h > r.before.h && !f.rise) { f.rise = 1; return ['The water rose again and the ground bounced back a little. The permanent part stays.', true]; }
    if (r.newPerm > 0 && r.level === 2 && r.type === 'dry' && !f.hard) { f.hard = 1; return ['Pumping hard in a dry year: the biggest drop in the whole game comes from years like this.']; }
    return [null];
  }

  let busy = false;
  async function next(){
    if (busy || $('scrPlay').hidden) return;
    busy = true; $('btnNext').disabled = true;
    const r = playYear(+pump.value);
    stats();
    const [msg, good] = message(r); alert(msg, good);
    await tween(view, r.summer, 650);
    await tween(view, r.winter, 450);
    S.year++;
    if (S.year > YEARS) return end();
    S.type = Math.random() < 0.45 ? 'wet' : 'dry';
    header();
    busy = false; $('btnNext').disabled = false;
  }

  function end(){
    busy = false; $('btnNext').disabled = false;
    const perm = S.perm, sunk = Math.max(0, total(S));
    $('endIncome').textContent = fmt$(S.income);
    $('endSunk').textContent = sunk.toFixed(1);
    $('endPerm').textContent = perm.toFixed(1);
    let v;
    if (perm < 2) v = `Your farms earned ${fmt$(S.income)} million and the ground barely moved. Saving water in dry years kept the valley safe.`;
    else {
      v = `Your farms earned ${fmt$(S.income)} million, but ${perm.toFixed(0)} cm of ground is gone for good.`;
      if (S.flags.dry) v += ' Wells ran dry.';
      if (S.flags.canal) v += ' The canal now carries less water.';
    }
    $('endVerdict').textContent = v;
    $('endTitle').textContent = perm < 2 ? 'A valley that lasts' : perm < 20 ? 'A valley that sank a little' : 'A valley that sank for good';
    show('scrEnd'); $('btnAgain').focus();
  }

  function start(){
    newGame(); setPump(1); header(); stats(); alert(null); draw(view);
    show('scrPlay'); $('btnNext').focus();
  }

  $('btnStart').addEventListener('click', start);
  $('btnAgain').addEventListener('click', start);
  $('btnNext').addEventListener('click', next);
  document.addEventListener('keydown', e => {
    if (e.code !== 'Space' || e.repeat) return;
    if (e.target.closest('button, a, input[type=text], textarea')) return;
    if ($('scrPlay').hidden) return;
    e.preventDefault(); next();
  });

  /* ---------- the real number: NISAR 2026 ---------- */
  fetch('../data/central_valley/summary.json', {cache: 'no-cache'})
    .then(r => r.ok ? r.json() : null)
    .then(s => {
      if (!s) return;
      const los = Math.abs(s.max_subsidence_cm), vert = Math.abs(s.max_subsidence_vertical_cm_estimate);
      const [a, b] = s.period || [];
      const days = a && b ? Math.round((Date.parse(b) - Date.parse(a)) / 864e5) : null;
      if (!isFinite(los) || !days) return;
      // tune: a normal dry summer starting 8 m above the lowest-ever level sinks the ground by NISAR's vertical estimate
      if (isFinite(vert) && vert > SE * YEAR.dry.summer) SV = (vert - SE * YEAR.dry.summer) / (YEAR.dry.summer - (H0 - HP0));
      const put = (k, v) => document.querySelectorAll(`[data-k="${k}"]`).forEach(e => { e.textContent = v; });
      put('los', los.toFixed(1)); put('days', days); put('year', a.slice(0, 4));
      $('nisarLine').hidden = false; $('endReal').hidden = false;
    })
    .catch(() => {});

  newGame(); setPump(1); draw(view);
})();
