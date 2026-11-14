// NISAR Pulse — Global Subsidence Atlas 2026 (Atlas Final v2)
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
async function okHead(p){ try{ const r = await fetch(ROOT + p, {method: 'HEAD'}); return r.ok; }catch(e){ return false; } }

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

function confBadge(r){
  const c = (r.confidence || 'low').toLowerCase();
  const lbl = (r.indicative_only || c === 'low') ? `${c} · indicative only` : c;
  return `<span class="cbadge ${esc(c)}">${esc(lbl)}</span>`;
}

function bboxToCoords(bbox){
  if (!Array.isArray(bbox) || bbox.length !== 4) return null;
  const [w, s, e, n] = bbox;
  if (![w, s, e, n].every(x => typeof x === 'number' && Number.isFinite(x))) return null;
  return [[w, n], [e, n], [e, s], [w, s]];
}

let map, mapReady = false, atlasData = null, sortedRegions = [], activeId = null;
let activeLayer = 'disp';
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
  if (vs.fastest_place && typeof vs.fastest_rate_cm_per_100d === 'number' && Number.isFinite(vs.fastest_rate_cm_per_100d)){
    document.getElementById('vFastest').textContent = `${fmtNum(vs.fastest_rate_cm_per_100d)} cm/100d`;
    document.getElementById('vFastestSub').textContent = `${vs.fastest_place} (LOS)`;
    document.getElementById('vcFastest').hidden = false;
    shown++;
  }
  if (typeof vs.area_gt5_km2 === 'number' && Number.isFinite(vs.area_gt5_km2)){
    document.getElementById('vArea').textContent = `${fmtInt(vs.area_gt5_km2)} km²`;
    document.getElementById('vcArea').hidden = false;
    shown++;
  }
  if (typeof vs.people_exposed === 'number' && Number.isFinite(vs.people_exposed)){
    document.getElementById('vPeople').textContent = fmtInt(vs.people_exposed);
    document.getElementById('vcPeople').hidden = false;
    shown++;
  }
  if (shown > 0) document.getElementById('vitalBar').hidden = false;
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
      const lbl = (r.indicative_only || (r.confidence || '').toLowerCase() === 'low') ? 'indicative only' : (r.confidence || 'medium');
      cap.innerHTML = `<b>#${tourIdx % top5.length + 1} · ${esc(r.name)}</b><span>${esc(fmtNum(r.rate_cm_per_100d))} cm/100d (LOS) · ${esc(lbl)}</span>`;
      cap.hidden = false;
    }
    tourIdx++;
  };
  step();
  tourTimer = setInterval(step, 6000);
}

