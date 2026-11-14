// NISAR Pulse — site logic. Reads files defined in rules/VERI_SOZLESMESI.md.
// Pages: site root = web/, data/ and game/ copied next to it. Local dev (/web/): ../data, ../game.
const LOCAL = location.pathname.includes('/web/');
const ROOT = LOCAL ? '../' : './';
const ESRI = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
const BADGE = {provisional:['provisional','PROVISIONAL'], 'beta-precal':['beta','PRE-CALIBRATION BETA'], mixed:['mixed','MIXED (incl. beta)'], preview:['preview','PREVIEW — not quantitative'], placeholder:['placeholder','PLACEHOLDER — layout test']};

async function getJSON(paths){
  for (const p of paths){ try{ const r = await fetch(p, {cache:'no-cache'}); if (r.ok) return {data: await r.json(), base: p.slice(0, p.lastIndexOf('/') + 1)}; }catch(e){} }
  return null;
}
async function exists(p){ try{ const r = await fetch(p, {method:'HEAD', cache:'no-cache'}); return r.ok; }catch(e){ return false; } }
function badge(q, note){
  const b = BADGE[q] || ['placeholder', (q || 'unknown').toUpperCase()];
  return `<span class="badge ${b[0]}">${b[1]}</span>${note ? `<small>${note}</small>` : ''}`;
}
function baseMap(el, center, zoom){
  return new maplibregl.Map({ container: el, center, zoom, attributionControl: {compact: true},
    style: { version: 8, sources: { sat: { type: 'raster', tiles: [ESRI], tileSize: 256, attribution: 'Imagery © Esri, Maxar, Earthstar Geographics' } },
             layers: [{ id: 'sat', type: 'raster', source: 'sat', paint: {'raster-brightness-max': 0.75} }] } });
}
const corners = ([w, s, e, n]) => [[w, n], [e, n], [e, s], [w, s]];

