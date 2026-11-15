// NISAR on the atlas (PC1). The atlas map stays the main view; this file adds
//  1) a light "NISAR now" layer on the atlas globe: real position, ground track and the
//     left-looking 33–47° swath, computed from the CelesTrak TLE with SGP4 (satellite.js);
// Uses globals from atlas.js: map, mapReady. (web/nisar3d.js, the full 3D orbit view, is kept
// in the repo but not linked from the atlas, so the atlas stays focused on the measurements.)
(function(){
  const bar = document.querySelector('.atlas-toolbar');
  const wrap = document.querySelector('.atlas-mapwrap');
  if (!bar || !wrap) return;
  const ROOT = location.pathname.includes('/web/') ? '../' : './';
  const SAT = window.satellite;
  const D2R = Math.PI / 180, R_E = 6371.0;

  // ---------- toolbar: live-layer toggle + 3D button ----------
  const live = document.createElement('label');
  live.className = 'n3d-live-toggle';
  live.innerHTML = '<input type="checkbox" checked> <span class="dot"></span>NISAR now';
  live.title = "NISAR's real position, ground track and radar swath (SGP4 from CelesTrak TLE)";
  bar.appendChild(live);
  const key = document.createElement('div');
  key.className = 'nisar-key';
  key.innerHTML = '<b>NISAR now</b> · real orbit (SGP4, CelesTrak TLE)'
    + '<div><span class="k-sat"></span>spacecraft position</div>'
    + '<div><span class="k-track"></span>ground track (±50 min)</div>'
    + '<div><span class="k-swath"></span>radar swath, last 12 min (left-looking, ≈242 km)</div>';
  wrap.appendChild(key);

  // ---------- live layer on the atlas map ----------
  if (!SAT) return;
  let satrec = null;
  fetch(ROOT + 'data/nisar_tle.json').then(r => r.ok ? r.json() : null).then(t => {
    if (t) satrec = SAT.twoline2satrec(t.line1, t.line2);
  }).catch(() => {});

  const toLL = v => [Math.atan2(v[1], v[0]) / D2R, Math.asin(Math.max(-1, Math.min(1, v[2]))) / D2R];
  const norm = v => { const n = Math.hypot(v[0], v[1], v[2]); return [v[0] / n, v[1] / n, v[2] / n]; };
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const along = (u, w, g) => norm([u[0] * Math.cos(g) + w[0] * Math.sin(g), u[1] * Math.cos(g) + w[1] * Math.sin(g), u[2] * Math.cos(g) + w[2] * Math.sin(g)]);
  const centralAngle = (inc, rs) => inc * D2R - Math.asin(R_E * Math.sin(inc * D2R) / rs);

  // Earth-fixed state at time t: sub-satellite unit vector, left (look-side) unit vector, orbit radius.
  function ecef(t){
    const d = new Date(t), pv = SAT.propagate(satrec, d);
    if (!pv.position) return null;
    const g = SAT.gstime(d);
    const p = SAT.eciToEcf(pv.position, g);
    const q = SAT.eciToEcf({x: pv.position.x + pv.velocity.x, y: pv.position.y + pv.velocity.y, z: pv.position.z + pv.velocity.z}, g);
    const up = norm([p.x, p.y, p.z]);
    const left = norm(cross(up, [q.x - p.x, q.y - p.y, q.z - p.z]));
    return {up, left, rs: Math.hypot(p.x, p.y, p.z)};
  }
  // Split a lon/lat line where it crosses the antimeridian so MapLibre does not draw across the map.
  function splitLines(pts){
    const out = [[]];
    pts.forEach((p, i) => {
      if (i && Math.abs(p[0] - pts[i - 1][0]) > 180) out.push([]);
      out[out.length - 1].push(p);
    });
    return out.filter(l => l.length > 1);
  }

  function build(now){
    const track = [], near = [], far = [], swathPolys = [];
    for (let k = -50; k <= 50; k += 0.5){
      const s = ecef(now + k * 60000); if (!s) continue;
      track.push(toLL(s.up));
      if (k >= -12 && k <= 0){
        near.push(toLL(along(s.up, s.left, centralAngle(33, s.rs))));
        far.push(toLL(along(s.up, s.left, centralAngle(47, s.rs))));
      }
    }
    for (let i = 1; i < near.length; i++){
      const ring = [near[i - 1], far[i - 1], far[i], near[i], near[i - 1]];
      const lons = ring.map(p => p[0]);
      if (Math.max(...lons) - Math.min(...lons) < 180) swathPolys.push(ring);
    }
    const s0 = ecef(now);
    return {
      track: {type: 'FeatureCollection', features: splitLines(track).map(c => ({type: 'Feature', geometry: {type: 'LineString', coordinates: c}, properties: {}}))},
      swath: {type: 'FeatureCollection', features: swathPolys.map(r => ({type: 'Feature', geometry: {type: 'Polygon', coordinates: [r]}, properties: {}}))},
      pos: s0 ? toLL(s0.up) : null
    };
  }

  let marker = null, added = false;
  function ensureLayers(){
    if (added || typeof map === 'undefined' || !map || !mapReady) return added;
    const empty = {type: 'FeatureCollection', features: []};
    map.addSource('nisar-track', {type: 'geojson', data: empty});
    map.addSource('nisar-swath', {type: 'geojson', data: empty});
    const before = map.getLayer('atlas-pts') ? 'atlas-pts' : undefined;
    map.addLayer({id: 'nisar-swath', type: 'fill', source: 'nisar-swath', paint: {'fill-color': '#38bdf8', 'fill-opacity': 0.32}}, before);
    map.addLayer({id: 'nisar-track', type: 'line', source: 'nisar-track', paint: {'line-color': '#fbbf24', 'line-width': 1.4, 'line-opacity': 0.8, 'line-dasharray': [2, 2]}}, before);
    const el = document.createElement('div');
    el.className = 'nisar-marker';
    el.innerHTML = '<svg viewBox="0 0 40 24" aria-hidden="true"><rect x="1" y="9" width="12" height="6" fill="#1e3a8a" stroke="#93c5fd" stroke-width=".8"/><rect x="27" y="9" width="12" height="6" fill="#1e3a8a" stroke="#93c5fd" stroke-width=".8"/><rect x="15" y="7" width="10" height="10" rx="1" fill="#d4a017" stroke="#fde68a" stroke-width=".8"/><ellipse cx="20" cy="4" rx="7" ry="2.4" fill="#e7c27a" stroke="#fff4d6" stroke-width=".6"/></svg><span>NISAR</span>';
    el.title = 'NISAR now (real position, SGP4 from CelesTrak TLE)';
    marker = new maplibregl.Marker({element: el, anchor: 'center'});
    added = true;
    return true;
  }
  function update(){
    if (!satrec || !live.querySelector('input').checked || document.hidden) return;
    if (!ensureLayers()) return;
    const g = build(Date.now());
    map.getSource('nisar-track').setData(g.track);
    map.getSource('nisar-swath').setData(g.swath);
    if (g.pos){ marker.setLngLat(g.pos); if (!marker._map) marker.addTo(map); }
  }
  function setVisible(on){
    if (!added) return;
    ['nisar-track', 'nisar-swath'].forEach(id => map.setLayoutProperty(id, 'visibility', on ? 'visible' : 'none'));
    if (on) update(); else if (marker) marker.remove();
  }
  live.querySelector('input').addEventListener('change', e => { setVisible(e.target.checked); key.hidden = !e.target.checked; });
  setInterval(update, 3000);
  setTimeout(update, 1500);
  document.addEventListener('visibilitychange', update);
})();
