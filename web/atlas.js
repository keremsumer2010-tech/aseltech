// NISAR Pulse — Global Subsidence Atlas 2026 (Atlas Final v2 + Takviye)
const LOCAL = location.pathname.includes('/web/');
const ROOT = LOCAL ? '../' : './';
const ESRI = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
const BLUEMARBLE = ROOT + 'web/assets/bluemarble_2k.jpg';
const STYLE = {
  version: 8,
  sources: {
    bluemarble: {
      type: 'image',
      url: BLUEMARBLE,
      coordinates: [[-180, 85.0511], [180, 85.0511], [180, -85.0511], [-180, -85.0511]]
    },
    sat: {type: 'raster', tiles: [ESRI], tileSize: 256, attribution: 'Imagery © Esri, Maxar, Earthstar Geographics; Blue Marble © NASA Visible Earth'}
  },
  layers: [
    {id: 'bluemarble', type: 'raster', source: 'bluemarble', paint: {'raster-brightness-max': 0.85}},
    {id: 'sat', type: 'raster', source: 'sat', paint: {'raster-brightness-max': 0.78, 'raster-saturation': -0.2}}
  ]
};

const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const fmtNum = (v, d = 1) => (typeof v === 'number' && Number.isFinite(v)) ? (v < 0 ? '−' : (v > 0 ? '+' : '')) + Math.abs(v).toFixed(d) : '—';
const fmtUnit = (v, u, d = 1) => (typeof v === 'number' && Number.isFinite(v)) ? `${fmtNum(v, d)} ${u}` : '—';
const fmtInt = v => (typeof v === 'number' && Number.isFinite(v)) ? Math.round(v).toLocaleString('en-US') : '—';
const fmtDate = d => d ? new Date(d + 'T00:00:00Z').toLocaleDateString('en-GB', {day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC'}) : '—';
const fmtShort = d => d ? new Date(d + 'T00:00:00Z').toLocaleDateString('en-GB', {day: 'numeric', month: 'short', timeZone: 'UTC'}) : '—';
async function J(p){ try{ const r = await fetch(ROOT + p); return r.ok ? await r.json() : null; }catch(e){ return null; } }
const KNOWN_CARDS = new Set(['bangkok','beijing','cangzhou','central_valley','delhi','delta','eloy','hanoi','ho_chi_minh','isfahan','jakarta','karapinar','konya_plain','mashhad','mexico_city','quetta','rafsanjan','semarang','tehran','xian','yunlin']);
const KNOWN_SIGMA = new Set(['bangkok','beijing','central_valley','delta','hanoi','ho_chi_minh','isfahan','jakarta','karapinar','konya_plain','mashhad','mexico_city','rafsanjan','semarang','tehran']);
const KNOWN_VALNOTE = new Set(['bangkok','cangzhou','delhi','delta','eloy','hanoi','ho_chi_minh','isfahan','jakarta','konya_plain','mashhad','mexico_city','quetta','rafsanjan','semarang','tehran','xian','yunlin']);
let bulletinIds = new Set();
let qcFlags = null;
let detMap = new Map();
let robMap = new Map();
let operaMap = new Map();
let expMap = new Map();

async function initBulletins(){
  try{
    const r = await fetch(ROOT + 'docs/bulletins/index.html');
    if (!r.ok) return;
    const html = await r.text();
    const re = /href=['"]([a-z0-9_]+)\.html['"]/g;
    let m;
    while ((m = re.exec(html)) !== null) bulletinIds.add(m[1]);
  }catch(e){}
}

function rateColor(rate){
  if (typeof rate !== 'number' || !Number.isFinite(rate)) return '#64748b';
  if (rate <= -6) return '#991b1b';
  if (rate <= -4) return '#c8321f';
  if (rate <= -2) return '#d97706';
  return '#64748b';
}

function confColor(r){
  const c = (r.confidence || 'low').toLowerCase();
  if (c === 'high') return '#137333';
  if (c === 'medium' && !r.indicative_only) return '#0b3d91';
  return '#d97706';
}

function isIndicative(r){
  return Boolean(r.indicative_only || (r.confidence || '').toLowerCase() === 'low');
}

function confBadge(r){
  const c = (r.confidence || 'low').toLowerCase();
  const lbl = isIndicative(r) ? `${c} · indicative only` : c;
  return `<span class="cbadge ${esc(c)}">${esc(lbl)}</span>`;
}

function bboxToCoords(bbox){
  if (!Array.isArray(bbox) || bbox.length !== 4) return null;
  const [w, s, e, n] = bbox;
  if (![w, s, e, n].every(x => typeof x === 'number' && Number.isFinite(x))) return null;
  return [[w, n], [e, n], [e, s], [w, s]];
}

let map, mapReady = false, atlasData = null, sortedRegions = [], filteredRegions = [], activeId = null;
let activeLayer = 'disp';
let unitMode = 'los'; // 'los' | 'vert'
let animTimer = null, animDates = [], animIdx = 0, activeBase = '', activeBboxCoords = null, activeSigmaUrl = null;
let tourTimer = null, tourIdx = 0;

function stopAnim(){
  if (animTimer){ clearInterval(animTimer); animTimer = null; }
  const btn = document.getElementById('atlasPlayBtn');
  if (btn) btn.textContent = 'Play';
}

function stopTour(){
  if (tourTimer){ clearInterval(tourTimer); tourTimer = null; }
  const btn = document.getElementById('tourBtn');
  const cap = document.getElementById('tourCaption');
  if (btn){ btn.classList.remove('is-playing'); btn.textContent = 'Tour top 5'; }
  if (cap) cap.hidden = true;
}

function setMapOverlay(url, coords){
  if (!map || !mapReady) return;
  try{
    const src = map.getSource('city-overlay');
    if (!url || !coords || activeLayer === 'conf'){
      if (map.getLayer('city-overlay')) map.setLayoutProperty('city-overlay', 'visibility', 'none');
      return;
    }
    const fullUrl = ROOT + url;
    if (src){
      src.updateImage({url: fullUrl, coordinates: coords});
      if (map.getLayer('city-overlay')) map.setLayoutProperty('city-overlay', 'visibility', 'visible');
    } else {
      map.addSource('city-overlay', {type: 'image', url: fullUrl, coordinates: coords});
      map.addLayer({
        id: 'city-overlay',
        type: 'raster',
        source: 'city-overlay',
        paint: {'raster-opacity': 0.72, 'raster-fade-duration': 0}
      }, 'atlas-pts');
    }
  }catch(e){}
}

function updateLegend(){
  const el = document.getElementById('atlasLegend');
  if (!el) return;
  if (activeLayer === 'sigma'){
    el.innerHTML = `<b>Uncertainty &sigma; (cm, LOS)</b>
      <div class="al-row"><span class="al-dot" style="background:#137333"></span><span>Low chain noise (&lt; 1.0 cm)</span></div>
      <div class="al-row"><span class="al-dot" style="background:#d97706"></span><span>Moderate noise (1.0–2.5 cm)</span></div>
      <div class="al-row"><span class="al-dot" style="background:#991b1b"></span><span>High noise (&gt; 2.5 cm)</span></div>
      <div class="small" style="margin-top:4px">Overlay shows per-pixel &sigma; where available.</div>`;
  } else if (activeLayer === 'conf'){
    el.innerHTML = `<b>Confidence class</b>
      <div class="al-row"><span class="al-dot" style="background:#137333"></span><span>High confidence</span></div>
      <div class="al-row"><span class="al-dot" style="background:#0b3d91"></span><span>Medium confidence</span></div>
      <div class="al-row"><span class="al-dot" style="background:#d97706"></span><span>Low · indicative only</span></div>`;
  } else {
    el.innerHTML = `<b>Rate (cm / 100 days, LOS)</b>
      <div class="al-row"><span class="al-dot" style="background:#991b1b"></span><span>&le; &minus;6.0 cm/100d</span></div>
      <div class="al-row"><span class="al-dot" style="background:#c8321f"></span><span>&minus;4.0 to &minus;6.0 cm/100d</span></div>
      <div class="al-row"><span class="al-dot" style="background:#d97706"></span><span>&minus;2.0 to &minus;4.0 cm/100d</span></div>
      <div class="al-row"><span class="al-dot" style="background:#64748b"></span><span>&gt; &minus;2.0 cm/100d</span></div>`;
  }
}

function applyLayer(layer){
  activeLayer = layer;
  document.querySelectorAll('#atlasLayers .al-btn').forEach(b => b.classList.toggle('is-active', b.dataset.layer === layer));
  updateLegend();
  if (map && mapReady && map.getLayer('atlas-pts')){
    map.setPaintProperty('atlas-pts', 'circle-color', ['get', layer === 'conf' ? 'confColor' : 'color']);
  }
  if (layer === 'sigma'){
    setMapOverlay(activeSigmaUrl, activeBboxCoords);
  } else if (layer === 'disp' && animDates.length){
    setMapOverlay(`${activeBase}disp/${animDates[animIdx]}.png`, activeBboxCoords);
  } else {
    setMapOverlay(null, null);
  }
}

function setFrame(idx){
  if (!animDates.length) return;
  animIdx = ((idx % animDates.length) + animDates.length) % animDates.length;
  const d = animDates[animIdx];
  const img = document.getElementById('atlasAnimImg');
  const lbl = document.getElementById('atlasDateLbl');
  const rng = document.getElementById('atlasSlider');
  const url = `${activeBase}disp/${d}.png`;
  if (img) img.src = ROOT + url;
  if (lbl) lbl.textContent = fmtDate(d);
  if (rng) rng.value = String(animIdx);
  if (activeLayer === 'disp') setMapOverlay(url, activeBboxCoords);
}

function toggleAnim(){
  if (!animDates.length) return;
  const btn = document.getElementById('atlasPlayBtn');
  if (animTimer){
    stopAnim();
    return;
  }
  if (btn) btn.textContent = 'Pause';
  animTimer = setInterval(() => setFrame(animIdx + 1), 950);
}

async function initVitalSigns(){
  const vs = await J('data/global/vital_signs.json');
  if (!vs || typeof vs !== 'object') return;
  let shown = 0;
  if (typeof vs.cities_measured === 'number' && Number.isFinite(vs.cities_measured)){
    document.getElementById('vCities').textContent = fmtInt(vs.cities_measured);
    document.getElementById('vcCities').hidden = false;
    shown++;
  }
  const fName = vs.fastest?.name || vs.fastest_place;
  const fRate = vs.fastest?.rate_cm_per_100d ?? vs.fastest_rate_cm_per_100d;
  if (fName && typeof fRate === 'number' && Number.isFinite(fRate)){
    document.getElementById('vFastest').textContent = `${fmtNum(fRate)} cm/100d`;
    document.getElementById('vFastestSub').textContent = `${fName} (LOS)`;
    document.getElementById('vcFastest').hidden = false;
    shown++;
  }
  const areaVal = vs.area_km2_lt_minus5cm ?? vs.area_gt5_km2;
  if (typeof areaVal === 'number' && Number.isFinite(areaVal)){
    document.getElementById('vArea').textContent = `${fmtInt(areaVal)} km²`;
    document.getElementById('vcArea').hidden = false;
    shown++;
  }
  const pplVal = vs.people_on_sinking_ground ?? vs.people_exposed;
  if (typeof pplVal === 'number' && Number.isFinite(pplVal)){
    document.getElementById('vPeople').textContent = fmtInt(pplVal);
    document.getElementById('vcPeople').hidden = false;
    shown++;
  }
  if (shown > 0) document.getElementById('vitalBar').hidden = false;
}

async function initDataBox(){
  const box = document.getElementById('atlasDataLinks');
  if (!box) return;
  const hasExports = Boolean(atlasData?.exports || location.hostname.endsWith('github.io'));
  if (hasExports){
    box.insertAdjacentHTML('afterbegin', `<a href="${ROOT}data/global/atlas.geojson" download>atlas.geojson</a>`);
    box.insertAdjacentHTML('afterbegin', `<a href="${ROOT}data/global/atlas.csv" download>atlas.csv</a>`);
  }
}

function startTour(){
  const top5 = sortedRegions.slice(0, 5);
  if (!top5.length) return;
  if (tourTimer){ stopTour(); return; }
  const btn = document.getElementById('tourBtn');
  const cap = document.getElementById('tourCaption');
  if (btn){ btn.classList.add('is-playing'); btn.textContent = 'Stop tour'; }
  tourIdx = 0;
  const step = () => {
    const r = top5[tourIdx % top5.length];
    selectRegion(r.id, true, false);
    if (cap){
      const lbl = isIndicative(r) ? 'indicative only' : (r.confidence || 'medium');
      cap.innerHTML = `<b>#${tourIdx % top5.length + 1} · ${esc(r.name)}</b><span>${esc(fmtNum(r.rate_cm_per_100d))} cm/100d (LOS) · ${esc(lbl)}</span>`;
      cap.hidden = false;
    }
    tourIdx++;
  };
  step();
  tourTimer = setInterval(step, 6000);
}

function buildPointsSvg(ptsList, compareList, nameA, nameB){
  const pickP01 = pts => Array.isArray(pts) ? (pts.find(p => p.id === 'p01') || pts[0]) : null;
  const pA = pickP01(ptsList);
  if (!pA || !Array.isArray(pA.disp_cm) || !pA.disp_cm.length) return '';
  const pB = compareList ? pickP01(compareList) : null;
  const valsA = pA.disp_cm.map(Number).filter(Number.isFinite);
  const valsB = (pB && Array.isArray(pB.disp_cm)) ? pB.disp_cm.map(Number).filter(Number.isFinite) : [];
  if (!valsA.length) return '';

  const W = 340, H = 122, padL = 36, padR = 10, padT = 10, padB = 22;
  const plotW = W - padL - padR, plotH = H - padT - padB;
  const sigmas = valsA.map((_, i) => 0.4 * Math.sqrt(i));
  const allY = [0, ...valsA.map((v, i) => v - 2 * sigmas[i]), ...valsA.map((v, i) => v + 2 * sigmas[i]), ...valsB];
  let yMin = Math.min(...allY), yMax = Math.max(...allY);
  if (yMax - yMin < 1) { yMin -= 0.5; yMax += 0.5; }
  const yPad = (yMax - yMin) * 0.08;
  yMin -= yPad; yMax += yPad;
  const toX = (i, n) => padL + (n <= 1 ? plotW / 2 : (i / (n - 1)) * plotW);
  const toY = v => padT + ((yMax - v) / (yMax - yMin)) * plotH;

  const upper = valsA.map((v, i) => `${toX(i, valsA.length).toFixed(1)},${toY(v + 2 * sigmas[i]).toFixed(1)}`);
  const lower = valsA.map((v, i) => `${toX(i, valsA.length).toFixed(1)},${toY(v - 2 * sigmas[i]).toFixed(1)}`).reverse();
  const polyA = upper.concat(lower).join(' ');
  const lineA = valsA.map((v, i) => `${toX(i, valsA.length).toFixed(1)},${toY(v).toFixed(1)}`).join(' ');
  const lineB = valsB.length ? valsB.map((v, i) => `${toX(i, valsB.length).toFixed(1)},${toY(v).toFixed(1)}`).join(' ') : '';
  const y0 = toY(0).toFixed(1);
  const d0 = pA.dates?.[0] ? fmtShort(pA.dates[0]) : '';
  const d1 = pA.dates?.[pA.dates.length - 1] ? fmtShort(pA.dates[pA.dates.length - 1]) : '';

  return `<svg class="atlas-chart-svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="Time series at peak point ${esc(pA.name || pA.id)}">
    <line x1="${padL}" y1="${y0}" x2="${W - padR}" y2="${y0}" stroke="#cbd5e1" stroke-dasharray="3 3"/>
    ${!pB ? `<polygon points="${polyA}" fill="rgba(11,61,145,0.14)"/>` : ''}
    <polyline fill="none" stroke="#c8321f" stroke-width="2" points="${lineA}"/>
    ${lineB ? `<polyline fill="none" stroke="#0b3d91" stroke-width="2" points="${lineB}"/>` : ''}
    ${valsA.map((v, i) => `<circle cx="${toX(i, valsA.length).toFixed(1)}" cy="${toY(v).toFixed(1)}" r="2.5" fill="#c8321f"/>`).join('')}
    <text x="${padL - 4}" y="${padT + 8}" text-anchor="end" font-size="9" fill="#64748b" font-family="monospace">${yMax.toFixed(1)}</text>
    <text x="${padL - 4}" y="${H - padB}" text-anchor="end" font-size="9" fill="#64748b" font-family="monospace">${yMin.toFixed(1)}</text>
    <text x="${padL}" y="${H - 5}" text-anchor="start" font-size="9" fill="#64748b">${esc(d0)}</text>
    <text x="${W - padR}" y="${H - 5}" text-anchor="end" font-size="9" fill="#64748b">${esc(d1)}</text>
    ${pB ? `<text x="${padL + 4}" y="${padT + 9}" font-size="9" fill="#c8321f">${esc(nameA)}</text><text x="${padL + 4}" y="${padT + 20}" font-size="9" fill="#0b3d91">${esc(nameB)}</text>` : ''}
  </svg>`;
}

function buildGeoJson(regions){
  return {
    type: 'FeatureCollection',
    features: regions
      .filter(r => typeof r.lon === 'number' && typeof r.lat === 'number' && Number.isFinite(r.lon) && Number.isFinite(r.lat))
      .map(r => ({
        type: 'Feature',
        properties: {
          id: r.id,
          name: r.name,
          rate: r.rate_cm_per_100d ?? 0,
          color: rateColor(r.rate_cm_per_100d),
          confColor: confColor(r),
          indicative: isIndicative(r)
        },
        geometry: {type: 'Point', coordinates: [r.lon, r.lat]}
      }))
  };
}

function renderListAndMap(){
  const q = (document.getElementById('atlasSearch')?.value || '').trim().toLowerCase();
  const cf = document.getElementById('atlasConfFilter')?.value || 'all';
  const ctry = document.getElementById('atlasCountryFilter')?.value || 'all';

  filteredRegions = sortedRegions.filter(r => {
    if (q && !`${r.name} ${r.country || ''} ${r.id}`.toLowerCase().includes(q)) return false;
    if (cf === 'reliable' && isIndicative(r)) return false;
    if (cf === 'indicative' && !isIndicative(r)) return false;
    if (ctry !== 'all' && (r.country || '') !== ctry) return false;
    return true;
  });

  const listEl = document.getElementById('atlasList');
  listEl.innerHTML = filteredRegions.length ? filteredRegions.map(r => {
    const val = unitMode === 'vert' ? r.max_cm_vertical_est : r.rate_cm_per_100d;
    const unit = unitMode === 'vert' ? 'cm vert (est.)' : 'cm/100d';
    const rateTxt = (typeof val === 'number' && Number.isFinite(val)) ? `${fmtNum(val)} ${unit}` : 'no data';
    const indCls = isIndicative(r) ? ' is-indicative' : '';
    const actCls = r.id === activeId ? ' is-active' : '';
    const updBadge = /recomputed/i.test(r.note || '') ? ' <span class="cbadge updated">Updated</span>' : '';
    return `<button type="button" class="atlas-item${indCls}${actCls}" data-id="${esc(r.id)}">
      <span class="ai-left"><span class="ai-name">${r.rank ? '#' + r.rank + ' · ' : ''}${esc(r.name)}</span><span class="ai-sub">${r.country ? esc(r.country) + ' · ' : ''}${confBadge(r)}${updBadge}</span></span>
      <span class="ai-right"><span class="ai-rate" style="color:${rateColor(r.rate_cm_per_100d)}">${esc(rateTxt)}</span></span>
    </button>`;
  }).join('') : '<p class="small">No regions match this filter.</p>';

  listEl.querySelectorAll('.atlas-item').forEach(btn => {
    btn.addEventListener('click', () => { stopTour(); selectRegion(btn.dataset.id, true, true); });
  });

  if (map && mapReady && map.getSource('atlas-pts')){
    map.getSource('atlas-pts').setData(buildGeoJson(filteredRegions));
  }
}

async function renderCompare(){
  const aId = document.getElementById('cmpA')?.value;
  const bId = document.getElementById('cmpB')?.value;
  const body = document.getElementById('cmpBody');
  if (!body || !aId || !bId) return;
  const rA = sortedRegions.find(r => r.id === aId);
  const rB = sortedRegions.find(r => r.id === bId);
  if (!rA || !rB) return;
  const baseA = rA.path ? (rA.path.endsWith('/') ? rA.path : rA.path + '/') : `data/global/${rA.id}/`;
  const baseB = rB.path ? (rB.path.endsWith('/') ? rB.path : rB.path + '/') : `data/global/${rB.id}/`;
  const [ptsA, ptsB] = await Promise.all([J(baseA + 'points.json'), J(baseB + 'points.json')]);
  const svg = buildPointsSvg(ptsA, ptsB, rA.name, rB.name);
  body.innerHTML = `
    <div class="cmp-grid">
      <div class="cmp-col"><b>${esc(rA.name)}</b>Rate: ${esc(fmtUnit(rA.rate_cm_per_100d, 'cm/100d'))}<br>Max LOS: ${esc(fmtUnit(rA.max_cm_los, 'cm'))}<br>Vert (est.): ${esc(fmtUnit(rA.max_cm_vertical_est, 'cm'))}<br>${confBadge(rA)}</div>
      <div class="cmp-col"><b>${esc(rB.name)}</b>Rate: ${esc(fmtUnit(rB.rate_cm_per_100d, 'cm/100d'))}<br>Max LOS: ${esc(fmtUnit(rB.max_cm_los, 'cm'))}<br>Vert (est.): ${esc(fmtUnit(rB.max_cm_vertical_est, 'cm'))}<br>${confBadge(rB)}</div>
    </div>
    ${svg ? `<div class="atlas-chart-box"><div class="atlas-chart-hdr"><span>Peak point (p01) overlay (cm, LOS)</span></div>${svg}</div>` : ''}
  `;
}

async function loadGnssLayer(){
  const val = await J('data/central_valley/validation.json');
  if (!Array.isArray(val) || !map || !mapReady) return;
  const fc = {
    type: 'FeatureCollection',
    features: val
      .filter(s => typeof s.lon === 'number' && typeof s.lat === 'number')
      .map(s => ({
        type: 'Feature',
        properties: {
          station: s.station,
          corr: s.corr,
          rmse_cm: s.rmse_cm
        },
        geometry: {type: 'Point', coordinates: [s.lon, s.lat]}
      }))
  };
  map.addSource('cv-gnss', {type: 'geojson', data: fc});
  map.addLayer({
    id: 'cv-gnss',
    type: 'circle',
    source: 'cv-gnss',
    minzoom: 4,
    paint: {
      'circle-radius': 5.5,
      'circle-color': '#10b981',
      'circle-stroke-color': '#064e3b',
      'circle-stroke-width': 1.8
    }
  });
  map.on('click', 'cv-gnss', e => {
    const f = e.features?.[0];
    if (!f) return;
    const p = f.properties;
    new maplibregl.Popup({closeButton: true})
      .setLngLat(f.geometry.coordinates)
      .setHTML(`<div style="font-size:12px"><b>GPS station ${esc(p.station)}</b><br>r = ${Number(p.corr).toFixed(2)} · RMSE = ${Number(p.rmse_cm).toFixed(2)} cm<br><a href="https://geodesy.unr.edu/" target="_blank" rel="noopener">Nevada Geodetic Lab</a></div>`)
      .addTo(map);
  });
  map.on('mouseenter', 'cv-gnss', () => { map.getCanvas().style.cursor = 'pointer'; });
  map.on('mouseleave', 'cv-gnss', () => { map.getCanvas().style.cursor = ''; });
}

async function initAtlas(){
  initVitalSigns();
  await initBulletins();
  const [ad, qf, dt, rb, op, ex] = await Promise.all([
    J('data/global/atlas.json'),
    J('data/global/qc_flags.json'),
    J('data/global/detectability.json'),
    J('data/global/robustness.json'),
    J('data/global/opera_check.json'),
    J('data/global/exposure_atlas.json')
  ]);
  atlasData = ad;
  qcFlags = qf;
  if (Array.isArray(dt?.cities)) dt.cities.forEach(c => detMap.set(c.id, c));
  if (Array.isArray(rb?.cities)) rb.cities.forEach(c => robMap.set(c.id, c));
  if (Array.isArray(op)) op.forEach(c => operaMap.set(c.id, c));
  if (Array.isArray(ex?.cities)) ex.cities.forEach(c => expMap.set(c.id, c));
  initDataBox();
  if (!atlasData || !Array.isArray(atlasData.regions)){
    document.getElementById('atlasList').innerHTML = '<p class="small">Could not load data/global/atlas.json.</p>';
    return;
  }
  sortedRegions = atlasData.regions
    .slice()
    .sort((a, b) => (a.rate_cm_per_100d_common ?? a.rate_cm_per_100d ?? 999) - (b.rate_cm_per_100d_common ?? b.rate_cm_per_100d ?? 999));

  document.getElementById('stTotal').textContent = atlasData.n_regions ?? sortedRegions.length;
  document.getElementById('stRel').textContent = atlasData.n_reliable ?? sortedRegions.filter(r => !isIndicative(r)).length;
  document.getElementById('stInd').textContent = atlasData.n_indicative ?? sortedRegions.filter(r => isIndicative(r)).length;

  const countries = [...new Set(sortedRegions.map(r => r.country).filter(Boolean))].sort();
  const cSel = document.getElementById('atlasCountryFilter');
  if (cSel) cSel.innerHTML = '<option value="all">All countries</option>' + countries.map(c => `<option value="${esc(c)}">${esc(c)}</option>`).join('');

  const opts = sortedRegions.map(r => `<option value="${esc(r.id)}">${esc(r.name)}</option>`).join('');
  const cmpA = document.getElementById('cmpA');
  const cmpB = document.getElementById('cmpB');
  if (cmpA && cmpB){
    cmpA.innerHTML = opts;
    cmpB.innerHTML = opts;
    if (sortedRegions[1]) cmpB.value = sortedRegions[1].id;
    cmpA.addEventListener('change', renderCompare);
    cmpB.addEventListener('change', renderCompare);
  }

  document.getElementById('atlasSearch')?.addEventListener('input', renderListAndMap);
  document.getElementById('atlasConfFilter')?.addEventListener('change', renderListAndMap);
  document.getElementById('atlasCountryFilter')?.addEventListener('change', renderListAndMap);
  document.getElementById('unitToggle')?.addEventListener('click', e => {
    unitMode = unitMode === 'los' ? 'vert' : 'los';
    e.currentTarget.setAttribute('aria-pressed', String(unitMode === 'vert'));
    e.currentTarget.textContent = unitMode === 'vert' ? 'Values: Vertical (est.)' : 'Values: LOS';
    renderListAndMap();
    if (activeId) selectRegion(activeId, false, false);
  });
  document.getElementById('compareBtn')?.addEventListener('click', e => {
    const box = document.getElementById('compareBox');
    const open = box.hidden;
    box.hidden = !open;
    e.currentTarget.setAttribute('aria-expanded', String(open));
    if (open){
      if (activeId && cmpA) cmpA.value = activeId;
      renderCompare();
    }
  });
  document.getElementById('compareClose')?.addEventListener('click', () => {
    document.getElementById('compareBox').hidden = true;
    document.getElementById('compareBtn')?.setAttribute('aria-expanded', 'false');
  });

  document.querySelectorAll('#atlasLayers .al-btn').forEach(btn => {
    btn.addEventListener('click', () => applyLayer(btn.dataset.layer));
  });
  document.getElementById('tourBtn').addEventListener('click', startTour);

  if (typeof maplibregl !== 'undefined'){
    map = new maplibregl.Map({
      container: 'atlasMap',
      style: STYLE,
      center: [25, 22],
      zoom: 1.5,
      attributionControl: {compact: true},
      cooperativeGestures: true,
      fadeDuration: 0
    });
    map.addControl(new maplibregl.NavigationControl({showCompass: false}), 'top-left');

    map.on('style.load', () => {
      try{ map.setProjection({type: 'globe'}); }catch(e){}
    });

    if (!navigator.onLine) document.getElementById('offlinePill').hidden = false;
    map.on('error', e => {
      if (e && e.sourceId === 'sat') document.getElementById('offlinePill').hidden = false;
    });

    map.on('load', () => {
      mapReady = true;
      map.addSource('atlas-pts', {type: 'geojson', data: buildGeoJson(filteredRegions.length ? filteredRegions : sortedRegions)});
      map.addLayer({
        id: 'atlas-pts',
        type: 'circle',
        source: 'atlas-pts',
        paint: {
          'circle-radius': ['interpolate', ['linear'], ['abs', ['get', 'rate']], 0, 6, 10, 13],
          'circle-color': ['get', 'color'],
          'circle-stroke-color': '#ffffff',
          'circle-stroke-width': 2,
          'circle-opacity': ['case', ['get', 'indicative'], 0.55, 0.95]
        }
      });
      map.on('click', 'atlas-pts', e => {
        const f = e.features?.[0];
        if (f?.properties?.id){ stopTour(); selectRegion(f.properties.id, true, true); }
      });
      map.on('mouseenter', 'atlas-pts', () => { map.getCanvas().style.cursor = 'pointer'; });
      map.on('mouseleave', 'atlas-pts', () => { map.getCanvas().style.cursor = ''; });
      loadGnssLayer();
      if (activeLayer === 'disp' && animDates.length) setMapOverlay(`${activeBase}disp/${animDates[animIdx]}.png`, activeBboxCoords);
      else if (activeLayer === 'sigma') setMapOverlay(activeSigmaUrl, activeBboxCoords);
    });
  }

  renderListAndMap();

  window.addEventListener('hashchange', () => {
    const id = location.hash ? location.hash.slice(1) : '';
    if (id && id !== activeId && sortedRegions.some(r => r.id === id)) selectRegion(id, true, false);
  });

  const hashId = location.hash ? location.hash.slice(1) : '';
  const initial = sortedRegions.find(r => r.id === hashId) || sortedRegions[0];
  if (initial) selectRegion(initial.id, Boolean(hashId), false);
  renderTables(sortedRegions);
}

function renderTables(regions){
  const rel = regions.filter(r => !isIndicative(r));
  const ind = regions.filter(r => isIndicative(r));
  const fill = (id, rows) => {
    const tb = document.querySelector(`#${id} tbody`);
    if (!tb) return;
    tb.innerHTML = rows.length ? rows.map((r, i) => {
      const pTxt = Array.isArray(r.period) && r.period.length === 2 ? `${fmtShort(r.period[0])} – ${fmtShort(r.period[1])}` : '—';
      const rateVal = r.rate_cm_per_100d_common ?? r.rate_cm_per_100d;
      const ci = Array.isArray(r.rate_ci_cm_per_100d) && r.rate_ci_cm_per_100d.length === 2 ? r.rate_ci_cm_per_100d : null;
      const ciHtml = ci ? `<div class="small" style="font-size:.74rem;color:var(--dim)">[${esc(fmtNum(ci[0]))}, ${esc(fmtNum(ci[1]))}]</div>` : '';
      return `<tr data-id="${esc(r.id)}"><td>${i + 1}</td><td><b>${esc(r.name)}</b>${r.country ? ' · ' + esc(r.country) : ''}</td><td class="mono">${esc(fmtNum(rateVal))}${ciHtml}</td><td class="mono">${esc(fmtNum(r.max_cm_los))} cm</td><td>${esc(pTxt)}</td><td>${confBadge(r)}</td></tr>`;
    }).join('') : '<tr><td colspan="6" class="small">None in this class.</td></tr>';
    tb.querySelectorAll('tr[data-id]').forEach(tr => tr.addEventListener('click', () => {
      stopTour();
      selectRegion(tr.dataset.id, true, true);
      window.scrollTo({top: 0, behavior: 'smooth'});
    }));
  };
  fill('tblReliable', rel);
  fill('tblIndicative', ind);
  const qcLine = document.getElementById('atlasQcSummary');
  if (qcLine && qcFlags && qcFlags.flags){
    const nFlagged = Object.keys(qcFlags.flags).length;
    if (nFlagged > 0){
      qcLine.innerHTML = `Quality control: <b>${nFlagged}</b> regions flagged (time-series check) &mdash; <a href="${ROOT}docs/story/atlas_top5_check.md" target="_blank" rel="noopener">see method</a>`;
      qcLine.hidden = false;
    }
  }
  const chList = document.getElementById('atlasChangelogList');
  if (chList && !chList.dataset.loaded){
    chList.dataset.loaded = '1';
    fetch(ROOT + 'data/global/atlas_changelog.json').then(r => r.ok ? r.json() : null).then(ch => {
      const entries = Array.isArray(ch?.entries) ? ch.entries.slice(0, 10) : [];
      if (!entries.length){ chList.innerHTML = '<li>No changelog entries available.</li>'; return; }
      chList.innerHTML = entries.map(e => {
        const ts = esc((e.timestamp || '').replace('T', ' ').replace('Z', ' UTC'));
        const parts = [];
        if (e.n_regions) parts.push(`${e.n_regions} regions`);
        if (Array.isArray(e.added) && e.added.length) parts.push(`added: ${esc(e.added.join(', '))}`);
        if (Array.isArray(e.removed) && e.removed.length) parts.push(`removed: ${esc(e.removed.join(', '))}`);
        if (Array.isArray(e.value_changes) && e.value_changes.length) parts.push(e.value_changes.map(v => `${esc(v.id)} ${v.old_cm}→${v.new_cm} cm`).join('; '));
        if (e.note) parts.push(esc(e.note));
        return `<li><b>${ts}</b> — ${parts.join(' · ') || 'updated'}</li>`;
      }).join('');
    }).catch(() => { chList.innerHTML = '<li>Could not load atlas_changelog.json.</li>'; });
  }
}

async function selectRegion(id, fly, updateHash){
  const r = atlasData?.regions?.find(x => x.id === id);
  if (!r) return;
  stopAnim();
  activeId = id;
  if (updateHash && location.hash !== '#' + id){
    try{ history.replaceState(null, '', '#' + id); }catch(e){}
  }
  document.querySelectorAll('.atlas-item').forEach(el => el.classList.toggle('is-active', el.dataset.id === id));
  if (fly && map && typeof r.lon === 'number' && typeof r.lat === 'number'){
    map.flyTo({center: [r.lon, r.lat], zoom: 5.5, duration: 1200});
  }

  const base = r.path ? (r.path.endsWith('/') ? r.path : r.path + '/') : `data/global/${r.id}/`;
  activeBase = base;
  const [meta, pts, valNote] = await Promise.all([
    J(base + 'meta.json'),
    J(base + 'points.json'),
    KNOWN_VALNOTE.has(r.id) ? J(base + 'validation_note.json') : Promise.resolve(null)
  ]);
  const hasBul = Boolean(r.bulletin || bulletinIds.has(r.id));
  const hasCard = Boolean(r.city_card || KNOWN_CARDS.has(r.id));

  activeBboxCoords = bboxToCoords(meta?.bbox);
  activeSigmaUrl = r.sigma_png ? r.sigma_png : (KNOWN_SIGMA.has(r.id) ? ((r.id === 'central_valley' || r.id === 'karapinar') ? `data/${r.id}/uncertainty/sigma_cm.png` : `data/global/${r.id}/uncertainty/sigma_cm.png`) : null);
  animDates = Array.isArray(meta?.dates) ? meta.dates : [];
  animIdx = animDates.length ? animDates.length - 1 : 0;

  const periodTxt = Array.isArray(r.period) && r.period.length === 2
    ? `${fmtShort(r.period[0])} – ${fmtDate(r.period[1])} (${r.days ?? '—'} days)`
    : '—';
  const validTxt = (typeof r.valid_fraction === 'number' && Number.isFinite(r.valid_fraction))
    ? `${(r.valid_fraction * 100).toFixed(1)}%`
    : '—';
  const refTxt = Array.isArray(r.ref_range_cm) && r.ref_range_cm.length === 2
    ? `${fmtNum(Math.min(...r.ref_range_cm))} to ${fmtNum(Math.max(...r.ref_range_cm))} cm`
    : '—';
  const lastDate = animDates.length ? animDates[animIdx] : null;
  const pngPath = lastDate ? `${base}disp/${lastDate}.png` : null;
  const srcTxt = meta?.source || 'NASA-ISRO NISAR L2 GUNW (provisional) via ASF DAAC';
  const chartSvg = buildPointsSvg(pts, null, r.name, null);

  const extraCards = [];
  const detInfo = detMap.get(r.id);
  const detFlag = r.detectable !== undefined && r.detectable !== null ? r.detectable : detInfo?.detectable;
  if (detFlag !== undefined && detFlag !== null){
    const snrTxt = (typeof detInfo?.snr === 'number' && Number.isFinite(detInfo.snr)) ? ` (SNR ${detInfo.snr.toFixed(1)})` : '';
    const detVal = typeof detFlag === 'boolean' ? ((detFlag ? 'Yes' : 'No') + snrTxt) : String(detFlag);
    extraCards.push(`<div><dt>Detectable</dt><dd>${esc(detVal)}</dd></div>`);
  }
  const robInfo = robMap.get(r.id);
  const robSpread = (typeof r.robustness_spread === 'number' && Number.isFinite(r.robustness_spread)) ? r.robustness_spread : robInfo?.spread_cm;
  if (typeof robSpread === 'number' && Number.isFinite(robSpread)){
    const rngTxt = (typeof robInfo?.min_rate_cm_per_100d === 'number' && typeof robInfo?.max_rate_cm_per_100d === 'number')
      ? `${fmtNum(robInfo.min_rate_cm_per_100d)} to ${fmtNum(robInfo.max_rate_cm_per_100d)} cm/100d`
      : fmtUnit(robSpread, 'cm');
    extraCards.push(`<div><dt>Robustness</dt><dd style="font-size:.76rem">${esc(rngTxt)}</dd></div>`);
  }
  const expInfo = expMap.get(r.id);
  const expPop = (typeof r.people_exposed === 'number' && Number.isFinite(r.people_exposed)) ? r.people_exposed : expInfo?.people_lt_minus5cm;
  if (typeof expPop === 'number' && Number.isFinite(expPop)){
    extraCards.push(`<div><dt>People (&lt;&minus;5 cm)</dt><dd>${esc(fmtInt(expPop))}</dd></div>`);
  }
  const opInfo = operaMap.get(r.id);
  if (r.opera_check !== undefined && r.opera_check !== null){
    const opTxt = typeof r.opera_check === 'object' ? (r.opera_check.summary || r.opera_check.status || JSON.stringify(r.opera_check)) : String(r.opera_check);
    extraCards.push(`<div><dt>OPERA cross-check</dt><dd style="font-size:.76rem">${esc(opTxt)}</dd></div>`);
  } else if (opInfo){
    extraCards.push(`<div><dt>OPERA DISP-S1</dt><dd style="font-size:.76rem">r=${opInfo.r.toFixed(2)}, RMSE ${opInfo.rmse_cm.toFixed(1)} cm</dd></div>`);
  }

  const mainVal = unitMode === 'vert' ? r.max_cm_vertical_est : r.max_cm_los;
  const mainLbl = unitMode === 'vert' ? 'Max vertical (est.)' : 'Max LOS';

  const isRecomputed = /recomputed/i.test(r.note || '');
  const qcEntry = qcFlags?.flags?.[r.id];
  const qcTags = Array.isArray(qcEntry?.flags) ? qcEntry.flags.map(f => `<span class="qc-tag">${esc(f)}</span>`).join('') : '';
  const qcDetailTxt = r.note || qcEntry?.detail || '';
  const qcCleanTxt = (typeof qcEntry?.headline_without_flagged_steps_cm === 'number' && Number.isFinite(qcEntry.headline_without_flagged_steps_cm))
    ? `<br>Without flagged step(s): <b>${esc(fmtUnit(qcEntry.headline_without_flagged_steps_cm, 'cm'))}</b>` : '';
  const qcBoxHtml = (qcEntry || /^QC:/i.test(r.note || ''))
    ? `<div class="atlas-qc-box">${qcTags}<b>Time-series QC:</b> ${esc(qcDetailTxt)}${qcCleanTxt}</div>` : '';
  const valBoxHtml = valNote?.agreement_note
    ? `<div class="atlas-val-box"><b>Validation note${valNote.literature_vertical_cm_per_yr ? ` (lit. ${esc(valNote.literature_vertical_cm_per_yr)} cm/yr)` : ''}:</b> ${esc(valNote.agreement_note)}</div>` : '';
  const detail = document.getElementById('atlasDetail');
  detail.hidden = false;
  detail.innerHTML = `
    <h2>${esc(r.name)}${r.country ? ` <small class="small">(${esc(r.country)})</small>` : ''}</h2>
    <p style="margin:0 0 8px">${confBadge(r)} <span class="qbadge provisional">${esc((r.quality || 'provisional').toUpperCase())}</span>${isRecomputed ? ' <span class="cbadge updated">Updated</span>' : ''}</p>
    ${isRecomputed ? `<p class="atlas-updated"><b>Updated:</b> Recomputed with off-basin reference — old value &minus;3.5 cm</p>` : ''}
    ${qcBoxHtml}
    ${valBoxHtml}
    <dl class="atlas-kv">
      <div><dt>Rate (LOS)</dt><dd>${esc(fmtUnit(r.rate_cm_per_100d, 'cm/100d'))}</dd></div>
      <div><dt>${esc(mainLbl)}</dt><dd>${esc(fmtUnit(mainVal, 'cm'))}</dd></div>
      <div><dt>Vertical (est.)</dt><dd>${esc(fmtUnit(r.max_cm_vertical_est, 'cm'))}</dd></div>
      <div><dt>Yearly rate (est.)</dt><dd>${esc(fmtUnit(r.rate_cm_per_yr_estimate, 'cm/yr'))}</dd></div>
      <div><dt>Period</dt><dd style="font-size:.78rem">${esc(periodTxt)}</dd></div>
      <div><dt>Pairs / Valid px</dt><dd>${r.n_pairs ?? '—'} pairs · ${esc(validTxt)}</dd></div>
      <div><dt>2nd percentile (p2)</dt><dd>${esc(fmtUnit(r.p2_cm, 'cm'))}</dd></div>
      <div><dt>Ref. spread</dt><dd style="font-size:.78rem">${esc(refTxt)}</dd></div>
      ${extraCards.join('')}
    </dl>
    ${r.note ? `<p class="small">${esc(r.note)}</p>` : ''}
    <p class="atlas-src"><b>Source:</b> ${esc(srcTxt)}</p>
    ${chartSvg ? `<div class="atlas-chart-box"><div class="atlas-chart-hdr"><span>Peak point (p01) time series (cm, LOS)</span><span>&plusmn;2&sigma; band</span></div>${chartSvg}</div>` : ''}
    ${pngPath ? `<div class="atlas-player">
      <div class="atlas-player-hdr">
        <button type="button" class="atlas-play-btn" id="atlasPlayBtn">Play</button>
        <span class="atlas-date-lbl" id="atlasDateLbl">${esc(fmtDate(lastDate))}</span>
        <span class="qbadge provisional">PROVISIONAL</span>
      </div>
      <input type="range" class="atlas-slider" id="atlasSlider" min="0" max="${Math.max(0, animDates.length - 1)}" value="${animIdx}" aria-label="Time slider for cumulative displacement">
      <div class="atlas-png"><img id="atlasAnimImg" src="${ROOT + esc(pngPath)}" alt="Cumulative ground motion map for ${esc(r.name)}" loading="lazy"></div>
      <div class="atlas-cbar">
        <div class="atlas-cbar-grad"></div>
        <div class="atlas-cbar-lbls"><span>&minus;10 cm (sinking)</span><span>0 cm</span><span>+5 cm</span></div>
      </div>
    </div>` : ''}
    <div class="atlas-actions">
      ${hasBul ? `<a href="${ROOT}docs/bulletins/${esc(r.id)}.html" target="_blank" rel="noopener">Open bulletin →</a>` : ''}
      ${hasCard ? `<a href="${ROOT}docs/story/atlas_cities/${esc(r.id)}.md" target="_blank" rel="noopener">City card →</a>` : ''}
      ${(r.id === 'central_valley' || r.id === 'konya_plain' || r.id === 'karapinar') ? `<a href="${ROOT}game/?basin=${r.id === 'central_valley' ? 'tulare' : 'konya'}">Manage this valley in the simulator →</a>` : ''}
      <a href="explorer.html#${esc(r.id)}">Open in Explorer →</a>
    </div>
  `;

  const playBtn = document.getElementById('atlasPlayBtn');
  const slider = document.getElementById('atlasSlider');
  if (playBtn) playBtn.addEventListener('click', toggleAnim);
  if (slider) slider.addEventListener('input', e => { stopAnim(); setFrame(Number(e.target.value)); });

  if (activeLayer === 'sigma') setMapOverlay(activeSigmaUrl, activeBboxCoords);
  else if (activeLayer === 'disp' && pngPath) setMapOverlay(pngPath, activeBboxCoords);
  else setMapOverlay(null, null);

  try{ window.dispatchEvent(new CustomEvent('atlas:select', {detail: {id, region: r}})); }catch(e){}
}

window.atlasSelect = id => selectRegion(id, true, true);
initAtlas();
