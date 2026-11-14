// NISAR Pulse — main story. Reads files defined in rules/VERI_SOZLESMESI.md.
// Pages: site root = web/ (data/, game/, web3d/, docs/story/ copied next to it). Local dev (/web/): one level up.
const LOCAL = location.pathname.includes('/web/');
const ROOT = LOCAL ? '../' : './';
const ESRI = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
const corners = ([w, s, e, n]) => [[w, n], [e, n], [e, s], [w, s]];
const fmtDate = d => new Date(d + 'T00:00:00Z').toLocaleDateString('en-GB', {day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC'});
const fmtShort = d => new Date(d + 'T00:00:00Z').toLocaleDateString('en-GB', {day: 'numeric', month: 'short', timeZone: 'UTC'});
const minus = v => (v < 0 ? '−' : '+') + Math.abs(v).toFixed(1);
async function J(p){ try{ const r = await fetch(ROOT + p, {cache: 'no-cache'}); return r.ok ? await r.json() : null; }catch(e){ return null; } }
function setK(k, v){ document.querySelectorAll(`[data-k="${k}"]`).forEach(e => e.textContent = v); }
const STYLE = {version: 8,
  sources: {sat: {type: 'raster', tiles: [ESRI], tileSize: 256, attribution: 'Imagery © Esri, Maxar, Earthstar Geographics'}},
  layers: [{id: 'sat', type: 'raster', source: 'sat', paint: {'raster-brightness-max': 0.72, 'raster-saturation': -0.25}}]};
// Everyday sizes: coin ≈ 2.4 cm (1 € 2.33 cm, US quarter 2.43 cm), bank card 5.4 × 8.56 cm (ISO/IEC 7810 ID-1), A4 21 × 29.7 cm.
const SCALE = [[2.4, 'the width of a coin'], [5.4, 'the short side of a bank card'], [8.56, 'the long side of a bank card'], [21.0, 'the short side of an A4 sheet'], [29.7, 'the long side of an A4 sheet']];
const human = cm => { const a = Math.abs(cm); return SCALE.reduce((b, s) => Math.abs(s[0] - a) < Math.abs(b[0] - a) ? s : b)[1]; };
const NOISE_CM = 1.0; // below this a single point is within the measurement noise (docs/story/uncertainty.md)
const chartOpts = yTitle => ({responsive: true, animation: {duration: 300}, plugins: {legend: {labels: {color: '#2d3748', boxWidth: 12, font: {family: 'Inter', size: 11}}}},
  scales: {x: {ticks: {color: '#4a5568', font: {size: 10}}, grid: {color: '#e5e9f0'}}, y: {ticks: {color: '#4a5568', font: {size: 10}}, grid: {color: '#e5e9f0'}, title: {display: true, text: yTitle, color: '#4a5568'}}}});

const D = {};
async function load(){
  [D.cvMeta, D.cvSum, D.cvPts, D.val, D.assets, D.kpMeta, D.kpSum, D.sinks, D.uk, D.kpAssets, D.cvArea, D.ukClay, D.fens] = await Promise.all([
    J('data/central_valley/meta.json'), J('data/central_valley/summary.json'), J('data/central_valley/points.json'),
    J('data/central_valley/validation.json'), J('data/central_valley/assets.json'),
    J('data/karapinar/meta.json'), J('data/karapinar/summary.json'), J('data/karapinar/sinkholes.geojson'), J('data/uk/meta.json'),
    J('data/karapinar/assets.json'), J('data/central_valley/area_stats.json'), J('data/uk_clay/detection.json'), J('data/fens/crops.json')]);
  if (D.cvSum){ setK('cv.max', minus(D.cvSum.max_subsidence_cm)); setK('cv.maxabs', Math.abs(D.cvSum.max_subsidence_cm).toFixed(1)); setK('cv.vert', '≈' + minus(D.cvSum.max_subsidence_vertical_cm_estimate)); setK('cv.pairs', D.cvSum.n_pairs);
    setK('cv.period', `${fmtShort(D.cvSum.period[0])} – ${fmtDate(D.cvSum.period[1])}`); }
  if (D.cvArea?.area_km2_lt_5cm) setK('cv.area5', Math.round(D.cvArea.area_km2_lt_5cm.at(-1)));
  if (D.assets?.summary){ const s = D.assets.summary; setK('risk.high', s.high_risk_count); setK('risk.med', s.medium_risk_count); setK('risk.low', s.low_risk_count); setK('risk.evaluated', s.evaluated_segments); }
  if (D.val){ setK('gnss.good', D.val.filter(s => s.corr >= 0.4).length); setK('gnss.n', D.val.length);
    const r = D.val.map(s => s.rmse_cm).sort((a, b) => a - b), n = r.length; setK('gnss.mederr', (n % 2 ? r[(n - 1) / 2] : (r[n / 2 - 1] + r[n / 2]) / 2).toFixed(1)); }
  if (D.ukClay?.status === 'below_detection'){ setK('uk.clayThr', D.ukClay.detection_threshold_cm.toFixed(1)); const e = document.getElementById('ukClay'); if (e) e.hidden = false; }
  if (D.kpSum){ setK('kp.max', minus(D.kpSum.max_subsidence_cm)); setK('kp.pairs', D.kpSum.n_pairs); setK('kp.period', `${fmtShort(D.kpSum.period[0])} – ${fmtDate(D.kpSum.period[1])}`); }
  if (D.sinks) setK('kp.sinks', D.sinks.features.length);
  if (D.uk) setK('uk.date', fmtDate(D.uk.date));
}

/* ---------- what we found: docs/story/key_findings_public.md (numbered list) ---------- */
const esc = s => s.replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
async function findings(){
  let md; try{ const r = await fetch(ROOT + 'docs/story/key_findings_public.md', {cache: 'no-cache'}); if (!r.ok) return; md = await r.text(); }catch(e){ return; }
  const items = [...md.matchAll(/^\d+\.\s+\*\*(.+?)\*\*\s*(.+)$/gm)].map(m => ({
    title: m[1].replace(/:\s*$/, '').replace(/\s*\([^)]*\d{4}\)\s*$/, ''),
    text: m[2].replace(/\s*\([^()]*`[^`]+`[^()]*\)/g, '').replace(/`/g, '').trim()}));
  if (!items.length) return;
  document.getElementById('findingsList').innerHTML = items.map((f, i) =>
    `<article class="finding"><span class="fnum">${i + 1}</span><h3>${esc(f.title)}</h3><p>${esc(f.text)}</p></article>`).join('');
  document.getElementById('findings').hidden = false;
}

/* ---------- hero: live NISAR layer ---------- */
function hero(){
  if (!D.cvMeta) return;
  const m = D.cvMeta, base = ROOT + 'data/central_valley/disp/';
  // flat view: a tilted map shows the horizon, which MapLibre paints light grey behind the hero text
  const heroStyle = {...STYLE, layers: [{id: 'bg', type: 'background', paint: {'background-color': '#05080f'}}, ...STYLE.layers]};
  const hm = new maplibregl.Map({container: 'heroMap', style: heroStyle, center: [-119.45, 36.1], zoom: 8.4, interactive: false, attributionControl: false, pitch: 0, bearing: -12});
  hm.on('load', () => {
    // put the measured area in the right part of the screen, clear of the headline (left column on wide screens)
    const W = hm.getContainer().clientWidth, wide = W > 860;
    hm.fitBounds([[m.bbox[0], m.bbox[1]], [m.bbox[2], m.bbox[3]]], {duration: 0, bearing: -12,
      padding: wide ? {left: Math.round(W * 0.48), right: 40, top: 90, bottom: 70} : {left: 20, right: 20, top: 70, bottom: Math.round(hm.getContainer().clientHeight * 0.55)}});
    hm.addSource('h', {type: 'image', url: base + m.dates[0] + '.png', coordinates: corners(m.bbox)});
    hm.addLayer({id: 'h', type: 'raster', source: 'h', paint: {'raster-opacity': 0.85, 'raster-fade-duration': 600}});
    let i = 0; setInterval(() => { i = (i + 1) % m.dates.length; hm.getSource('h').updateImage({url: base + m.dates[i] + '.png', coordinates: corners(m.bbox)}); }, 1400);
    let b = -12; setInterval(() => { b += 0.04; hm.setBearing(b); }, 60);
  });
}

/* ---------- story map ---------- */
let map, chartP, chartG, cvIdx = 0, timer = null;
const CVB = [-120.2, 35.6, -119.0, 36.6];
const VIEWS = {
  intro: {center: [-45, 42], zoom: 1.4, layers: ['sites']},
  uk:    {bbox: [-0.3, 52.4, 0.4, 52.9], layers: ['uk-radar'], tag: 'NISAR radar image, 20 Oct 2026 · PREVIEW'},
  cv:    {bbox: CVB, layers: ['cv-disp', 'cv-pts'], tag: 'NISAR ground motion · PROVISIONAL', legend: true},
  gnss:  {bbox: CVB, layers: ['cv-disp', 'gnss'], dim: true, tag: 'GPS stations (green: r ≥ 0.4)', legend: true},
  risk:  {bbox: CVB, layers: ['cv-disp', 'risk'], dim: true, tag: 'Infrastructure tilt risk', legend: true},
  kp:    {bbox: [33.3, 37.6, 33.8, 37.9], layers: ['kp-disp', 'sinks'], tag: 'NISAR ground motion · PROVISIONAL', legend: true},
};
const ALL = ['sites', 'uk-radar', 'cv-disp', 'cv-pts', 'gnss', 'risk', 'kp-disp', 'sinks'];
const fc = feats => ({type: 'FeatureCollection', features: feats});
const pt = (props, c) => ({type: 'Feature', properties: props, geometry: {type: 'Point', coordinates: c}});

function storyMap(){
  map = new maplibregl.Map({container: 'map', style: STYLE, center: VIEWS.intro.center, zoom: VIEWS.intro.zoom, attributionControl: {compact: true}, scrollZoom: false});
  map.addControl(new maplibregl.NavigationControl({showCompass: false}), 'top-left');
  map.on('load', () => {
    map.addSource('sites', {type: 'geojson', data: fc([pt({}, [0.0, 52.6]), pt({}, [-119.5, 36.1]), pt({}, [33.55, 37.75])])});
    map.addLayer({id: 'sites', type: 'circle', source: 'sites', paint: {'circle-radius': 9, 'circle-color': '#ff5a47', 'circle-stroke-color': '#fff', 'circle-stroke-width': 2}});
    if (D.uk){ map.addSource('uk', {type: 'image', url: ROOT + `data/uk/radar_${D.uk.date}.png`, coordinates: corners(D.uk.bbox)}); map.addLayer({id: 'uk-radar', type: 'raster', source: 'uk', paint: {'raster-opacity': 0.9}}); }
    if (D.cvMeta){
      const m = D.cvMeta; cvIdx = m.dates.length - 1;
      map.addSource('cv', {type: 'image', url: ROOT + `data/central_valley/disp/${m.dates[cvIdx]}.png`, coordinates: corners(m.bbox)});
      map.addLayer({id: 'cv-disp', type: 'raster', source: 'cv', paint: {'raster-opacity': 0.85, 'raster-fade-duration': 0}});
    }
    if (D.cvPts){
      map.addSource('cvp', {type: 'geojson', data: fc(D.cvPts.map(p => pt({id: p.id}, [p.lon, p.lat])))});
      map.addLayer({id: 'cv-pts', type: 'circle', source: 'cvp', paint: {'circle-radius': 6, 'circle-color': '#fff', 'circle-stroke-color': '#1a1f29', 'circle-stroke-width': 2}});
      map.on('click', 'cv-pts', e => pickPoint(e.features[0].properties.id));
    }
    if (D.val){
      map.addSource('gnss', {type: 'geojson', data: fc(D.val.map(s => pt({st: s.station, r: s.corr}, [s.lon, s.lat])))});
      map.addLayer({id: 'gnss', type: 'circle', source: 'gnss', paint: {'circle-radius': 8, 'circle-color': ['case', ['>=', ['get', 'r'], 0.4], '#3fb950', '#6b7a96'], 'circle-stroke-color': '#fff', 'circle-stroke-width': 2}});
      map.on('click', 'gnss', e => pickStation(e.features[0].properties.st));
    }
    if (D.assets){
      map.addSource('risk', {type: 'geojson', data: D.assets});
      map.addLayer({id: 'risk', type: 'line', source: 'risk', paint: {'line-width': ['match', ['get', 'risk'], 'high', 3.5, 'medium', 2.2, 1.1],
        'line-color': ['match', ['get', 'risk'], 'high', '#ff5a47', 'medium', '#e3b341', '#3fb950'], 'line-opacity': 0.95}});
      map.on('click', 'risk', e => { const p = e.features[0].properties; popup(e.lngLat, `<b>${p.name || p.type}</b><br>${p.type} · risk <b>${p.risk}</b><br>gradient ${(+p.gradient_mm_per_km).toFixed(1)} mm/km · max ${(+p.max_cm).toFixed(1)} cm`); });
    }
    if (D.kpMeta){
      const m = D.kpMeta;
      map.addSource('kp', {type: 'image', url: ROOT + `data/karapinar/disp/${m.dates.at(-1)}.png`, coordinates: corners(m.bbox)});
      map.addLayer({id: 'kp-disp', type: 'raster', source: 'kp', paint: {'raster-opacity': 0.8}});
    }
    if (D.sinks){
      map.addSource('sinks', {type: 'geojson', data: D.sinks});
      map.addLayer({id: 'sinks', type: 'circle', source: 'sinks', paint: {'circle-radius': 6, 'circle-color': '#ff5a47', 'circle-stroke-color': '#fff', 'circle-stroke-width': 1.5}});
      map.on('click', 'sinks', e => { const p = e.features[0].properties; popup(e.lngLat, `<b>${p.name}</b>${p.year_formed ? ' · ' + p.year_formed : ''}<br><a href="${p.source_url}" target="_blank" rel="noopener">${p.source_title || 'source'}</a>`); });
    }
    for (const id of ['cv-pts', 'gnss', 'risk', 'sinks']) if (map.getLayer(id)){ map.on('mouseenter', id, () => map.getCanvas().style.cursor = 'pointer'); map.on('mouseleave', id, () => map.getCanvas().style.cursor = ''); }
    show('intro'); observe();
  });
}
function popup(ll, html){ new maplibregl.Popup().setLngLat(ll).setHTML(html).addTo(map); }
let current = '';
function inView(v){ if (!v.bbox) return map.getZoom() < 3; const c = map.getCenter(); return c.lng > v.bbox[0] && c.lng < v.bbox[2] && c.lat > v.bbox[1] && c.lat < v.bbox[3] && map.getZoom() > 6; }
function show(step, force){
  const v = VIEWS[step]; if (!v || (step === current && !force)) return;
  if (force && step === current && inView(v)) return;
  current = step;
  for (const id of ALL) if (map.getLayer(id)) map.setLayoutProperty(id, 'visibility', v.layers.includes(id) ? 'visible' : 'none');
  if (map.getLayer('cv-disp')) map.setPaintProperty('cv-disp', 'raster-opacity', v.dim ? 0.45 : 0.85);
  if (v.bbox) map.fitBounds([[v.bbox[0], v.bbox[1]], [v.bbox[2], v.bbox[3]]], {padding: 40, duration: 1800, essential: true});
  else map.flyTo({center: v.center, zoom: v.zoom, duration: 1800, essential: true});
  document.getElementById('mapLegend').style.display = v.legend ? '' : 'none';
  const lm = step === 'kp' ? D.kpMeta : D.cvMeta;
  // colours saturate at vmin/vmax, so the ends of the scale read '≤' / '≥'
  if (lm){ document.getElementById('lgMin').textContent = '≤ −' + Math.abs(lm.vmin); document.getElementById('lgMax').textContent = '≥ +' + lm.vmax; }
  const t = document.getElementById('mapTag'); t.textContent = v.tag || ''; t.style.display = v.tag ? '' : 'none';
}
function observe(){
  const steps = [...document.querySelectorAll('.step')];
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting){ steps.forEach(s => s.classList.toggle('is-active', s === e.target)); show(e.target.dataset.step); } }), {rootMargin: '-40% 0px -50% 0px'});
  steps.forEach(s => io.observe(s));
  let t; window.addEventListener('scroll', () => { clearTimeout(t); t = setTimeout(() => { const a = document.querySelector('.step.is-active'); if (a && !map.isMoving()) show(a.dataset.step, true); }, 400); }, {passive: true});
}