// Human-scale comparisons (standard sizes).
const SCALE = [[8.56, 'the width of a bank card'], [21.0, 'the short side of an A4 sheet'], [29.7, 'the long side of an A4 sheet'], [100, 'a metre stick']];
function humanScale(cm){ const a = Math.abs(cm); let best = SCALE[0]; for (const s of SCALE) if (Math.abs(s[0] - a) < Math.abs(best[0] - a)) best = s; return best[1]; }
const fmtDate = d => new Date(d + 'T00:00:00Z').toLocaleDateString('en-GB', {day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC'});

/* ---------- 1 · UK ---------- */
async function initUK(){
  const r = await getJSON([ROOT + 'data/uk/meta.json']);
  if (!r) return;
  const m = r.data, base = r.base;
  const opt = document.getElementById('ukOptical'), rad = document.getElementById('ukRadar');
  opt.src = base + `optical_${m.date}.jpg`; rad.src = base + `radar_${m.date}.png`;
  for (const id of ['ukOptical', 'ukRadarWrap', 'compareRange']) document.getElementById(id).hidden = false;
  document.querySelectorAll('.compare-label').forEach(e => e.hidden = false);
  document.getElementById('compareEmpty').hidden = true;
  document.getElementById('ukMeta').innerHTML = `${badge(m.quality || 'preview')} ${fmtDate(m.date)} · optical: ${m.optical_product || ''} · radar: NISAR GCOV quick-look`;
  const range = document.getElementById('compareRange'), top = document.getElementById('ukRadarWrap'), box = document.getElementById('compare');
  const upd = () => { top.style.clipPath = `inset(0 0 0 ${range.value}%)`; box.style.setProperty('--split', range.value + '%'); };
  range.addEventListener('input', upd); upd();
}

/* ---------- 2 · USA ---------- */
async function initUSA(){
  const r = await getJSON([ROOT + 'data/central_valley/meta.json', 'mock/central_valley/meta.json']);
  const map = baseMap('cvMap', [-119.6, 36.1], 7.6);
  if (!r){ document.getElementById('cvSentence').textContent = 'Data are being processed.'; return; }
  const m = r.data, base = r.base;
  document.getElementById('cvBadge').innerHTML = badge(m.quality, m.quality_note);
  document.getElementById('legMin').textContent = `${m.vmin} cm`; document.getElementById('legMax').textContent = `+${m.vmax} cm`;
  const slider = document.getElementById('cvSlider'), label = document.getElementById('cvDate');
  slider.max = m.dates.length - 1; slider.value = m.dates.length - 1;
  const pts = (await getJSON([base + 'points.json']))?.data || [];
  map.on('load', () => {
    map.addSource('disp', {type: 'image', url: base + `disp/${m.dates.at(-1)}.png`, coordinates: corners(m.bbox)});
    map.addLayer({id: 'disp', type: 'raster', source: 'disp', paint: {'raster-opacity': 0.8, 'raster-fade-duration': 0}});
    map.addSource('pts', {type: 'geojson', data: {type: 'FeatureCollection', features: pts.map(p => ({type: 'Feature', properties: {id: p.id}, geometry: {type: 'Point', coordinates: [p.lon, p.lat]}}))}});
    map.addLayer({id: 'pts', type: 'circle', source: 'pts', paint: {'circle-radius': 7, 'circle-color': '#fff', 'circle-stroke-color': '#000', 'circle-stroke-width': 2}});
    map.on('click', 'pts', e => select(pts.find(p => p.id === e.features[0].properties.id)));
    map.on('mouseenter', 'pts', () => map.getCanvas().style.cursor = 'pointer');
    map.on('mouseleave', 'pts', () => map.getCanvas().style.cursor = '');
    show(+slider.value);
    if (pts.length) select(pts[0]);
  });
  let shown = base + `disp/${m.dates.at(-1)}.png`;
  function show(i){
    label.textContent = fmtDate(m.dates[i]);
    const url = base + `disp/${m.dates[i]}.png`, s = map.getSource('disp');
    if (s && url !== shown){ shown = url; s.updateImage({url, coordinates: corners(m.bbox)}); }
  }
  slider.addEventListener('input', () => show(+slider.value));
  let timer = null; const btn = document.getElementById('cvPlay');
  btn.addEventListener('click', () => {
    if (timer){ clearInterval(timer); timer = null; btn.textContent = '▶'; return; }
    btn.textContent = '❚❚';
    timer = setInterval(() => { slider.value = (+slider.value + 1) % m.dates.length; show(+slider.value); }, 900);
  });
  let chart = null;
  function select(p){
    if (!p) return;
    const v = p.disp_cm.at(-1), months = Math.max(1, Math.round((new Date(p.dates.at(-1)) - new Date(p.dates[0])) / 2.63e9));
    const verb = v < 0 ? 'sank' : 'rose';
    const tag = m.quality === 'placeholder' ? ' <span class="badge placeholder">PLACEHOLDER</span>' : '';
    document.getElementById('cvSentence').innerHTML =
      `<b>${p.name}:</b> this spot ${verb} <b>${Math.abs(v).toFixed(1)} cm</b> between ${fmtDate(p.dates[0])} and ${fmtDate(p.dates.at(-1))} (${months} month${months > 1 ? 's' : ''}) — about ${humanScale(v)}.${tag}`;
    const data = {labels: p.dates.map(fmtDate), datasets: [{label: 'Ground motion (cm, line of sight)', data: p.disp_cm, borderColor: '#ff6b5a', backgroundColor: 'rgba(255,107,90,.15)', fill: true, tension: .25}]};
    if (chart){ chart.data = data; chart.update(); return; }
    chart = new Chart(document.getElementById('cvChart'), {type: 'line', data, options: {plugins: {legend: {labels: {color: '#93a3c0'}}}, scales: {x: {ticks: {color: '#93a3c0'}, grid: {color: '#1f2b44'}}, y: {ticks: {color: '#93a3c0'}, grid: {color: '#1f2b44'}, title: {display: true, text: 'cm', color: '#93a3c0'}}}}});
  }
}

/* ---------- 3 · KONYA ---------- */
async function initKonya(){
  const map = baseMap('kpMap', [33.55, 37.75], 9.2);
  const meta = await getJSON([ROOT + 'data/karapinar/meta.json']);
  const sk = await getJSON([ROOT + 'data/karapinar/sinkholes.geojson']);
  if (meta) document.getElementById('kpBadge').innerHTML = badge(meta.data.quality, meta.data.quality_note);
  map.on('load', () => {
    if (meta){
      const m = meta.data;
      map.addSource('kdisp', {type: 'image', url: meta.base + `disp/${m.dates.at(-1)}.png`, coordinates: corners(m.bbox)});
      map.addLayer({id: 'kdisp', type: 'raster', source: 'kdisp', paint: {'raster-opacity': 0.75}});
    }
    if (sk && sk.data.features?.length){
      document.getElementById('kpEmpty').hidden = true;
      map.addSource('sk', {type: 'geojson', data: sk.data});
      map.addLayer({id: 'sk', type: 'circle', source: 'sk', paint: {'circle-radius': 6, 'circle-color': '#ff6b5a', 'circle-stroke-color': '#fff', 'circle-stroke-width': 1.5}});
      document.getElementById('kpList').innerHTML = sk.data.features.slice(0, 12).map(f => {
        const p = f.properties; return `<li>${p.name}${p.year_formed ? ` (${p.year_formed})` : ''} — <a href="${p.source_url}" target="_blank" rel="noopener">source</a></li>`; }).join('');
      map.on('click', 'sk', e => { const p = e.features[0].properties;
        new maplibregl.Popup().setLngLat(e.lngLat).setHTML(`<b>${p.name}</b><br>${p.year_formed || ''}<br><a href="${p.source_url}" target="_blank" rel="noopener">${p.source_title || 'source'}</a>`).addTo(map); });
    }
  });
}

/* ---------- 5 · GAME ---------- */
async function initGame(){
  const url = ROOT + 'game/index.html';
  if (await exists(url)){
    const f = document.getElementById('gameFrame'); f.src = url; f.hidden = false; document.getElementById('gamePoster').hidden = true;
    document.getElementById('gameLink').href = url; document.getElementById('gameNote').hidden = true;
  } else { document.getElementById('gameLink').hidden = true; }
}

/* ---------- 0 · HERO media (AI-labelled) ---------- */
async function initHero(){
  const url = 'assets/hero.mp4';
  if (await exists(url)){ const v = document.getElementById('heroVideo'); v.src = url; v.hidden = false; document.getElementById('heroAiTag').hidden = false; }
}

initHero(); initUK(); initUSA(); initKonya(); initGame();
