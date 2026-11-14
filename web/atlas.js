// NISAR Pulse — Global Subsidence Atlas 2026
const LOCAL = location.pathname.includes('/web/');
const ROOT = LOCAL ? '../' : './';
const ESRI = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
const STYLE = {
  version: 8,
  sources: {sat: {type: 'raster', tiles: [ESRI], tileSize: 256, attribution: 'Imagery © Esri, Maxar, Earthstar Geographics'}},
  layers: [{id: 'sat', type: 'raster', source: 'sat', paint: {'raster-brightness-max': 0.78, 'raster-saturation': -0.2}}]
};

const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const fmtNum = (v, d = 1) => (typeof v === 'number' && Number.isFinite(v)) ? (v < 0 ? '−' : (v > 0 ? '+' : '')) + Math.abs(v).toFixed(d) : '—';
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

function confBadge(r){
  const c = (r.confidence || 'low').toLowerCase();
  const lbl = (r.indicative_only || c === 'low') ? `${c} · indicative only` : c;
  return `<span class="cbadge ${esc(c)}">${esc(lbl)}</span>`;
}

let map, atlasData = null, activeId = null;

async function initAtlas(){
  atlasData = await J('data/global/atlas.json');
  if (!atlasData || !Array.isArray(atlasData.regions)){
    document.getElementById('atlasList').innerHTML = '<p class="small">Could not load data/global/atlas.json.</p>';
    return;
  }
  const regions = atlasData.regions
    .slice()
    .sort((a, b) => (a.rate_cm_per_100d ?? 999) - (b.rate_cm_per_100d ?? 999));

  document.getElementById('stTotal').textContent = atlasData.n_regions ?? regions.length;
  document.getElementById('stRel').textContent = atlasData.n_reliable ?? regions.filter(r => !r.indicative_only).length;
  document.getElementById('stInd').textContent = atlasData.n_indicative ?? regions.filter(r => r.indicative_only).length;

  const listEl = document.getElementById('atlasList');
  listEl.innerHTML = regions.map(r => {
    const rateTxt = (typeof r.rate_cm_per_100d === 'number' && Number.isFinite(r.rate_cm_per_100d))
      ? `${fmtNum(r.rate_cm_per_100d)} cm/100d`
      : 'no data';
    return `<button type="button" class="atlas-item" data-id="${esc(r.id)}">
      <span class="ai-left"><span class="ai-name">${r.rank ? '#' + r.rank + ' · ' : ''}${esc(r.name)}</span><span class="ai-sub">${esc(r.country || '')} · ${confBadge(r)}</span></span>
      <span class="ai-right"><span class="ai-rate" style="color:${rateColor(r.rate_cm_per_100d)}">${esc(rateTxt)}</span></span>
    </button>`;
  }).join('');

  listEl.querySelectorAll('.atlas-item').forEach(btn => {
    btn.addEventListener('click', () => selectRegion(btn.dataset.id, true));
  });

  const geojson = {
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
          indicative: Boolean(r.indicative_only)
        },
        geometry: {type: 'Point', coordinates: [r.lon, r.lat]}
      }))
  };

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

  map.on('load', () => {
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
        'circle-opacity': ['case', ['get', 'indicative'], 0.72, 0.95]
      }
    });
    map.on('click', 'atlas-pts', e => {
      const f = e.features?.[0];
      if (f?.properties?.id) selectRegion(f.properties.id, true);
    });
    map.on('mouseenter', 'atlas-pts', () => { map.getCanvas().style.cursor = 'pointer'; });
    map.on('mouseleave', 'atlas-pts', () => { map.getCanvas().style.cursor = ''; });
  });

  const hashId = location.hash ? location.hash.slice(1) : '';
  const initial = regions.find(r => r.id === hashId) || regions[0];
  if (initial) selectRegion(initial.id, false);
  renderTables(regions);
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
      selectRegion(tr.dataset.id, true);
      window.scrollTo({top: 0, behavior: 'smooth'});
    }));
  };
  fill('tblReliable', rel);
  fill('tblIndicative', ind);
}