/* ---------- Chapter 2: compare ---------- */
function compare(){
  if (!D.uk) return;
  document.getElementById('ukOptical').src = ROOT + `data/uk/optical_${D.uk.date}.jpg`;
  document.getElementById('ukRadar').src = ROOT + `data/uk/radar_${D.uk.date}.png`;
  const r = document.getElementById('compareRange'), box = document.getElementById('compare');
  const up = () => box.style.setProperty('--split', r.value + '%'); r.addEventListener('input', up); up();
}

/* ---------- Chapter 3: time + points ---------- */
function cvControls(){
  if (!D.cvMeta) return;
  const m = D.cvMeta, s = document.getElementById('slider'), lbl = document.getElementById('dateLbl'), btn = document.getElementById('cvPlay');
  s.max = m.dates.length - 1; s.value = m.dates.length - 1; lbl.textContent = fmtDate(m.dates.at(-1));
  const go = i => { cvIdx = i; s.value = i; lbl.textContent = fmtDate(m.dates[i]); const src = map?.getSource('cv'); if (src) src.updateImage({url: ROOT + `data/central_valley/disp/${m.dates[i]}.png`, coordinates: corners(m.bbox)}); };
  s.addEventListener('input', () => go(+s.value));
  btn.addEventListener('click', () => { if (timer){ clearInterval(timer); timer = null; btn.textContent = '▶'; return; } btn.textContent = '❚❚'; timer = setInterval(() => go((cvIdx + 1) % m.dates.length), 900); });
  if (D.cvPts?.length){ const worst = D.cvPts.reduce((a, b) => (b.disp_cm.at(-1) ?? 0) < (a.disp_cm.at(-1) ?? 0) ? b : a); pickPoint(worst.id); }
}
function pickPoint(id){
  const p = D.cvPts.find(q => q.id === id); if (!p) return;
  const v = p.disp_cm.at(-1), r = document.getElementById('readout');
  if (v == null){ r.textContent = `${p.name}: no reliable measurement here.`; return; }
  const days = Math.round((new Date(p.dates.at(-1)) - new Date(p.dates[0])) / 864e5);
  const months = (Math.round(days / 30.44 * 2) / 2).toString().replace(/\.5$/, '½');
  const span = `${fmtShort(p.dates[0])} – ${fmtShort(p.dates.at(-1))} (${months} months)`;
  r.innerHTML = Math.abs(v) < NOISE_CM
    ? `<b>${p.name}</b>: no clear change (${minus(v)} cm), within the measurement noise of about ±${NOISE_CM} cm · ${span}.`
    : `<b>${p.name}</b> ${v < 0 ? 'sank' : 'rose'} about <b>${Math.abs(v).toFixed(1)} cm</b> as seen by the satellite · ${span} — about ${human(v)}.`;
  const data = {labels: p.dates.map(fmtShort), datasets: [{label: 'Ground motion seen by NISAR (cm)', data: p.disp_cm, borderColor: '#ff5a47', backgroundColor: 'rgba(255,90,71,.12)', fill: true, tension: .25, pointRadius: 3}]};
  if (chartP){ chartP.data = data; chartP.update(); } else chartP = new Chart(document.getElementById('pointChart'), {type: 'line', data, options: chartOpts('cm')});
}

