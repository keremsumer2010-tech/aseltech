// NISAR satellite + radar animation over the atlas globe (PC1).
// Uses the globals `map`, `mapReady` and `selectRegion` from atlas.js; loaded after it.
(function(){
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const wrap = document.querySelector('.atlas-mapwrap');
  if (!wrap) return;

  const NS = 'http://www.w3.org/2000/svg';
  const layer = document.createElement('div');
  layer.className = 'sat-layer';
  layer.setAttribute('aria-hidden', 'true');
  layer.innerHTML = `
    <svg id="satFx">
      <defs>
        <linearGradient id="satBeamGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#7dd3fc" stop-opacity="0.55"/>
          <stop offset="1" stop-color="#38bdf8" stop-opacity="0.08"/>
        </linearGradient>
        <radialGradient id="satSpot" cx="0.5" cy="0.5" r="0.5">
          <stop offset="0" stop-color="#e0f2fe" stop-opacity="0.75"/>
          <stop offset="1" stop-color="#38bdf8" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <g class="sat-beam" id="satBeam" opacity="0">
        <polygon id="satCone" fill="url(#satBeamGrad)"/>
        <ellipse id="satFoot" fill="url(#satSpot)"/>
        <g id="satChirps"></g>
        <g id="satRings"></g>
      </g>
    </svg>
    <div class="sat-craft" id="satCraft">${craftSvg()}</div>
    <div class="sat-tag" id="satTag"><b>NISAR</b> · L-band radar (24 cm) · 12-day repeat</div>`;
  wrap.appendChild(layer);

  const craft = layer.querySelector('#satCraft');
  const tag = layer.querySelector('#satTag');
  const beam = layer.querySelector('#satBeam');
  const cone = layer.querySelector('#satCone');
  const foot = layer.querySelector('#satFoot');
  const chirps = layer.querySelector('#satChirps');
  const rings = layer.querySelector('#satRings');
  const chirpEls = [0, 1, 2, 3].map(() => mk('ellipse', 'sat-chirp', chirps));
  const ringEls = [0, 1, 2].map(() => mk('ellipse', 'sat-ring', rings));

  function mk(tagName, cls, parent){
    const el = document.createElementNS(NS, tagName);
    el.setAttribute('class', cls);
    parent.appendChild(el);
    return el;
  }

  function craftSvg(){
    // Stylised NISAR: solar wing, gold bus, deployable boom and 12 m mesh reflector.
    const panels = Array.from({length: 6}, (_, i) =>
      `<rect x="${4 + i * 7}" y="20" width="6.2" height="14" fill="#1e3a8a" stroke="#93c5fd" stroke-width=".5"/>`).join('');
    const ribs = Array.from({length: 10}, (_, i) => {
      const a = (i / 10) * Math.PI * 2;
      return `<line x1="86" y1="60" x2="${(86 + 27 * Math.cos(a)).toFixed(1)}" y2="${(60 + 10 * Math.sin(a)).toFixed(1)}" stroke="#94a3b8" stroke-width=".6"/>`;
    }).join('');
    return `<svg viewBox="0 0 118 84" xmlns="${NS}">
      <line x1="46" y1="27" x2="52" y2="27" stroke="#cbd5e1" stroke-width="1.5"/>
      ${panels}
      <rect x="52" y="18" width="18" height="18" rx="1.5" fill="#d4a017" stroke="#fde68a" stroke-width=".8"/>
      <rect x="55" y="21" width="12" height="4" fill="#b45309" opacity=".7"/>
      <line x1="66" y1="35" x2="84" y2="55" stroke="#e2e8f0" stroke-width="1.6"/>
      <ellipse cx="86" cy="60" rx="27" ry="10" fill="rgba(241,245,249,.55)" stroke="#f8fafc" stroke-width="1.6"/>
      ${ribs}
      <circle cx="86" cy="60" r="2" fill="#f8fafc"/>
    </svg>`;
  }

  // ---- state ----
  const D2R = Math.PI / 180;
  let cur = {lon: 20, lat: 30};          // sub-satellite point now
  let from = null, to = null, t0 = 0, dur = 2400;
  let target = null;                       // selected ground point
  let arrivedAt = 0;

  function slerp(a, b, t){
    const va = vec(a), vb = vec(b);
    const dot = Math.min(1, Math.max(-1, va[0]*vb[0] + va[1]*vb[1] + va[2]*vb[2]));
    const om = Math.acos(dot);
    if (om < 1e-6) return {lon: b.lon, lat: b.lat};
    const s = Math.sin(om), k1 = Math.sin((1 - t) * om) / s, k2 = Math.sin(t * om) / s;
    const v = [k1*va[0] + k2*vb[0], k1*va[1] + k2*vb[1], k1*va[2] + k2*vb[2]];
    return {lon: Math.atan2(v[1], v[0]) / D2R, lat: Math.asin(v[2]) / D2R};
  }
  function vec(p){ const la = p.lat * D2R, lo = p.lon * D2R; return [Math.cos(la)*Math.cos(lo), Math.cos(la)*Math.sin(lo), Math.sin(la)]; }
  function angDist(a, b){ const va = vec(a), vb = vec(b); return Math.acos(Math.min(1, Math.max(-1, va[0]*vb[0] + va[1]*vb[1] + va[2]*vb[2]))) / D2R; }
  const ease = t => t < .5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3) / 2;

  function flyTo(lon, lat){
    target = {lon, lat};
    if (reduce){ cur = {lon, lat}; from = null; arrivedAt = performance.now(); return; }
    from = {...cur}; to = {lon, lat}; t0 = performance.now();
    dur = Math.min(3200, 1400 + angDist(from, to) * 18);
    arrivedAt = 0;
  }

  // Hook into the atlas selection without editing atlas.js.
  if (typeof selectRegion === 'function'){
    const orig = selectRegion;
    selectRegion = async function(id, fly, upd){
      const r = (typeof atlasData !== 'undefined' && atlasData?.regions) ? atlasData.regions.find(x => x.id === id) : null;
      if (r && typeof r.lon === 'number' && typeof r.lat === 'number') flyTo(r.lon, r.lat);
      return orig.apply(this, arguments);
    };
  }

  function visible(p){
    try{ const c = map.getCenter(); return angDist({lon: c.lng, lat: c.lat}, p) < 78; }catch(e){ return true; }
  }

  function frame(now){
    requestAnimationFrame(frame);
    if (typeof map === 'undefined' || !map || !mapReady) return;

    if (from && to){
      const k = Math.min(1, (now - t0) / dur);
      cur = slerp(from, to, ease(k));
      if (k >= 1){ from = null; arrivedAt = now; }
    }

    const zoom = map.getZoom();
    const alt = 70 + Math.min(70, zoom * 11);            // apparent altitude in px
    const side = 36 + Math.min(40, zoom * 6);            // side-looking offset
    const bob = reduce ? 0 : Math.sin(now / 900) * 3;
    const g = map.project([cur.lon, cur.lat]);
    const sx = g.x - side, sy = g.y - alt + bob;
    const on = visible(cur);

    craft.style.opacity = on ? '1' : '0';
    tag.style.opacity = on ? '1' : '0';
    craft.style.transform = `translate(${sx}px, ${sy}px)`;
    tag.style.transform = `translate(calc(${sx}px - 50%), ${sy - 80}px)`;

    // Radar beam: only once the craft has arrived over the selected point.
    const showBeam = target && !from && arrivedAt && on && visible(target);
    if (!showBeam){ beam.setAttribute('opacity', '0'); return; }
    const p = map.project([target.lon, target.lat]);
    const ax = sx + 36.6, ay = sy + 24.4;                  // reflector centre (craft local 86,60 → offset)
    const rx = 30 + zoom * 4, ry = rx * 0.36;
    const since = now - arrivedAt;
    beam.setAttribute('opacity', String(Math.min(1, since / 350)));
    cone.setAttribute('points', `${ax},${ay} ${p.x - rx},${p.y} ${p.x + rx},${p.y}`);
    foot.setAttribute('cx', p.x); foot.setAttribute('cy', p.y);
    foot.setAttribute('rx', rx * 1.25); foot.setAttribute('ry', ry * 1.25);

    // Chirps travelling down the beam (pulses of radar energy).
    chirpEls.forEach((el, i) => {
      const t = reduce ? (i + 1) / 5 : ((since / 900) + i / chirpEls.length) % 1;
      el.setAttribute('cx', ax + (p.x - ax) * t);
      el.setAttribute('cy', ay + (p.y - ay) * t);
      el.setAttribute('rx', 4 + rx * t);
      el.setAttribute('ry', 1.5 + ry * t);
      el.setAttribute('opacity', (Math.sin(Math.PI * t) * 0.9).toFixed(2));
    });
    // Echo rings spreading on the ground.
    ringEls.forEach((el, i) => {
      const t = reduce ? 0.5 : ((since / 1600) + i / ringEls.length) % 1;
      el.setAttribute('cx', p.x); el.setAttribute('cy', p.y);
      el.setAttribute('rx', rx * (0.6 + 1.8 * t));
      el.setAttribute('ry', ry * (0.6 + 1.8 * t));
      el.setAttribute('opacity', ((1 - t) * 0.8).toFixed(2));
    });
  }
  requestAnimationFrame(frame);
})();