async function initAtlas(){
  initVitalSigns();
  atlasData = await J('data/global/atlas.json');
  if (!atlasData || !Array.isArray(atlasData.regions)){
    document.getElementById('atlasList').innerHTML = '<p class="small">Could not load data/global/atlas.json.</p>';
    return;
  }
  sortedRegions = atlasData.regions
    .slice()
    .sort((a, b) => (a.rate_cm_per_100d ?? 999) - (b.rate_cm_per_100d ?? 999));

  document.getElementById('stTotal').textContent = atlasData.n_regions ?? sortedRegions.length;
  document.getElementById('stRel').textContent = atlasData.n_reliable ?? sortedRegions.filter(r => !r.indicative_only).length;
  document.getElementById('stInd').textContent = atlasData.n_indicative ?? sortedRegions.filter(r => r.indicative_only).length;

  const listEl = document.getElementById('atlasList');
  listEl.innerHTML = sortedRegions.map(r => {
    const rateTxt = (typeof r.rate_cm_per_100d === 'number' && Number.isFinite(r.rate_cm_per_100d))
      ? `${fmtNum(r.rate_cm_per_100d)} cm/100d`
      : 'no data';
    const indCls = (r.indicative_only || (r.confidence || '').toLowerCase() === 'low') ? ' is-indicative' : '';
    return `<button type="button" class="atlas-item${indCls}" data-id="${esc(r.id)}">
      <span class="ai-left"><span class="ai-name">${r.rank ? '#' + r.rank + ' · ' : ''}${esc(r.name)}</span><span class="ai-sub">${r.country ? esc(r.country) + ' · ' : ''}${confBadge(r)}</span></span>
      <span class="ai-right"><span class="ai-rate" style="color:${rateColor(r.rate_cm_per_100d)}">${esc(rateTxt)}</span></span>
    </button>`;
  }).join('');

  listEl.querySelectorAll('.atlas-item').forEach(btn => {
    btn.addEventListener('click', () => { stopTour(); selectRegion(btn.dataset.id, true, true); });
  });

  document.querySelectorAll('#atlasLayers .al-btn').forEach(btn => {
    btn.addEventListener('click', () => applyLayer(btn.dataset.layer));
  });
  document.getElementById('tourBtn').addEventListener('click', startTour);

  const geojson = {
    type: 'FeatureCollection',
    features: sortedRegions
      .filter(r => typeof r.lon === 'number' && typeof r.lat === 'number' && Number.isFinite(r.lon) && Number.isFinite(r.lat))
      .map(r => ({
        type: 'Feature',
        properties: {
          id: r.id,
          name: r.name,
          rate: r.rate_cm_per_100d ?? 0,
          color: rateColor(r.rate_cm_per_100d),
          confColor: confColor(r),
          indicative: Boolean(r.indicative_only || (r.confidence || '').toLowerCase() === 'low')
        },
        geometry: {type: 'Point', coordinates: [r.lon, r.lat]}
      }))
  };

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
      map.addSource('atlas-pts', {type: 'geojson', data: geojson});
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
      if (activeLayer === 'disp' && animDates.length) setMapOverlay(`${activeBase}disp/${animDates[animIdx]}.png`, activeBboxCoords);
      else if (activeLayer === 'sigma') setMapOverlay(activeSigmaUrl, activeBboxCoords);
    });
  }

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
  const rel = regions.filter(r => !r.indicative_only && (r.confidence || '').toLowerCase() !== 'low');
  const ind = regions.filter(r => r.indicative_only || (r.confidence || '').toLowerCase() === 'low');
  const fill = (id, rows) => {
    const tb = document.querySelector(`#${id} tbody`);
    if (!tb) return;
    tb.innerHTML = rows.length ? rows.map((r, i) => {
      const pTxt = Array.isArray(r.period) && r.period.length === 2 ? `${fmtShort(r.period[0])} – ${fmtShort(r.period[1])}` : '—';
      return `<tr data-id="${esc(r.id)}"><td>${i + 1}</td><td><b>${esc(r.name)}</b>${r.country ? ' · ' + esc(r.country) : ''}</td><td class="mono">${esc(fmtNum(r.rate_cm_per_100d))}</td><td class="mono">${esc(fmtNum(r.max_cm_los))} cm</td><td>${esc(pTxt)}</td><td>${confBadge(r)}</td></tr>`;
    }).join('') : '<tr><td colspan="6" class="small">None in this class.</td></tr>';
    tb.querySelectorAll('tr[data-id]').forEach(tr => tr.addEventListener('click', () => {
      stopTour();
      selectRegion(tr.dataset.id, true, true);
      window.scrollTo({top: 0, behavior: 'smooth'});
    }));
  };
  fill('tblReliable', rel);
  fill('tblIndicative', ind);
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
  const sigmaCand1 = `${base}uncertainty/sigma_cm.png`;
  const sigmaCand2 = `data/global/${r.id}/uncertainty/sigma_cm.png`;
  const [meta, hasBul, hasCard, hasSig1, hasSig2] = await Promise.all([
    J(base + 'meta.json'),
    okHead(`docs/bulletins/${r.id}.html`),
    okHead(`docs/story/atlas_cities/${r.id}.md`),
    okHead(sigmaCand1),
    sigmaCand1 === sigmaCand2 ? Promise.resolve(false) : okHead(sigmaCand2)
  ]);

  activeBboxCoords = bboxToCoords(meta?.bbox);
  activeSigmaUrl = hasSig1 ? sigmaCand1 : (hasSig2 ? sigmaCand2 : null);
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

  const extraCards = [];
  if (r.detectable !== undefined && r.detectable !== null){
    const detVal = typeof r.detectable === 'boolean' ? (r.detectable ? 'Yes (above noise)' : 'No (below noise)') : String(r.detectable);
    extraCards.push(`<div><dt>Detectable</dt><dd>${esc(detVal)}</dd></div>`);
  }
  if (typeof r.robustness_spread === 'number' && Number.isFinite(r.robustness_spread)){
    extraCards.push(`<div><dt>Robustness spread</dt><dd>${esc(fmtUnit(r.robustness_spread, 'cm'))}</dd></div>`);
  }
  if (typeof r.people_exposed === 'number' && Number.isFinite(r.people_exposed)){
    extraCards.push(`<div><dt>People exposed</dt><dd>${esc(fmtInt(r.people_exposed))}</dd></div>`);
  }
  if (r.opera_check !== undefined && r.opera_check !== null){
    const opTxt = typeof r.opera_check === 'object' ? (r.opera_check.summary || r.opera_check.status || JSON.stringify(r.opera_check)) : String(r.opera_check);
    extraCards.push(`<div><dt>OPERA cross-check</dt><dd style="font-size:.76rem">${esc(opTxt)}</dd></div>`);
  }

  const detail = document.getElementById('atlasDetail');
  detail.hidden = false;
  detail.innerHTML = `
    <h2>${esc(r.name)}${r.country ? ` <small class="small">(${esc(r.country)})</small>` : ''}</h2>
    <p style="margin:0 0 8px">${confBadge(r)} <span class="qbadge provisional">${esc((r.quality || 'provisional').toUpperCase())}</span></p>
    <dl class="atlas-kv">
      <div><dt>Rate (LOS)</dt><dd>${esc(fmtUnit(r.rate_cm_per_100d, 'cm/100d'))}</dd></div>
      <div><dt>Max LOS</dt><dd>${esc(fmtUnit(r.max_cm_los, 'cm'))}</dd></div>
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
}

initAtlas();