/* ---------- Chapter 4: GNSS ---------- */
function gnssTable(){
  if (!D.val) return;
  const sorted = D.val.slice().sort((a, b) => b.corr - a.corr), tb = document.querySelector('#gnssTable tbody');
  tb.innerHTML = sorted.map(s => `<tr data-st="${s.station}"><td>${s.station}</td><td class="${s.corr >= 0.4 ? 'good' : 'weak'}">${s.corr.toFixed(2)}</td><td>${s.rmse_cm.toFixed(1)}</td><td>${minus(s.gnss.at(-1))}</td><td>${minus(s.insar.at(-1))}</td></tr>`).join('');
  tb.querySelectorAll('tr').forEach(tr => tr.addEventListener('click', () => pickStation(tr.dataset.st)));
  pickStation(sorted[0].station);
}
function pickStation(st){
  const s = D.val.find(x => x.station === st); if (!s) return;
  document.querySelectorAll('#gnssTable tr').forEach(tr => tr.classList.toggle('sel', tr.dataset.st === st));
  const data = {labels: s.dates.map(fmtShort), datasets: [
    {label: `GPS ${s.station} (up, cm)`, data: s.gnss, borderColor: '#3fb950', tension: .2, pointRadius: 3},
    {label: 'NISAR, converted to up–down (cm)', data: s.insar, borderColor: '#4fb6ff', borderDash: [5, 4], tension: .2, pointRadius: 3}]};
  if (chartG){ chartG.data = data; chartG.update(); } else chartG = new Chart(document.getElementById('gnssChart'), {type: 'line', data, options: chartOpts('cm')});
}

