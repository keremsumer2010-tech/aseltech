// NISAR Pulse — data explorer. Everything is driven by data/catalog.json (built by analysis/build_catalog.py).
const LOCAL = location.pathname.includes('/web/');
const ROOT = LOCAL ? '../' : './';
const ESRI = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
const STYLE = {version: 8, sources: {sat: {type: 'raster', tiles: [ESRI], tileSize: 256, attribution: 'Imagery © Esri, Maxar, Earthstar Geographics'}},
  layers: [{id: 'sat', type: 'raster', source: 'sat', paint: {'raster-brightness-max': 0.72, 'raster-saturation': -0.25}}]};
const RAMPS = {  // same colour maps as the PNGs (matplotlib RdBu, viridis, magma)
  RdBu: 'linear-gradient(90deg,#67001f,#d6604d,#f7f7f7,#4393c3,#053061)',
  viridis: 'linear-gradient(90deg,#440154,#3b528b,#21918c,#5ec962,#fde725)',
  magma: 'linear-gradient(90deg,#000004,#51127c,#b73779,#fc8961,#fcfdbf)'};
const MAPKINDS = ['raster_series', 'raster'];
const $ = id => document.getElementById(id);
const fmt = d => new Date(d + 'T00:00:00Z').toLocaleDateString('en-GB', {day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC'});
const sgn = v => (v < 0 ? '−' : '+') + Math.abs(v).toFixed(1);
async function J(p){ try{ const r = await fetch(ROOT + p, {cache: 'no-cache'}); return r.ok ? await r.json() : null; }catch(e){ return null; } }
const corners = ([w, s, e, n]) => [[w, n], [e, n], [e, s], [w, s]];

let CAT = [], site = null, layer = null, idx = 0, timer = null, chart = null, grid = null, pts = null, marker = null;
const map = new maplibregl.Map({container: 'xpMap', style: STYLE, center: [0, 30], zoom: 1.5, attributionControl: {compact: true}});
map.addControl(new maplibregl.NavigationControl({showCompass: false}), 'top-right');
// controls fill at once; map layers wait for the style (a hidden or slow map must not leave the page empty)
const mapReady = new Promise(res => map.once('load', res));

function badge(q){
  const t = {provisional: 'PROVISIONAL', mixed: 'MIXED: includes pre-calibration beta', preview: 'PREVIEW — not quantitative', reference: 'REFERENCE (literature)'}[q] || (q || '').toUpperCase();
  return `<span class="qbadge ${q === 'mixed' ? 'beta' : q}">${t}</span>`;
}
function setLegend(l){
  const g = l?.legend; $('xpLegend').hidden = !g; if (!g) return;
  $('xpRamp').style.background = RAMPS[g.cmap] || RAMPS.viridis;
  $('xpMin').textContent = (g.cmap === 'RdBu' ? '≤ ' : '') + g.vmin; $('xpMax').textContent = (g.cmap === 'RdBu' ? '≥ +' : '') + g.vmax;
  $('xpUnits').textContent = g.units; $('xpLow').textContent = g.low || ''; $('xpHigh').textContent = g.high || '';
}
function pngUrl(l, i){ return ROOT + (l.kind === 'raster_series' ? l.png.replace('{date}', l.dates[i]) : l.png); }

function showLayer(l, keepDate){
  layer = l; if (!keepDate) idx = l.dates ? l.dates.length - 1 : 0;
  const url = pngUrl(l, idx), src = map.getSource('xl');
  if (src) src.updateImage({url, coordinates: corners(l.bbox)});
  else { map.addSource('xl', {type: 'image', url, coordinates: corners(l.bbox)}); map.addLayer({id: 'xl', type: 'raster', source: 'xl', paint: {'raster-opacity': 0.85, 'raster-fade-duration': 0}}, map.getLayer('ov-risk') ? 'ov-risk' : undefined); }
  $('xpTime').hidden = l.kind !== 'raster_series';
  if (l.kind === 'raster_series'){ const s = $('xpSlider'); s.max = l.dates.length - 1; s.value = idx; $('xpDate').textContent = fmt(l.dates[idx]); }
  setLegend(l);
  $('xpBadge').innerHTML = badge(l.quality) + (l.quality === 'mixed' ? ' <small>Dates before 17 Jun 2026 use pre-calibration beta products.</small>' : '');
  if (marker) pick(marker.getLngLat());
}
function go(i){ idx = i; showLayer(layer, true); }

async function chooseSite(name){
  site = CAT.find(s => s.site === name); if (!site) return;
  stop(); grid = null; pts = null; if (marker){ marker.remove(); marker = null; }
  $('xpPick').textContent = 'Click the map to see one spot.'; $('xpChartBox').hidden = true;
  const mapLayers = site.layers.filter(l => MAPKINDS.includes(l.kind));
  $('xpLayers').innerHTML = mapLayers.map((l, i) => `<label class="xp-radio"><input type="radio" name="lyr" value="${l.id}" ${i === 0 ? 'checked' : ''}> ${l.title}</label>`).join('');
  $('xpLayers').querySelectorAll('input').forEach(r => r.addEventListener('change', () => showLayer(mapLayers.find(l => l.id === r.value))));
  const ovs = site.layers.filter(l => l.kind === 'geojson');
  $('xpOverlays').innerHTML = ovs.map(l => `<label class="xp-check"><input type="checkbox" data-id="${l.id}" checked> ${l.title}</label>`).join('');
  $('xpBadge').innerHTML = badge(site.quality);
  await mapReady; if (site.site !== name) return;
  // overlays (geojson)
  for (const id of ['ov-risk', 'ov-sink']) if (map.getLayer(id)){ map.removeLayer(id); map.removeSource(id); }
  for (const l of ovs){
    const d = await J(l.file); if (!d) continue;
    const id = l.id === 'risk' ? 'ov-risk' : 'ov-sink';
    map.addSource(id, {type: 'geojson', data: d});
    if (id === 'ov-risk') map.addLayer({id, type: 'line', source: id, paint: {'line-width': ['match', ['get', 'risk'], 'high', 3.2, 'medium', 2, 1], 'line-color': ['match', ['get', 'risk'], 'high', '#ff5a47', 'medium', '#e3b341', '#3fb950']}});
    else map.addLayer({id, type: 'circle', source: id, paint: {'circle-radius': 5, 'circle-color': '#ff5a47', 'circle-stroke-color': '#fff', 'circle-stroke-width': 1.5}});
  }
  $('xpOverlays').querySelectorAll('input').forEach(c => c.addEventListener('change', () => { const id = c.dataset.id === 'risk' ? 'ov-risk' : 'ov-sink'; if (map.getLayer(id)) map.setLayoutProperty(id, 'visibility', c.checked ? 'visible' : 'none'); }));
  if (mapLayers.length) showLayer(mapLayers[0]); else { $('xpLegend').hidden = true; $('xpTime').hidden = true; }
  const b = site.bbox || mapLayers[0]?.bbox; if (b) map.fitBounds([[b[0], b[1]], [b[2], b[3]]], {padding: 30, duration: 1200});
  const gl = site.layers.find(l => l.id === 'grid'), pl = site.layers.find(l => l.id === 'points');
  if (gl) grid = await J(gl.file);
  if (pl) pts = await J(pl.file);
  $('xpHow').innerHTML = grid ? `Clicked values come from a ~${Math.round(grid.step_deg * 111)} km grid made from the 80 m measurements (median per cell), so peaks look a little smaller than the 1 km headline numbers.`
    : pts ? 'This region has no clickable grid yet: a click shows the nearest of its measured points.' : '';
  history.replaceState(null, '', '#' + site.site);
}

function cellSeries(ll){
  if (!grid) return null;
  const [w, s, e, n] = grid.bbox, c = Math.floor((ll.lng - w) / grid.step_deg), r = Math.floor((n - ll.lat) / grid.step_deg);
  if (c < 0 || r < 0 || c >= grid.ncols || r >= grid.nrows) return null;
  const k = r * grid.ncols + c, series = grid.values.map(v => v[k]);
  return series.some(v => v != null) ? {series, dates: grid.dates, label: `${grid.step_deg * 111 < 1.5 ? '~1' : '~2'} km cell at ${ll.lat.toFixed(3)}°, ${ll.lng.toFixed(3)}°`} : {series: null};
}
function nearestPoint(ll){
  if (!pts?.length) return null;
  const kx = 111.32 * Math.cos(ll.lat * Math.PI / 180);
  let best = null, bd = 1e9;
  for (const p of pts){ const d = Math.hypot((p.lon - ll.lng) * kx, (p.lat - ll.lat) * 110.57); if (d < bd){ bd = d; best = p; } }
  return bd <= 10 ? {series: best.disp_cm, dates: best.dates, label: `nearest measured point: ${best.name} (${bd.toFixed(1)} km away)`} : null;
}
function pick(ll){
  if (!site) return;
  if (marker) marker.setLngLat(ll); else marker = new maplibregl.Marker({color: '#0b3d91'}).setLngLat(ll).addTo(map);
  const r = cellSeries(ll) ?? nearestPoint(ll);
  if (!r || !r.series){ $('xpPick').innerHTML = 'No reliable measurement here (masked: water, changing crops or outside the radar view).'; $('xpChartBox').hidden = true; return; }
  const motion = site.layers.find(l => l.id === 'motion');
  const di = layer?.id === 'motion' ? idx : r.dates.length - 1, v = r.series[Math.min(di, r.series.length - 1)];
  const valTxt = v == null ? 'no value on this date' : `<b>${sgn(v)} cm</b> since ${fmt(r.dates[0])}`;
  $('xpPick').innerHTML = `${r.label}<br>On ${fmt(r.dates[di])}: ${valTxt}${Math.abs(v ?? 9) < 1 ? ' (within the ~1 cm noise)' : ''}.` +
    (layer && layer.id !== 'motion' ? `<br><span class="small">The chart shows ground motion; the map shows “${layer.title}”.</span>` : '');
  const data = {labels: r.dates.map(d => new Date(d + 'T00:00:00Z').toLocaleDateString('en-GB', {day: 'numeric', month: 'short', timeZone: 'UTC'})),
    datasets: [{label: 'Ground motion seen by NISAR (cm)', data: r.series, borderColor: '#c8321f', backgroundColor: 'rgba(200,50,31,.1)', fill: true, tension: .25, pointRadius: 2.5, spanGaps: true}]};
  $('xpChartBox').hidden = false;
  if (chart){ chart.data = data; chart.update(); }
  else chart = new Chart($('xpChart'), {type: 'line', data, options: {responsive: true, animation: {duration: 250}, plugins: {legend: {labels: {boxWidth: 12, font: {size: 11}}}},
    scales: {x: {ticks: {font: {size: 10}, maxRotation: 0, autoSkip: true}}, y: {title: {display: true, text: 'cm'}}}}});
  void motion;
}
function stop(){ if (timer){ clearInterval(timer); timer = null; $('xpPlay').textContent = '▶'; } }

(async () => {
  CAT = (await J('data/catalog.json') || []).filter(s => s.layers.some(l => MAPKINDS.includes(l.kind)));
  $('xpSite').innerHTML = CAT.map(s => `<option value="${s.site}">${s.title}</option>`).join('');
  $('xpSite').addEventListener('change', e => chooseSite(e.target.value));
  $('xpSlider').addEventListener('input', e => { stop(); go(+e.target.value); });
  $('xpPlay').addEventListener('click', () => { if (timer) return stop(); $('xpPlay').textContent = '❚❚'; timer = setInterval(() => go((idx + 1) % layer.dates.length), 900); });
  map.on('click', e => pick(e.lngLat));
  map.on('click', 'ov-sink', e => { const p = e.features[0].properties; new maplibregl.Popup().setLngLat(e.lngLat).setHTML(`<b>${p.name}</b>${p.year_formed ? ' · ' + p.year_formed : ''}<br><a href="${p.source_url}" target="_blank" rel="noopener">${p.source_title || 'source'}</a>`).addTo(map); });
  map.on('click', 'ov-risk', e => { const p = e.features[0].properties; new maplibregl.Popup().setLngLat(e.lngLat).setHTML(`<b>${p.name || p.type}</b><br>${p.type} · risk <b>${p.risk}</b><br>${(+p.gradient_mm_per_km).toFixed(0)} mm/km · ${(+p.max_cm).toFixed(1)} cm`).addTo(map); });
  const start = CAT.find(s => s.site === location.hash.slice(1)) ? location.hash.slice(1) : CAT[0]?.site;
  if (start){ $('xpSite').value = start; chooseSite(start); }
})();