async function selectRegion(id, fly){
  const r = atlasData?.regions?.find(x => x.id === id);
  if (!r) return;
  activeId = id;
  document.querySelectorAll('.atlas-item').forEach(el => el.classList.toggle('is-active', el.dataset.id === id));
  if (fly && map && typeof r.lon === 'number' && typeof r.lat === 'number'){
    map.flyTo({center: [r.lon, r.lat], zoom: 4.5, duration: 1200});
  }

  const base = r.path ? (r.path.endsWith('/') ? r.path : r.path + '/') : `data/global/${r.id}/`;
  const [meta, hasBul] = await Promise.all([
    J(base + 'meta.json'),
    okHead(`docs/bulletins/${r.id}.html`)
  ]);

  const periodTxt = Array.isArray(r.period) && r.period.length === 2
    ? `${fmtShort(r.period[0])} – ${fmtDate(r.period[1])} (${r.days ?? '—'} days)`
    : '—';
  const validTxt = (typeof r.valid_fraction === 'number' && Number.isFinite(r.valid_fraction))
    ? `${(r.valid_fraction * 100).toFixed(1)}%`
    : '—';
  const refTxt = Array.isArray(r.ref_range_cm) && r.ref_range_cm.length === 2
    ? `${fmtNum(Math.min(...r.ref_range_cm))} to ${fmtNum(Math.max(...r.ref_range_cm))} cm`
    : '—';
  const lastDate = meta?.dates?.length ? meta.dates[meta.dates.length - 1] : null;
  const pngPath = lastDate ? `${base}disp/${lastDate}.png` : null;
  const srcTxt = meta?.source || 'NASA-ISRO NISAR L2 GUNW (provisional) via ASF DAAC';

  const detail = document.getElementById('atlasDetail');
  detail.hidden = false;
  detail.innerHTML = `
    <h2>${esc(r.name)} <small class="small">(${esc(r.country || '')})</small></h2>
    <p style="margin:0 0 8px">${confBadge(r)} <span class="qbadge provisional">${esc((r.quality || 'provisional').toUpperCase())}</span></p>
    <dl class="atlas-kv">
      <div><dt>Rate (LOS)</dt><dd>${esc(fmtNum(r.rate_cm_per_100d))} cm/100d</dd></div>
      <div><dt>Max LOS</dt><dd>${esc(fmtNum(r.max_cm_los))} cm</dd></div>
      <div><dt>Vertical (est.)</dt><dd>${esc(fmtNum(r.max_cm_vertical_est))} cm</dd></div>
      <div><dt>Yearly rate (est.)</dt><dd>${esc(fmtNum(r.rate_cm_per_yr_estimate))} cm/yr</dd></div>
      <div><dt>Period</dt><dd style="font-size:.78rem">${esc(periodTxt)}</dd></div>
      <div><dt>Pairs / Valid px</dt><dd>${r.n_pairs ?? '—'} pairs · ${esc(validTxt)}</dd></div>
      <div><dt>2nd percentile (p2)</dt><dd>${esc(fmtNum(r.p2_cm))} cm</dd></div>
      <div><dt>Ref. spread</dt><dd style="font-size:.78rem">${esc(refTxt)}</dd></div>
    </dl>
    ${r.note ? `<p class="small">${esc(r.note)}</p>` : ''}
    <p class="atlas-src"><b>Source:</b> ${esc(srcTxt)}</p>
    ${pngPath ? `<div class="atlas-png"><img src="${ROOT + esc(pngPath)}" alt="Cumulative ground motion map for ${esc(r.name)}" loading="lazy"><p class="small" style="margin:4px 0 0">Cumulative LOS map (${esc(fmtDate(lastDate))}).</p></div>` : ''}
    <div class="atlas-actions">
      ${hasBul ? `<a href="${ROOT}docs/bulletins/${esc(r.id)}.html" target="_blank" rel="noopener">Open bulletin →</a>` : ''}
      <a href="explorer.html#${esc(r.id)}">Open in Explorer →</a>
    </div>
  `;
}

initAtlas();