/* ---------- Chapter 5: risk ---------- */
function riskList(){
  if (!D.assets) return;
  const top = D.assets.features.filter(f => f.properties.risk === 'high').sort((a, b) => b.properties.gradient_mm_per_km - a.properties.gradient_mm_per_km).slice(0, 6);
  const ol = document.getElementById('riskList');
  ol.innerHTML = top.map((f, i) => `<li data-i="${i}">${f.properties.name || f.properties.type} — <span>${f.properties.gradient_mm_per_km.toFixed(0)} mm/km</span>, ${f.properties.max_cm.toFixed(1)} cm</li>`).join('');
  ol.querySelectorAll('li').forEach(li => li.addEventListener('click', () => { const c = top[+li.dataset.i].geometry.coordinates; map.flyTo({center: c[Math.floor(c.length / 2)], zoom: 12, duration: 1500}); }));
}

/* ---------- Chapter 3: full-year box (mixed series, data/central_valley_fullyear) ---------- */
async function fullYear(){
  const d = await J('data/central_valley_fullyear/decomp.json'); const p = d?.point_decompositions?.[0];
  if (!p || d.status !== 'ok') return;
  setK('fy.name', p.name); setK('fy.end', Math.abs(p.end_disp_cm).toFixed(1)); setK('fy.perm', Math.abs(p.permanent_cm_per_yr).toFixed(1)); setK('fy.swing', p.seasonal_peak_to_peak_cm.toFixed(1));
  const im = document.getElementById('fyImg'); im.src = ROOT + im.dataset.src;
  document.getElementById('fyBox').hidden = false;
}

/* ---------- Chapter 2: HH vs HV (Fens fields) ---------- */
function polChart(){
  const f = D.fens; if (!f?.fields?.length) return;
  const mean = key => f.dates.map((_, t) => f.fields.reduce((a, x) => a + x[key][t], 0) / f.fields.length);
  const hh = mean('hh_db'), hv = mean('hv_db'), diff = hh.reduce((a, v, i) => a + v - hv[i], 0) / hh.length;
  setK('fens.n', f.fields.length); setK('fens.diff', diff.toFixed(0)); setK('fens.period', `${fmtShort(f.dates[0])} – ${fmtDate(f.dates.at(-1))}`);
  document.getElementById('polBox').hidden = false;
  new Chart(document.getElementById('polChart'), {type: 'line', data: {labels: f.dates.map(fmtShort), datasets: [
    {label: 'HH (dB)', data: hh.map(v => +v.toFixed(1)), borderColor: '#0b3d91', tension: .25, pointRadius: 3},
    {label: 'HV (dB)', data: hv.map(v => +v.toFixed(1)), borderColor: '#1f7a35', tension: .25, pointRadius: 3}]}, options: chartOpts('dB')});
}

/* ---------- Chapter 6: sinkholes ---------- */
function ringChart(){
  const ra = D.kpAssets?.summary?.sinkhole_ring_analysis; if (!ra?.disjoint_rings) return;
  const rings = ra.disjoint_rings, bg = rings.find(r => r.band.startsWith('>')), r1 = rings[0];
  setK('kp.ring1', Math.abs(r1.mean_cm).toFixed(1)); setK('kp.ringbg', Math.abs(bg.mean_cm).toFixed(1)); setK('kp.ringN', ra.sinkholes_inside_1km_footprint);
  document.getElementById('ringBox').hidden = false;
  new Chart(document.getElementById('ringChart'), {type: 'bar',
    data: {labels: rings.map(r => r.band.replace(' (background)', '')), datasets: [{label: 'Average sinking (cm)', data: rings.map(r => Math.abs(r.mean_cm)), backgroundColor: ['#c8321f', '#d6604d', '#e8a08f', '#b8c2d0']}]},
    options: {...chartOpts('cm sinking'), plugins: {legend: {display: false}}, scales: {...chartOpts('cm sinking').scales, x: {...chartOpts('').scales.x, title: {display: true, text: 'Distance from nearest sinkhole', color: '#4a5568'}}}}});
}
function sinkList(){
  if (!D.sinks) return;
  const ul = document.getElementById('sinkList');
  ul.innerHTML = D.sinks.features.map((f, i) => `<li data-i="${i}">${f.properties.name}${f.properties.year_formed ? ' · ' + f.properties.year_formed : ''}</li>`).join('');
  ul.querySelectorAll('li').forEach(li => li.addEventListener('click', () => map.flyTo({center: D.sinks.features[+li.dataset.i].geometry.coordinates, zoom: 13, duration: 1500})));
}

/* ---------- simulator + 3D ---------- */
function extras(){
  const g = ROOT + 'game/index.html', v3 = ROOT + 'web3d/index.html';
  const vid = document.getElementById('cvVideo'); if (vid) vid.src = ROOT + 'docs/story/media/cv_subsidence.mp4';
  document.getElementById('gameOpen').href = g; document.getElementById('view3d').href = v3;
  // the game loads only on request: the page stays fast and the poster explains what it is
  document.getElementById('gamePlay')?.addEventListener('click', () => {
    const box = document.getElementById('gameBox'), f = document.createElement('iframe');
    f.title = 'Valley Under Pressure simulator'; f.src = g; f.allow = 'fullscreen';
    box.closest('.sim')?.classList.add('playing');
    box.replaceChildren(f); f.focus();
    box.scrollIntoView({block: 'start'});
  });
}

load().then(() => { hero(); storyMap(); compare(); cvControls(); gnssTable(); riskList(); sinkList(); ringChart(); polChart(); fullYear(); extras(); findings(); });
