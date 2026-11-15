/* Valley Under Pressure v2 — Interactive Satellite & Hydrogeology Simulation */
(function () {
  'use strict';

  const BASIN_UI = {
    tulare: {
      id: 'tulare',
      shortLabel: 'Tulare Basin',
      bbox: [-120.2, 35.6, -119.0, 36.6],
      center: [-119.62, 36.08],
      zoom: 8.6,
      zoneRadLon: 0.082,
      zoneRadLat: 0.064,
      rasterUrl: '../data/central_valley/disp/2026-10-14.png',
      summaryUrl: '../data/central_valley/summary.json',
      pointsUrl: '../data/central_valley/points.json',
      assetsUrl: '../data/central_valley/assets.json',
      localInfraUrl: '../risk/central_valley_infra.geojson',
      sinkholesUrl: null,
      windowLabel: '2026-06-28 → 2026-10-14',
      calNote: 'ref range −4.7…−7.8 cm LOS',
      endAssetsText: '81 / 645 segments',
      endValLabel: 'Validation GNSS r (CAHA)',
      endValText: '0.90 (RMSE 0.75 cm)',
    },
    konya: {
      id: 'konya',
      shortLabel: 'Konya Closed Basin',
      bbox: [33.3, 37.6, 33.8, 37.9],
      center: [33.63, 37.73],
      zoom: 10.6,
      zoneRadLon: 0.036,
      zoneRadLat: 0.025,
      rasterUrl: '../data/karapinar/disp/2026-10-12.png',
      summaryUrl: '../data/karapinar/summary.json',
      pointsUrl: '../data/karapinar/points.json',
      assetsUrl: '../data/karapinar/assets.json',
      localInfraUrl: '../risk/karapinar_infra.geojson',
      sinkholesUrl: '../data/karapinar/sinkholes.geojson',
      windowLabel: '2026-06-26 → 2026-10-12',
      calNote: '41.9 deg incidence; 29 documented obruks',
      endAssetsText: '10 / 64 corridors · 29 obruks',
      endValLabel: '0–1 km Obruk Ring NISAR Mean',
      endValText: '−4.15 cm LOS',
    },
  };

  const urlBasin = new URLSearchParams(window.location.search).get('basin');
  let activeBasinId = (urlBasin === 'konya' || urlBasin === 'konya_plain' || urlBasin === 'karapinar') ? 'konya' : 'tulare';
  let simState = null;
  let selectedDistrictId = 'p01';
  let applyAll = true; // sliders set the whole basin; the readout follows the district clicked on the map
  let activePreset = 'baseline';
  let chartStart = null; // first month shown in the panned timeline (null = follow the current month)
  const CHART_WINDOW = 12;
  let overlayMode = 'sim'; // 'sim' | 'blend' | 'nisar'
  let audioEnabled = false;
  let audioCtx = null;

  let map = null;
  let mapReady = false;
  let districtMarkers = {};
  let refMarker = null;
  let assetsGeoJson = null;
  let infraBackdropGeoJson = null;
  let sinkholesGeoJson = null;
  let summaryData = null;
  let pointsData = null;
  const basinDataCache = {};
  let timelineChart = null;
  let endCompareChart = null;

  // DOM helpers
  const $ = (id) => document.getElementById(id);

  function rdBuColorForCm(cm) {
    // RdBu color scale matching data/central_valley/meta.json (negative=red sink, 0=white/neutral, +6=blue uplift)
    if (cm >= 2.0) return '#2166ac';
    if (cm >= 0.3) return '#67a9cf';
    if (cm > -1.0) return '#d1e5f0';
    if (cm > -3.5) return '#f4a582';
    if (cm > -7.0) return '#d6604d';
    if (cm > -12.0) return '#b2182b';
    return '#67001f';
  }

  function canalColorForGradient(gradMmKm) {
    if (gradMmKm >= ValleyModel.CONFIG.thresholds.canalHighGradientMmKm) return '#f06938';
    if (gradMmKm >= ValleyModel.CONFIG.thresholds.canalMediumGradientMmKm) return '#e69f00';
    return '#009e73';
  }

  function playTone(kind) {
    if (!audioEnabled) return;
    try {
      if (!audioCtx) {
        const Ctx = window.AudioContext || window.webkitAudioContext;
        if (Ctx) audioCtx = new Ctx();
      }
      if (!audioCtx) return;
      if (audioCtx.state === 'suspended') audioCtx.resume();
      const now = audioCtx.currentTime;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = kind === 'warn' ? 'sawtooth' : 'triangle';
      osc.frequency.setValueAtTime(kind === 'warn' ? 190 : 520, now);
      if (kind === 'warn') {
        osc.frequency.exponentialRampToValueAtTime(125, now + 0.14);
      }
      gain.gain.setValueAtTime(0.035, now);
      gain.gain.exponentialRampToValueAtTime(0.0008, now + (kind === 'warn' ? 0.16 : 0.045));
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(now);
      osc.stop(now + (kind === 'warn' ? 0.17 : 0.05));
    } catch (_err) {
      // Ignore audio errors if blocked by browser policy
    }
  }

  /**
   * Build crisp district boundary polygons around each simulated district so live RdBu fills
   * and boundary lines update dynamically over the satellite imagery every month.
   */
  function buildDistrictZonesGeoJson() {
    const features = [];
    const steps = 8;
    const ui = BASIN_UI[activeBasinId] || BASIN_UI.tulare;
    simState.districts.forEach((d) => {
      const coords = [];
      const radLon = ui.zoneRadLon;
      const radLat = ui.zoneRadLat;
      for (let i = 0; i <= steps; i++) {
        const ang = (i / steps) * Math.PI * 2 + Math.PI / 8;
        coords.push([d.lon + Math.cos(ang) * radLon, d.lat + Math.sin(ang) * radLat]);
      }
      const absCm = Math.abs(d.totalCm);
      const isSelected = d.id === selectedDistrictId;
      const rdColor = absCm < 0.25 ? '#94a3b8' : rdBuColorForCm(d.totalCm);
      const fillOpacity = Number(Math.min(0.36, 0.05 + absCm * 0.025).toFixed(3));
      features.push({
        type: 'Feature',
        properties: {
          id: d.id,
          color: rdColor,
          opacity: fillOpacity,
          strokeColor: isSelected ? '#4da3ff' : rdColor,
          strokeWidth: isSelected ? 2.4 : 1.5,
        },
        geometry: { type: 'Polygon', coordinates: [coords] },
      });
    });
    return { type: 'FeatureCollection', features };
  }

  /**
   * Assign each segment in assets.json to its nearest simulation district once,
   * then recalculate live color/gradient dynamically on each turn.
   */
  function tagAssetsToNearestDistrict(geojson) {
    if (!geojson || !Array.isArray(geojson.features)) return;
    geojson.features.forEach((feat) => {
      const geom = feat.geometry;
      if (!geom || !geom.coordinates || !geom.coordinates.length) return;
      const mid =
        geom.type === 'LineString'
          ? geom.coordinates[Math.floor(geom.coordinates.length / 2)]
          : geom.coordinates[0][0];
      if (!Array.isArray(mid)) return;
      let bestId = simState.districts[0].id;
      let bestDist = Infinity;
      simState.districts.forEach((d) => {
        const dx = mid[0] - d.lon;
        const dy = mid[1] - d.lat;
        const d2 = dx * dx + dy * dy;
        if (d2 < bestDist) {
          bestDist = d2;
          bestId = d.id;
        }
      });
      feat.properties._districtId = bestId;
    });
  }

  function buildDynamicCanalsGeoJson() {
    if (!assetsGeoJson || !Array.isArray(assetsGeoJson.features)) {
      return { type: 'FeatureCollection', features: [] };
    }
    const byId = {};
    simState.districts.forEach((d) => {
      byId[d.id] = d;
    });

    const canalFeatures = assetsGeoJson.features
      .filter((f) => f.properties && (f.properties.type === 'canal' || (activeBasinId === 'konya' && f.properties.risk === 'high')))
      .map((f) => {
        const d = byId[f.properties._districtId] || simState.districts[0];
        const amp = Math.max(0.15, Math.abs(d.totalCm) / Math.max(1.5, Math.abs(ValleyModel.losToVertical(d.nisarLosCm, simState.incidenceDeg))));
        const baseGrad = typeof f.properties.gradient_mm_per_km === 'number' ? f.properties.gradient_mm_per_km : 4.0;
        const liveGrad = Number((baseGrad * Math.min(2.5, amp)).toFixed(2));
        return {
          type: 'Feature',
          geometry: f.geometry,
          properties: {
            ...f.properties,
            simGradient: liveGrad,
            simColor: canalColorForGradient(liveGrad),
          },
        };
      });
    return { type: 'FeatureCollection', features: canalFeatures };
  }

  function rebuildMapMarkers() {
    Object.values(districtMarkers).forEach((m) => {
      if (m && m.marker) m.marker.remove();
    });
    districtMarkers = {};
    if (refMarker) {
      refMarker.remove();
      refMarker = null;
    }
    if (!mapReady || !simState) return;

    // Interactive District Place Labels (zero missing glyph server errors)
    simState.districts.forEach((d) => {
      const el = document.createElement('button');
      el.type = 'button';
      el.className = 'dmark';
      el.setAttribute('aria-label', `Show readout for ${d.shortName}`);
      el.innerHTML = `<span>${d.shortName}</span> <span class="mval">0.0 cm</span>`;
      el.addEventListener('click', () => selectDistrict(d.id, false));
      const mk = new maplibregl.Marker({ element: el, anchor: 'bottom' })
        .setLngLat([d.lon, d.lat])
        .addTo(map);
      districtMarkers[d.id] = { marker: mk, el };
    });

    // Stable reference marker from points.json
    if (Array.isArray(pointsData)) {
      const refPt = pointsData.find((p) => p.kind === 'near_reference');
      if (refPt) {
        const refEl = document.createElement('div');
        refEl.className = 'refmark';
        refEl.textContent = `Reference: ${refPt.name}`;
        refMarker = new maplibregl.Marker({ element: refEl, anchor: 'top' })
          .setLngLat([refPt.lon, refPt.lat])
          .addTo(map);
      }
    }
  }

  /**
   * Initialize MapLibre 4.7.1 with Esri World Imagery + NISAR Raster + Real OSM Canals/Roads + District Markers.
   */
  function showStaticMap(ui) {
    const el = document.getElementById('map');
    if (!el) return;
    el.innerHTML = `<div class="map-static"><img src="${ui.rasterUrl}" alt="NISAR ground motion map of the selected basin">
      <p>Static map: the interactive map needs WebGL (graphics hardware acceleration), which is off in this browser. The simulation, sliders and charts still work.</p></div>`;
  }

  function initMap() {
    const ui = BASIN_UI[activeBasinId] || BASIN_UI.tulare;
    // Without WebGL or the MapLibre script the simulator used to stop here (black screen).
    // Now the map shows the NISAR image as a static picture and the simulation keeps working (PC1).
    const webgl = (() => { try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (e) { return false; } })();
    if (typeof maplibregl === 'undefined' || !webgl) { showStaticMap(ui); return; }
    try {
    map = new maplibregl.Map({
      container: 'map',
      center: ui.center,
      zoom: ui.zoom,
      minZoom: 7.0,
      maxZoom: 14,
      attributionControl: { compact: true },
      style: {
        version: 8,
        sources: {
          esri: {
            type: 'raster',
            tiles: [
              'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            ],
            tileSize: 256,
            attribution: 'Tiles © Esri — World Imagery · Infra © OpenStreetMap (ODbL) · Data: NASA-ISRO NISAR (Provisional)',
          },
          'nisar-disp': {
            type: 'image',
            url: ui.rasterUrl,
            coordinates: [
              [ui.bbox[0], ui.bbox[3]],
              [ui.bbox[2], ui.bbox[3]],
              [ui.bbox[2], ui.bbox[1]],
              [ui.bbox[0], ui.bbox[1]],
            ],
          },
        },
        layers: [
          {
            id: 'esri-sat',
            type: 'raster',
            source: 'esri',
            paint: { 'raster-brightness-max': 0.86, 'raster-saturation': -0.15 },
          },
          {
            id: 'nisar-raster',
            type: 'raster',
            source: 'nisar-disp',
            paint: { 'raster-opacity': 0.14 },
          },
        ],
      },
    });
    } catch (err) { map = null; console.warn('Simulator map disabled:', err); showStaticMap(ui); return; }

    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'top-right');

    map.on('load', () => {
      mapReady = true;

      // Dynamic District Boundary Polygons (crisp outline + subtle RdBu fill)
      map.addSource('sim-zones', {
        type: 'geojson',
        data: buildDistrictZonesGeoJson(),
      });
      map.addLayer({
        id: 'sim-zones-fill',
        type: 'fill',
        source: 'sim-zones',
        paint: {
          'fill-color': ['get', 'color'],
          'fill-opacity': ['get', 'opacity'],
        },
      });
      map.addLayer({
        id: 'sim-zones-line',
        type: 'line',
        source: 'sim-zones',
        paint: {
          'line-color': ['get', 'strokeColor'],
          'line-width': ['get', 'strokeWidth'],
          'line-opacity': 0.92,
        },
      });

      // Roads/rails & canals backdrop from active basin assets.json
      map.addSource('infra-backdrop', {
        type: 'geojson',
        data: infraBackdropGeoJson || assetsGeoJson || { type: 'FeatureCollection', features: [] },
      });
      map.addLayer({
        id: 'infra-roads-rail',
        type: 'line',
        source: 'infra-backdrop',
        filter: ['!=', ['get', 'type'], 'canal'],
        paint: {
          'line-color': '#94a3b8',
          'line-width': ['match', ['get', 'type'], 'rail', 1.2, 0.9],
          'line-opacity': 0.28,
        },
      });

      // All canals backdrop subtle
      map.addLayer({
        id: 'infra-canals-base',
        type: 'line',
        source: 'infra-backdrop',
        filter: ['==', ['get', 'type'], 'canal'],
        paint: {
          'line-color': '#38bdf8',
          'line-width': 1.4,
          'line-opacity': 0.42,
        },
      });

      // Evaluated dynamic canals / corridors from assets.json
      map.addSource('infra-canals', {
        type: 'geojson',
        data: buildDynamicCanalsGeoJson(),
      });
      map.addLayer({
        id: 'infra-canals-risk',
        type: 'line',
        source: 'infra-canals',
        paint: {
          'line-color': ['get', 'simColor'],
          'line-width': 3.2,
          'line-opacity': 0.92,
        },
      });

      // Konya Karapinar documented sinkholes (29 features)
      map.addSource('karapinar-sinkholes', {
        type: 'geojson',
        data: sinkholesGeoJson || { type: 'FeatureCollection', features: [] },
      });
      map.addLayer({
        id: 'karapinar-sinkholes-layer',
        type: 'circle',
        source: 'karapinar-sinkholes',
        layout: {
          visibility: activeBasinId === 'konya' ? 'visible' : 'none',
        },
        paint: {
          'circle-radius': 5.5,
          'circle-color': 'rgba(230, 159, 0, 0.24)',
          'circle-stroke-color': '#e69f00',
          'circle-stroke-width': 1.6,
        },
      });

      rebuildMapMarkers();
      applyOverlayMode();
      refreshMapDynamicLayers();
    });
  }

  function applyOverlayMode() {
    if (!mapReady) return;
    if (overlayMode === 'sim') {
      map.setPaintProperty('nisar-raster', 'raster-opacity', 0.14);
      map.setLayoutProperty('sim-zones-fill', 'visibility', 'visible');
      map.setLayoutProperty('sim-zones-line', 'visibility', 'visible');
    } else if (overlayMode === 'blend') {
      map.setPaintProperty('nisar-raster', 'raster-opacity', 0.56);
      map.setLayoutProperty('sim-zones-fill', 'visibility', 'visible');
      map.setLayoutProperty('sim-zones-line', 'visibility', 'visible');
    } else {
      map.setPaintProperty('nisar-raster', 'raster-opacity', 0.86);
      map.setLayoutProperty('sim-zones-fill', 'visibility', 'none');
      map.setLayoutProperty('sim-zones-line', 'visibility', 'none');
    }
  }

  function refreshMapDynamicLayers() {
    if (mapReady) {
      const zSrc = map.getSource('sim-zones');
      if (zSrc) zSrc.setData(buildDistrictZonesGeoJson());
      const cSrc = map.getSource('infra-canals');
      if (cSrc) cSrc.setData(buildDynamicCanalsGeoJson());
    }
    simState.districts.forEach((d) => {
      const m = districtMarkers[d.id];
      if (!m) return;
      const valSpan = m.el.querySelector('.mval');
      if (valSpan) {
        valSpan.textContent = `${d.totalCm.toFixed(1)} cm`;
        valSpan.style.color = d.totalCm < -4 ? '#c8321f' : d.totalCm < -1 ? '#a86b00' : '#1f7a35';
      }
      m.el.classList.toggle('sel', d.id === selectedDistrictId);
    });
  }

  /**
   * Draw an animated SVG zigzag crack line & trigger a micro-tremor over damaged canal locations.
   */
  function triggerCanalCrackAnimation(district) {
    const svg = $('fxSvg');
    const stage = $('mapStage');
    if (stage) {
      stage.classList.remove('tremor');
      void stage.offsetWidth;
      stage.classList.add('tremor');
      setTimeout(() => stage.classList.remove('tremor'), 280);
    }
    if (!mapReady || !svg || !district) return;
    const pt = map.project([district.lon, district.lat]);
    if (!pt || pt.x < 0 || pt.y < 0) return;

    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    const x = pt.x;
    const y = pt.y;
    const dStr = `M ${x - 28} ${y - 18} L ${x - 10} ${y - 6} L ${x - 15} ${y + 4} L ${x + 3} ${y + 2} L ${x + 12} ${y + 18} L ${x + 28} ${y + 12}`;
    path.setAttribute('d', dStr);
    path.setAttribute('class', 'crack-line');
    svg.appendChild(path);
    setTimeout(() => {
      if (path.parentNode) path.parentNode.removeChild(path);
    }, 950);
  }

  /**
   * Draw real-time stratigraphic cross-section on <canvas id="stratCanvas"> showing:
   * ground surface deflection, unconfined aquifer water table h, preconsolidation head h_pc,
   * Corcoran clay compression (elastic vs permanent layers), and wells turning dry.
   */
  function renderStratigraphy(d) {
    const canvas = $('stratCanvas');
    if (!canvas) return;
    const maxDpr = window.innerWidth < 900 ? 1.5 : 2;
    const dpr = Math.min(window.devicePixelRatio || 1, maxDpr);
    const rect = canvas.getBoundingClientRect();
    const w = Math.max(260, Math.round(rect.width || 360));
    const h = Math.max(110, Math.round(rect.height || 150));
    if (canvas.width !== w * dpr || canvas.height !== h * dpr) {
      canvas.width = w * dpr;
      canvas.height = h * dpr;
    }
    const ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);

    // Light palette matching the site: sky, sand, water, clay
    ctx.fillStyle = '#f3f5f8';
    ctx.fillRect(0, 0, w, h);

    const datumY = 24;
    // Exaggerate visual sag so 0..30 cm is clearly legible
    const sagPx = Math.min(20, Math.max(-2, -d.totalCm * 0.7));
    const permPx = Math.min(18, Math.max(0, -d.inelasticCm * 0.7));
    const elastPx = Math.max(0, sagPx - permPx);
    const sandBot = 86;

    // Sand above the clay, with a sagging surface
    const sagMidY = datumY + sagPx;
    ctx.fillStyle = '#efe6d2';
    ctx.beginPath();
    ctx.moveTo(0, datumY + 2);
    ctx.quadraticCurveTo(w * 0.5, sagMidY + 6, w, datumY + 2);
    ctx.lineTo(w, h);
    ctx.lineTo(0, h);
    ctx.closePath();
    ctx.fill();

    // Water depth mapped between 25 m and 95 m below the surface
    const mapDepthY = (headM) => {
      const depth = -headM;
      return Math.max(datumY + 6, Math.min(h - 8, datumY + 8 + ((depth - 25) / 70) * (h - datumY - 20)));
    };
    const wtY = mapDepthY(d.headM);
    const hpcY = mapDepthY(d.preconsolidationHeadM);

    // Wet sand below the water level
    ctx.fillStyle = '#d3e3f3';
    ctx.fillRect(0, wtY, w, h - wtY);

    // Clay layer (thinner where squeezed)
    const clayTop = sandBot + sagPx * 0.3;
    const baseClayPx = Math.max(14, Math.min(34, d.clayThicknessM * 0.4));
    const currentClayPx = Math.max(8, baseClayPx - sagPx * 0.55);
    ctx.fillStyle = '#b9926a';
    ctx.fillRect(0, clayTop, w, currentClayPx);
    if (elastPx > 0.3) {
      ctx.fillStyle = 'rgba(47, 127, 209, 0.45)';
      ctx.fillRect(0, clayTop, w, Math.min(10, elastPx + 1.5));
    }
    if (permPx > 0.3) {
      ctx.fillStyle = 'rgba(200, 50, 31, 0.85)';
      ctx.fillRect(0, clayTop + currentClayPx - Math.min(14, permPx), w, Math.min(14, permPx));
    }

    // Original ground level
    ctx.save();
    ctx.setLineDash([4, 4]);
    ctx.strokeStyle = '#9aa6b8';
    ctx.beginPath();
    ctx.moveTo(0, datumY);
    ctx.lineTo(w, datumY);
    ctx.stroke();
    ctx.restore();

    // Ground surface
    ctx.strokeStyle = '#6b5a3e';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, datumY + 2);
    ctx.quadraticCurveTo(w * 0.5, sagMidY + 6, w, datumY + 2);
    ctx.stroke();

    // Lowest level ever (h_pc)
    ctx.save();
    ctx.setLineDash([6, 4]);
    ctx.strokeStyle = '#e69f00';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    ctx.moveTo(0, hpcY);
    ctx.lineTo(w, hpcY);
    ctx.stroke();
    ctx.restore();

    // Water level
    ctx.strokeStyle = '#0b3d91';
    ctx.lineWidth = 2.2;
    ctx.beginPath();
    ctx.moveTo(0, wtY);
    ctx.lineTo(w, wtY);
    ctx.stroke();

    // Up to 5 representative wells
    const sampleWells = d.wellDepthsM.slice(0, 5);
    sampleWells.forEach((wd, idx) => {
      const wx = 46 + idx * ((w - 92) / Math.max(1, sampleWells.length - 1));
      const wellBotY = mapDepthY(-wd);
      const isDry = -d.headM >= wd;
      ctx.strokeStyle = isDry ? '#c8321f' : '#3f4a5a';
      ctx.lineWidth = 2.4;
      ctx.beginPath();
      ctx.moveTo(wx, datumY + 2);
      ctx.lineTo(wx, wellBotY);
      ctx.stroke();
      ctx.fillStyle = isDry ? '#c8321f' : '#3f4a5a';
      ctx.fillRect(wx - 4, datumY - 4, 8, 6);
    });

    // Labels
    ctx.font = '600 11.5px Inter, system-ui, sans-serif';
    ctx.fillStyle = '#4a5568';
    ctx.fillText('Ground', 8, 15);
    ctx.textAlign = 'right';
    ctx.fillStyle = d.totalCm < -0.05 ? '#c8321f' : '#1a1f29';
    ctx.fillText(`${d.totalCm.toFixed(1)} cm`, w - 8, 15);
    ctx.textAlign = 'left';
    ctx.fillStyle = '#0b3d91';
    ctx.fillText(`Water ${d.headM.toFixed(1)} m`, 8, Math.max(datumY + 18, wtY - 5));
    ctx.textAlign = 'right';
    ctx.fillStyle = '#8a5a00';
    ctx.fillText(`Lowest ${d.preconsolidationHeadM.toFixed(1)} m`, w - 8, Math.min(h - 6, hpcY + 14));
    ctx.textAlign = 'left';

    const pill = $('stratRegimePill');
    if (pill) {
      const inVirgin = d.headM <= d.preconsolidationHeadM + 0.05;
      pill.textContent = inVirgin ? 'Permanent squeeze' : 'Springs back';
      pill.style.color = inVirgin ? '#c8321f' : '#1f7a35';
      pill.style.background = inVirgin ? '#fbe9e6' : '#e7f4ec';
      pill.style.borderColor = inVirgin ? '#f0c2ba' : '#b9dcc5';
    }
  }

  /**
   * Initialize and update Chart.js 4.4.1 bottom timeline comparing selected district subsidence vs 2026 NISAR.
   */
  function updateTimelineChart(d) {
    const canvas = $('timelineChart');
    if (!canvas || typeof Chart === 'undefined') return;

    const labels = ['Start'];
    for (let i = 0; i < ValleyModel.CONFIG.totalMonths; i++) {
      const m = ValleyModel.MONTH_NAMES[i % 12];
      const y = 26 + Math.floor((9 + i) / 12);
      labels.push(`${m} '${y}`);
    }

    const hist = d.history || [];
    const totalSeries = [0, ...hist.map((h) => h.totalCm)];
    const permSeries = [0, ...hist.map((h) => h.inelasticCm)];
    const nisarVertRef = Number(ValleyModel.losToVertical(d.nisarLosCm, simState.incidenceDeg).toFixed(2));
    const nisarRefLine = labels.map((_, idx) => (idx <= 1 ? null : nisarVertRef));

    if (typeof Chart === 'undefined') return;
    if (!timelineChart) {
      timelineChart = new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Total sinking',
              data: totalSeries,
              borderColor: '#0b3d91',
              backgroundColor: 'rgba(11, 61, 145, 0.08)',
              borderWidth: 2.4,
              tension: 0.25,
              pointRadius: 3,
              pointBackgroundColor: '#0b3d91',
            },
            {
              label: 'Permanent',
              data: permSeries,
              borderColor: '#c8321f',
              backgroundColor: 'rgba(200, 50, 31, 0.14)',
              fill: true,
              borderWidth: 2.4,
              tension: 0.25,
              pointRadius: 2.5,
              pointBackgroundColor: '#c8321f',
            },
            {
              label: 'NISAR 2026',
              data: nisarRefLine,
              borderColor: '#a86b00',
              borderDash: [6, 4],
              borderWidth: 1.8,
              pointRadius: 0,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: false,
          interaction: { mode: 'index', intersect: false },
          plugins: {
            legend: {
              display: false,
              position: 'top',
              align: 'start',
              labels: { color: '#4a5568', boxWidth: 12, boxHeight: 3, font: { size: 12, family: 'Inter' }, padding: 12 },
            },
            tooltip: { titleFont: { family: 'Inter' }, bodyFont: { family: 'Inter' } },
          },
          scales: {
            x: {
              min: 0,
              max: CHART_WINDOW,
              ticks: { color: '#4a5568', font: { size: 11.5, family: 'Inter' }, autoSkip: true, maxRotation: 0 },
              grid: { color: '#eef1f5' },
            },
            y: {
              title: { display: true, text: 'cm', color: '#6b7687', font: { size: 11.5, family: 'Inter' } },
              ticks: { color: '#4a5568', font: { size: 11.5, family: 'IBM Plex Mono' } },
              grid: { color: '#eef1f5' },
              suggestedMin: -16,
              suggestedMax: 1,
            },
          },
        },
      });
    } else {
      timelineChart.data.datasets[0].data = totalSeries;
      timelineChart.data.datasets[1].data = permSeries;
      timelineChart.data.datasets[2].data = nisarRefLine;
      timelineChart.data.datasets[2].label = `NISAR 2026 (${nisarVertRef} cm vertical)`;
    }
    // show a 12-month window that follows the current month unless the user has dragged it
    const last = labels.length - 1;
    const follow = Math.min(Math.max(0, hist.length - CHART_WINDOW + 2), last - CHART_WINDOW);
    const start = chartStart === null ? follow : Math.max(0, Math.min(chartStart, last - CHART_WINDOW));
    timelineChart.options.scales.x.min = start;
    timelineChart.options.scales.x.max = start + CHART_WINDOW;
    timelineChart.update('none');

    $('chartTitle').textContent = `${d.shortName} vs NISAR 2026`;
  }

  // drag or scroll the timeline to move through the 24 months
  function wireChartPan() {
    const wrap = document.querySelector('.timeline-canvas-wrap');
    if (!wrap) return;
    const total = ValleyModel.CONFIG.totalMonths;
    const current = () => (timelineChart ? timelineChart.options.scales.x.min : 0);
    const setStart = (v) => {
      chartStart = Math.max(0, Math.min(Math.round(v), total - CHART_WINDOW));
      const d = simState && (simState.districts.find((x) => x.id === selectedDistrictId) || simState.districts[0]);
      if (d) updateTimelineChart(d);
    };
    let drag = null;
    wrap.addEventListener('pointerdown', (e) => {
      drag = { x: e.clientX, start: current(), w: wrap.clientWidth };
      wrap.classList.add('dragging');
      wrap.setPointerCapture(e.pointerId);
    });
    wrap.addEventListener('pointermove', (e) => {
      if (!drag) return;
      const perMonth = drag.w / CHART_WINDOW;
      setStart(drag.start - (e.clientX - drag.x) / perMonth);
    });
    const end = () => { drag = null; wrap.classList.remove('dragging'); };
    wrap.addEventListener('pointerup', end);
    wrap.addEventListener('pointercancel', end);
    wrap.addEventListener('wheel', (e) => {
      const delta = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
      if (!delta) return;
      e.preventDefault();
      setStart(current() + Math.sign(delta));
    }, { passive: false });
  }

  function selectDistrict(districtId, flyTo) {
    selectedDistrictId = districtId;
    const d = simState.districts.find((x) => x.id === districtId) || simState.districts[0];
    if (flyTo && mapReady) {
      map.easeTo({ center: [d.lon, d.lat], duration: 380 });
    }
    syncUI();
  }

  function syncUI() {
    if (!simState) return;
    const d = simState.districts.find((x) => x.id === selectedDistrictId) || simState.districts[0];
    const wySpec = ValleyModel.getWaterYearSpec(simState.currentWaterYear);

    // Header Pills: Month X of 24 · Date · Season
    const moIdx = simState.monthStep;
    const calLabel = moIdx === 0 ? 'Oct 2026' : simState.valleyHistory[moIdx - 1].label;
    const seasonTag = /^(Dec|Jan|Feb)/.test(calLabel)
      ? 'Winter · wet recharge'
      : /^(Mar|Apr|May)/.test(calLabel)
      ? 'Spring · snowmelt'
      : /^(Jun|Jul|Aug)/.test(calLabel)
      ? 'Summer · peak pumping'
      : 'Autumn · early year';
    $('monthPill').textContent = `Month ${moIdx} of ${simState.totalMonths} · ${seasonTag}`;
    $('stampDate').textContent = calLabel.toUpperCase();

    const wyYearNum = moIdx < 12 ? 1 : 2;
    const wyPill = $('wyPill');
    wyPill.textContent = `WY${wyYearNum}: ${wySpec.label} (${wySpec.maxSurfacePct}% Surface Cap)`;
    wyPill.className = 'pill ' + (
      wySpec.id === 'Wet' ? 'wy-wet' :
      wySpec.id === 'Above Normal' ? 'wy-above' :
      wySpec.id === 'Dry' ? 'wy-dry' :
      wySpec.id === 'Critical' ? 'wy-critical' : 'wy-below'
    );

    $('sinkholeLegendItem').hidden = activeBasinId !== 'konya';


    // Sliders, ARIA valuetext & Dynamic Surface Cap
    $('pumpSlider').value = d.controls.pumpingPct;
    $('pumpSlider').setAttribute('aria-valuetext', `${d.controls.pumpingPct} percent of baseline pumping`);
    $('pumpVal').textContent = `${d.controls.pumpingPct}%`;
    $('surfaceSlider').max = wySpec.maxSurfacePct;
    const cappedSurface = Math.min(d.controls.surfaceAllocPct, wySpec.maxSurfacePct);
    $('surfaceSlider').value = cappedSurface;
    $('surfaceSlider').setAttribute('aria-valuetext', `${cappedSurface} percent canal and recharge allocation`);
    $('surfaceVal').textContent = `${cappedSurface}%`;
    $('fallowSlider').value = d.controls.fallowPct;
    $('fallowSlider').setAttribute('aria-valuetext', `${d.controls.fallowPct} percent land fallowed`);
    $('fallowVal').textContent = `${d.controls.fallowPct}%`;

    // District KPIs: 3 primary readouts + quiet secondary strip (Okabe-Ito + text tags)
    const isVirgin = d.headM <= d.preconsolidationHeadM + 0.05;
    $('kpiDistrictTitle').textContent = `Readout: ${d.shortName}`;
    $('kpiTotalCm').textContent = `${d.totalCm.toFixed(2)} cm`;
    $('kpiSplitCm').textContent = `Elastic: ${d.elasticCm.toFixed(2)} cm`;
    $('kpiPermCm').textContent = `${d.inelasticCm.toFixed(2)} cm`;
    $('kpiRegimeSub').textContent = isVirgin ? 'Collapsing' : 'Springs back';
    $('kpiRegimeSub').style.color = isVirgin ? '#c8321f' : '#1f7a35';

    $('kpiRevenue').textContent = `$${d.cumulativeRevenueMUsd.toFixed(1)}M`;
    $('kpiRevSub').textContent = `${100 - d.controls.fallowPct}% cropped`;

    // Events
    if (simState.events.length > 0) {
      $('eventList').innerHTML = simState.events
        .map(
          (ev) => `<div class="event-item ${ev.severity || ''}">
            <div class="event-title">${ev.title}</div>
            <div>${ev.detail}</div>
            <div class="event-src">Source: ${ev.source}</div>
          </div>`
        )
        .join('');
    }

    // Turn button states
    $('nextMonthBtn').disabled = simState.finished;
    $('fastForwardBtn').disabled = simState.finished;
    $('nextMonthBtn').textContent = simState.finished ? '24 Months Complete' : 'Advance one month →';

    renderStratigraphy(d);
    updateTimelineChart(d);
    refreshMapDynamicLayers();
    refreshVSliders();
    setSeg($('presetSeg'), activePreset);
  }

  /* ---------- sliding segmented controls ---------- */
  function setSeg(seg, value) {
    if (!seg) return;
    const btns = [...seg.querySelectorAll('.seg-btn')];
    const key = (b) => b.dataset.preset || b.dataset.basin || b.dataset.tab;
    btns.forEach((b) => b.classList.toggle('active', key(b) === value));
    const on = btns.find((b) => key(b) === value);
    const thumb = seg.querySelector('.seg-thumb');
    seg.classList.toggle('none', !on);
    if (!on || !thumb) return;
    // the dark bar is a little shorter than the button it sits under
    const inset = 4;
    const first = !seg.dataset.placed && on.offsetWidth > 0;
    if (first) thumb.style.transition = 'none'; // first placement jumps; later changes slide
    thumb.style.width = `${on.offsetWidth - inset * 2}px`;
    thumb.style.transform = `translateX(${on.offsetLeft + inset}px)`;
    if (first) { void thumb.offsetWidth; thumb.style.transition = ''; seg.dataset.placed = '1'; }
  }

  /* ---------- vertical sliders (the hidden range inputs stay the source of truth) ---------- */
  const vsliders = [];
  function initVSliders() {
    document.querySelectorAll('.vs').forEach((wrap) => {
      const input = $(wrap.dataset.for);
      const track = wrap.querySelector('.vs-track');
      const handle = wrap.querySelector('.vs-handle');
      const fill = wrap.querySelector('.vs-fill');
      const cap = wrap.querySelector('.vs-cap');
      const canvas = wrap.querySelector('.vs-water');
      const full = Number(input.getAttribute('max')); // scale stays fixed even when the water-year cap lowers input.max
      const vs = { wrap, input, track, handle, fill, cap, canvas, full, level: Number(input.value) / full, cols: null };
      const setFromY = (clientY) => {
        const r = track.getBoundingClientRect();
        const frac = 1 - (clientY - r.top) / r.height;
        const step = Number(input.step) || 1;
        let v = Math.round((frac * full) / step) * step;
        v = Math.max(Number(input.min), Math.min(Number(input.max), v));
        if (String(v) !== input.value) {
          input.value = v;
          input.dispatchEvent(new Event('input', { bubbles: true }));
        }
        draw(vs);
      };
      track.addEventListener('pointerdown', (e) => { track.setPointerCapture(e.pointerId); vs.drag = true; setFromY(e.clientY); });
      track.addEventListener('pointermove', (e) => { if (vs.drag) setFromY(e.clientY); });
      track.addEventListener('pointerup', () => { vs.drag = false; });
      track.addEventListener('pointercancel', () => { vs.drag = false; });
      track.addEventListener('keydown', (e) => {
        const step = Number(input.step) || 1;
        const map = { ArrowUp: step, ArrowRight: step, ArrowDown: -step, ArrowLeft: -step, PageUp: step * 4, PageDown: -step * 4 };
        let v = Number(input.value);
        if (e.key in map) v += map[e.key];
        else if (e.key === 'Home') v = Number(input.min);
        else if (e.key === 'End') v = Number(input.max);
        else return;
        e.preventDefault();
        v = Math.max(Number(input.min), Math.min(Number(input.max), v));
        input.value = v;
        input.dispatchEvent(new Event('input', { bubbles: true }));
        draw(vs);
      });
      vsliders.push(vs);
    });
    requestAnimationFrame(waterLoop);
  }
  function draw(vs) {
    const v = Number(vs.input.value);
    const frac = Math.max(0, Math.min(1, v / vs.full));
    vs.target = frac;
    vs.handle.style.top = `${(1 - frac) * 100}%`;
    if (vs.fill) vs.fill.style.height = `${frac * 100}%`;
    if (vs.cap) vs.cap.style.height = `${(1 - Number(vs.input.max) / vs.full) * 100}%`;
    vs.track.setAttribute('aria-valuemin', vs.input.min);
    vs.track.setAttribute('aria-valuemax', vs.input.max);
    vs.track.setAttribute('aria-valuenow', String(v));
    vs.track.setAttribute('aria-valuetext', vs.input.getAttribute('aria-valuetext') || `${v} percent`);
  }
  function refreshVSliders() { vsliders.forEach(draw); }

  // a few dozen springs make the water surface slosh when the level changes
  const still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function waterLoop() {
    vsliders.forEach((vs) => {
      if (!vs.canvas) return;
      const c = vs.canvas;
      const w = c.clientWidth, h = c.clientHeight;
      if (!w || !h) return;
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      if (c.width !== Math.round(w * dpr)) { c.width = Math.round(w * dpr); c.height = Math.round(h * dpr); }
      const N = 18;
      if (!vs.cols) vs.cols = Array.from({ length: N }, () => ({ y: 0, v: 0 }));
      const target = vs.target ?? vs.level;
      const prev = vs.level;
      vs.level += (target - vs.level) * (still ? 1 : 0.18);
      const push = (vs.level - prev) * h * 0.9;
      if (!still && Math.abs(push) > 0.01) {
        vs.cols[0].v += push; vs.cols[N - 1].v -= push * 0.6; vs.cols[Math.floor(N / 2)].v += push * 0.3;
      }
      for (let k = 0; k < 2; k++) {
        vs.cols.forEach((col) => { col.v += -0.06 * col.y; col.v *= 0.94; col.y += col.v; });
        for (let i = 0; i < N; i++) {
          const l = vs.cols[i - 1], r = vs.cols[i + 1];
          if (l) vs.cols[i].v += 0.12 * (l.y - vs.cols[i].y);
          if (r) vs.cols[i].v += 0.12 * (r.y - vs.cols[i].y);
        }
      }
      if (still) vs.cols.forEach((col) => { col.y = 0; col.v = 0; });
      const ctx = c.getContext('2d');
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, w, h);
      const top = (1 - vs.level) * h;
      const t = performance.now() / 900;
      ctx.beginPath();
      ctx.moveTo(0, h);
      for (let i = 0; i < N; i++) {
        const x = (i / (N - 1)) * w;
        const ripple = still ? 0 : Math.sin(t + i * 0.7) * 1.2;
        ctx.lineTo(x, Math.max(0, top + vs.cols[i].y + ripple));
      }
      ctx.lineTo(w, h);
      ctx.closePath();
      const g = ctx.createLinearGradient(0, top, 0, h);
      g.addColorStop(0, '#5aa2e6');
      g.addColorStop(1, '#0b3d91');
      ctx.fillStyle = g;
      ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,.65)';
      ctx.lineWidth = 2;
      ctx.beginPath();
      for (let i = 0; i < N; i++) {
        const x = (i / (N - 1)) * w;
        const ripple = still ? 0 : Math.sin(t + i * 0.7) * 1.2;
        const y = Math.max(0, top + vs.cols[i].y + ripple);
        if (i) ctx.lineTo(x, y); else ctx.moveTo(x, y);
      }
      ctx.stroke();
    });
    requestAnimationFrame(waterLoop);
  }

  function showEndModal() {
    const worst = [...simState.districts].sort((a, b) => a.totalCm - b.totalCm)[0];
    const totalRev = simState.districts.reduce((s, x) => s + x.cumulativeRevenueMUsd, 0);
    const totalDry = simState.districts.reduce((s, x) => s + x.dryWells, 0);
    const maxCanalLoss = simState.districts.reduce((m, x) => Math.max(m, x.canalCapacityLossPct), 0);

    $('endYourTotal').textContent = `${worst.totalCm.toFixed(1)} cm (${worst.shortName})`;
    $('endYourPerm').textContent = `${worst.inelasticCm.toFixed(1)} cm (${Math.abs(worst.totalCm) > 0.1 ? Math.round((worst.inelasticCm / worst.totalCm) * 100) : 0}% irreversible)`;
    $('endYourCanal').textContent = `${maxCanalLoss.toFixed(1)}%`;
    $('endYourWells').textContent = `${totalDry} wells`;
    $('endYourRev').textContent = `$${totalRev.toFixed(1)}M`;

    const ui = BASIN_UI[activeBasinId] || BASIN_UI.tulare;
    const basinCfg = ValleyModel.getBasinConfig(activeBasinId);
    const measuredLos = summaryData ? summaryData.max_subsidence_cm : basinCfg.targetMeasuredLosCm;
    const measuredVert = summaryData ? summaryData.max_subsidence_vertical_cm_estimate : basinCfg.targetMeasuredVertCm;
    const rate = summaryData ? summaryData.rate_cm_per_yr_estimate : (activeBasinId === 'konya' ? -20.0 : -26.4);
    $('endNisarLos').textContent = `${measuredLos} cm`;
    $('endNisarVert').textContent = `~${measuredVert} cm`;
    $('endNisarRate').textContent = `${rate} cm/yr LOS`;
    $('endNisarAssets').textContent = ui.endAssetsText;
    $('endNisarValLabel').textContent = ui.endValLabel;
    $('endNisarVal').textContent = ui.endValText;

    const sinkNote = activeBasinId === 'konya' && simState.sinkholeRiskActive ? ' Sinkhole risk indicators are elevated near mapped obruks (indicator only).' : '';
    let takeaway = '';
    if (Math.abs(worst.inelasticCm) >= 12) {
      takeaway = `What this means: Heavy groundwater pumping dropped levels past historical lows, locking in ${worst.inelasticCm.toFixed(1)} cm of permanent clay collapse near ${worst.shortName}. Even future wet winters cannot restore that lost underground pore storage.${sinkNote}`;
    } else if (Math.abs(worst.inelasticCm) <= 4) {
      takeaway = `What this means: Limiting groundwater extraction balanced winter recharge and kept permanent collapse to ${worst.inelasticCm.toFixed(1)} cm across the basin. Surface corridor gradients stayed within safe design limits.`;
    } else {
      takeaway = `What this means: Summer irrigation temporarily pushed hotspots past historical lows, causing ${worst.inelasticCm.toFixed(1)} cm of permanent clay collapse near ${worst.shortName}. Reducing summer pumping peaks before dry years protects surface corridors and shallow wells.${sinkNote}`;
    }
    $('endMeaning').textContent = takeaway;

    const qdBanner = $('quickDemoBanner');
    const qdText = $('quickDemoSummaryText');
    if (qdBanner && qdText) {
      if (activePreset === 'overpump' || isQuickDemo) {
        const baselineRef = activeBasinId === 'konya' ? 8.0 : 10.1;
        const worstSinkAbs = Math.abs(worst.totalCm);
        const deltaSink = Math.max(0, worstSinkAbs - baselineRef);
        const permSink = Math.abs(worst.inelasticCm);
        qdText.textContent = `Pumping 50% more → ${deltaSink.toFixed(1)} cm more sinking, ${permSink.toFixed(1)} cm of it permanent.`;
        qdBanner.hidden = false;
      } else {
        qdBanner.hidden = true;
      }
    }

    $('endModal').hidden = false;
    renderEndCompareChart();
  }

  function renderEndCompareChart() {
    const canvas = $('endCompareChart');
    if (!canvas || !window.Chart || !simState) return;
    const labels = simState.districts.map((d) => d.shortName);
    const simTotal = simState.districts.map((d) => Number(Math.abs(d.totalCm).toFixed(2)));
    const simPerm = simState.districts.map((d) => Number(Math.abs(d.inelasticCm).toFixed(2)));
    const nisarVert = simState.districts.map((d) =>
      Number(Math.abs(ValleyModel.losToVertical(d.nisarLosCm, simState.incidenceDeg)).toFixed(2))
    );

    if (endCompareChart) {
      endCompareChart.destroy();
      endCompareChart = null;
    }

    if (typeof Chart === 'undefined') return;
    endCompareChart = new Chart(canvas.getContext('2d'), {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Your 24-Mo Total Sink (cm)',
            data: simTotal,
            backgroundColor: 'rgba(11, 61, 145, 0.85)',
            borderColor: '#0b3d91',
            borderWidth: 1,
          },
          {
            label: 'Your Permanent Collapse (cm)',
            data: simPerm,
            backgroundColor: 'rgba(200, 50, 31, 0.85)',
            borderColor: '#c8321f',
            borderWidth: 1,
          },
          {
            label: '2026 NISAR 108-Day Est. (cm)',
            data: nisarVert,
            backgroundColor: 'rgba(232, 168, 56, 0.85)',
            borderColor: '#a86b00',
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        plugins: {
          legend: {
            position: 'top',
            labels: { color: '#4a5568', boxWidth: 11, font: { size: 10.5 }, padding: 8 },
          },
        },
        scales: {
          x: {
            ticks: { color: '#4a5568', font: { size: 10.5 } },
            grid: { display: false },
          },
          y: {
            beginAtZero: true,
            title: { display: true, text: 'Subsidence magnitude (cm)', color: '#4a5568', font: { size: 10.5 } },
            ticks: { color: '#4a5568', font: { size: 10 } },
            grid: { color: '#eef1f5' },
          },
        },
      },
    });
  }

  function advanceMonths(count) {
    if (!simState || simState.finished) return;
    chartStart = null;
    let damagedDistrict = null;
    let hadWarn = false;
    for (let i = 0; i < count && !simState.finished; i++) {
      const res = ValleyModel.stepMonth(simState);
      if (res.newEvents && res.newEvents.length) {
        const canalEv = res.newEvents.find((e) => e.id.startsWith('canal-'));
        if (canalEv) {
          const did = canalEv.id.split('-')[1];
          damagedDistrict = simState.districts.find((x) => x.id === did) || simState.districts[0];
          hadWarn = true;
        }
      }
    }
    playTone(hadWarn ? 'warn' : 'click');
    if (damagedDistrict) {
      triggerCanalCrackAnimation(damagedDistrict);
    }
    syncUI();
    if (simState.finished) {
      showEndModal();
    }
  }

  function buildParamsTableHtml() {
    const cal = ValleyModel.runCalibrationCheck(summaryData, activeBasinId);
    const basinCfg = ValleyModel.getBasinConfig(activeBasinId);
    const p = ValleyModel.CONFIG.physics;
    const rows = [
      ['Model Check Factor (k)', `${cal.calibrationFactor}`, `Multiplier (${basinCfg.shortLabel} 108-day benchmark)`, `Calibrated to ${basinCfg.summaryPath} (${cal.measuredVertCm} cm vert / ${cal.measuredLosCm} cm LOS)`, false],
      ['Specific Yield (S_y)', `${p.specificYield.value}`, p.specificYield.unit, p.specificYield.source, p.specificYield.illustrative],
      ['Elastic Skeletal Storage (S_ske)', `${p.elasticSpecificStorage.value}`, p.elasticSpecificStorage.unit, p.elasticSpecificStorage.source, p.elasticSpecificStorage.illustrative],
      ['Inelastic Skeletal Storage (S_skv)', `${p.inelasticSpecificStorage.value}`, p.inelasticSpecificStorage.unit, p.inelasticSpecificStorage.source, p.inelasticSpecificStorage.illustrative],
      ['Compressible Clay Interbeds (b0)', '12–82 m across districts', 'Aggregate thickness', 'CVHM SUB aggregate interbeds (Corcoran Clay alone <= 61 m per Page 1986)', true],
      ['Water Year Probabilities & Caps', 'DWR 5-class weights (15–100% cap)', 'Probability / %', 'Formula from DWR WSIHIST; class probabilities illustrative', true],
      ['Baseline Demand / Recharge', `${p.baselineAnnualDemandM.value} / ${p.baselineAnnualRechargeM.value}`, 'm/yr eq', p.baselineAnnualDemandM.source, true],
      ['Canal Capacity Loss Curve', 'Up to 60% above 10 mm/km', '% conveyance drop', 'Friant-Kern >60% capacity loss verified (FWA/KVPR); onset threshold illustrative', true],
      ['Well Failure Depths & Crop Prices', 'Representative depths & $/ha', 'wells / USD', 'Stylized regional baseline per district', true],
    ];
    return `<div class="sources-ref-box">
      <h3>NASA Space Apps Challenge Resources &amp; Land Subsidence StoryMap Framework</h3>
      <p style="margin:0 0 6px;">
        <strong>1. NASA NISAR Land Subsidence StoryMap (2013–2017 UAVSAR → 2026 Spaceborne NISAR):</strong>
        NASA's official <a href="https://storymaps.arcgis.com/stories/109e602e748346f3be8dc89124619828" target="_blank" rel="noopener">NISAR Land Subsidence StoryMap</a>
        (Peacock, A., An, K., Pinto, N., &amp; Lou, Y., 2024, <em>NISAR ArcGIS Storymaps</em>, Zenodo, <a href="https://doi.org/10.5281/zenodo.10818833" target="_blank" rel="noopener">doi:10.5281/zenodo.10818833</a>)
        demonstrated with airborne L-band UAVSAR that groundwater pumping in California's Central Valley formed a deep subsidence bowl and sank segments of the <strong>California Aqueduct</strong> by more than 40 inches (&gt;100 cm, or ~20–25 cm/yr) between 2013 and 2017 (Miller et al. 2020; Jones et al. 2020).
        Our 2026 simulator and risk dossier extend that exact framework from space using provisional NISAR L2 GUNW radar (recording −7.42 cm LOS / 49.12 mm/km tilt along the California Aqueduct in 108 summer days), GPS validation, and OpenStreetMap conveyance networks.
      </p>
      <ul>
        <li><strong>NISAR Applications White Papers (<a href="https://science.nasa.gov/mission/nisar/societal-benefits/" target="_blank" rel="noopener">NASA Societal Benefits</a>):</strong>
          <a href="https://assets.science.nasa.gov/content/dam/science/missions/nisar/nisar-jpl/pdf/NISAR_Applications_Subsidence.pdf" target="_blank" rel="noopener">Subsidence</a> (early centimetre-scale deformation monitoring),
          <a href="https://assets.science.nasa.gov/content/dam/science/missions/nisar/nisar-jpl/pdf/NISAR_Applications_Drought_and_Groundwater_Withdrawal1.pdf" target="_blank" rel="noopener">Drought &amp; Groundwater Withdrawal</a> (surface-water curtailment → pumping → clay compaction),
          <a href="https://assets.science.nasa.gov/content/dam/science/missions/nisar/nisar-jpl/pdf/NISAR_Applications_Sinkholes1.pdf" target="_blank" rel="noopener">Sinkholes &amp; Cavern Collapse</a> (precursor deformation in carbonate terrains such as Karapınar, indicator only),
          <a href="https://assets.science.nasa.gov/content/dam/science/missions/nisar/nisar-jpl/pdf/NISAR_Applications_Levees_and_Dams1.pdf" target="_blank" rel="noopener">Levees &amp; Dams</a>, and
          <a href="https://assets.science.nasa.gov/content/dam/science/missions/nisar/nisar-jpl/pdf/NISAR_Applications_Soil_Moisture_and_Water_Resources.pdf" target="_blank" rel="noopener">Soil Moisture &amp; Water Resources</a>.
        </li>
        <li><strong>NISAR Data User Guide &amp; SAR Education:</strong>
          <a href="https://nisar-docs.asf.alaska.edu/" target="_blank" rel="noopener">ASF NISAR Data User Guide</a>,
          <a href="https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/sar" target="_blank" rel="noopener">NASA Earthdata Intro to SAR</a>,
          <a href="https://appliedsciences.nasa.gov/get-involved/training" target="_blank" rel="noopener">NASA ARSET SAR Trainings</a>, and
          <a href="https://uavsar.jpl.nasa.gov/education/postcards.html" target="_blank" rel="noopener">NASA/JPL UAVSAR Postcards</a>.
        </li>
      </ul>
    </div>
    <table class="param-table">
      <thead><tr><th>Parameter</th><th>Value</th><th>Provenance / Tag</th></tr></thead>
      <tbody>${rows
        .map(
          (r) => `<tr>
            <td><strong>${r[0]}</strong></td>
            <td class="mono">${r[1]} <span style="color:var(--muted)">(${r[2]})</span></td>
            <td><span class="pill ${r[4] ? 'illustrative' : 'wy-wet'}">${r[4] ? 'ILLUSTRATIVE' : 'SOURCED'}</span><br><span style="color:var(--muted);font-size:11px;">${r[3]}</span></td>
          </tr>`
        )
        .join('')}
      </tbody>
    </table>`;
  }

  const CLASSROOM_SCENARIOS = {
    normal: {
      id: 'normal',
      label: 'Scenario 1: Normal Year (Below Normal → Above Normal · 100% Pump)',
      year1WaterYear: 'Below Normal',
      year2WaterYear: 'Above Normal',
      pumpingPct: 100,
      surfaceAllocPct: 70,
      fallowPct: 0,
    },
    drought: {
      id: 'drought',
      label: 'Scenario 2: Multi-Year Drought (Dry → Critical · 140% Pump)',
      year1WaterYear: 'Dry',
      year2WaterYear: 'Critical',
      pumpingPct: 140,
      surfaceAllocPct: 20,
      fallowPct: 0,
    },
    sustainable: {
      id: 'sustainable',
      label: 'Scenario 3: Sustainable Pumping (Below Normal → Dry · 55% Pump · 25% Fallow)',
      year1WaterYear: 'Below Normal',
      year2WaterYear: 'Dry',
      pumpingPct: 55,
      surfaceAllocPct: 85,
      fallowPct: 25,
    },
  };

  function runClassroomScenario(scenKey) {
    const spec = CLASSROOM_SCENARIOS[scenKey];
    if (!spec) return;
    const ui = BASIN_UI[activeBasinId] || BASIN_UI.tulare;
    const hydrated = ValleyModel.hydrateFromRepoData(pointsData, summaryData, activeBasinId);
    simState = ValleyModel.createSimulationState({
      basinId: activeBasinId,
      districts: hydrated.districts,
      summaryData: hydrated.summaryData,
      year1WaterYear: spec.year1WaterYear,
      year2WaterYear: spec.year2WaterYear,
    });
    selectedDistrictId = simState.districts[0].id;
    applyAll = true;
    if ($('applyAllChk')) $('applyAllChk').checked = true;
    ValleyModel.setDistrictControls(simState, 'ALL', {
      pumpingPct: spec.pumpingPct,
      surfaceAllocPct: spec.surfaceAllocPct,
      fallowPct: spec.fallowPct,
    });
    document.querySelectorAll('.classroom-scen-btn').forEach((b) => {
      b.classList.toggle('active', b.dataset.classroom === scenKey);
    });
    activePreset = null;
    if ($('classroomModal')) $('classroomModal').hidden = true;
    if ($('startModal')) $('startModal').hidden = true;
    if ($('endClassroomBox')) $('endClassroomBox').hidden = false;
    if ($('endClassroomScenarioTag')) {
      $('endClassroomScenarioTag').textContent = `${ui.shortLabel} · ${spec.label}`;
    }
    advanceMonths(24);
  }

  function resetSimulation(keepModalHidden) {
    const ui = BASIN_UI[activeBasinId] || BASIN_UI.tulare;
    const hydrated = ValleyModel.hydrateFromRepoData(pointsData, summaryData, activeBasinId);
    simState = ValleyModel.createSimulationState({
      basinId: activeBasinId,
      districts: hydrated.districts,
      summaryData: hydrated.summaryData,
      year1WaterYear: 'Below Normal',
    });
    selectedDistrictId = simState.districts[0].id;
    chartStart = null;
    // start from the 2026 baseline scenario (the same settings the NISAR calibration uses)
    activePreset = 'baseline';
    document.querySelectorAll('.classroom-scen-btn').forEach((b) => b.classList.remove('active'));
    if ($('endClassroomBox')) $('endClassroomBox').hidden = true;
    ValleyModel.setDistrictControls(simState, 'ALL', presetPatch('baseline'));
    if (keepModalHidden) $('endModal').hidden = true;
    $('eventList').innerHTML = `<div class="event-item">
      <div class="event-title">Simulation ready — ${ui.shortLabel}, October 2026</div>
      <div>Starting point tuned to match NASA-ISRO NISAR provisional measurements (${ui.windowLabel}).</div>
      <div class="event-src">Source: ${ui.summaryUrl}</div>
    </div>`;
    syncUI();
  }

  function updateBasinCalibrationCard() {
    document.querySelectorAll('.basin-btn').forEach((b) => {
      const on = b.dataset.basin === activeBasinId;
      b.classList.toggle('active', on);
      if (b.hasAttribute('aria-checked')) b.setAttribute('aria-checked', on ? 'true' : 'false');
    });
    const endLink = $('endAtlasLink');
    if (endLink) endLink.href = activeBasinId === 'konya' ? '../web/atlas.html#konya_plain' : '../web/atlas.html#central_valley';
    const ui = BASIN_UI[activeBasinId] || BASIN_UI.tulare;
    const cal = ValleyModel.runCalibrationCheck(summaryData, activeBasinId);
    const rng = summaryData && (summaryData.range_cm || summaryData.max_subsidence_range_cm);
    const calNote = Array.isArray(rng) && rng.length === 2
      ? `ref range ${Math.max(rng[0], rng[1])}…${Math.min(rng[0], rng[1])} cm LOS`
      : ui.calNote;
    $('startCalibrationBox').innerHTML =
      `<strong>Model check against NISAR (${cal.within10Pct ? 'PASS ±10%' : 'CHECK'} · ${ui.shortLabel}):</strong>
      Under baseline summer pumping for the 108-day NISAR window (${ui.windowLabel}), the model simulates
      <span class="mono color-ok">${cal.simulatedVertCm} cm</span> vertical (<span class="mono">${cal.simulatedLosCm} cm</span> LOS) at ${cal.district} vs
      <span class="mono">${cal.measuredVertCm} cm</span> vertical (<span class="mono">${cal.measuredLosCm} cm</span> LOS; ${calNote}) measured by NISAR
      (<span class="mono">error: ${cal.errorPct}%</span>, extraction scale factor <span class="mono">k=${cal.calibrationFactor}</span>).`;
  }

  async function loadBasinData(basinId) {
    if (basinDataCache[basinId]) return basinDataCache[basinId];
    const ui = BASIN_UI[basinId] || BASIN_UI.tulare;
    const fetchSafe = async (url) => {
      if (!url) return null;
      try {
        const r = await fetch(url);
        if (!r.ok) {
          console.warn(`Optional/data asset HTTP ${r.status}: ${url}`);
          return null;
        }
        return await r.json();
      } catch (err) {
        console.warn(`Failed fetching ${url}:`, err);
        return null;
      }
    };
    const isLocal = location.hostname === '127.0.0.1' || location.hostname === 'localhost';
    const [sRes, pRes, aRes, iRes, shRes] = await Promise.all([
      fetchSafe(ui.summaryUrl),
      fetchSafe(ui.pointsUrl),
      fetchSafe(ui.assetsUrl),
      isLocal ? fetchSafe(ui.localInfraUrl) : Promise.resolve(null),
      ui.sinkholesUrl ? fetchSafe(ui.sinkholesUrl) : Promise.resolve(null),
    ]);
    const bundle = { summary: sRes, points: pRes, assets: aRes, infra: iRes, sinkholes: shRes };
    basinDataCache[basinId] = bundle;
    return bundle;
  }

  async function switchBasin(basinId, flyMap) {
    if (!BASIN_UI[basinId]) return;
    activeBasinId = basinId;
    document.querySelectorAll('.basin-btn').forEach((b) => {
      b.classList.toggle('active', b.dataset.basin === basinId);
      if (b.getAttribute('role') === 'radio') b.setAttribute('aria-checked', String(b.dataset.basin === basinId));
    });
    setSeg($('basinSeg'), basinId);
    const ui = BASIN_UI[basinId];
    const bundle = await loadBasinData(basinId);
    summaryData = bundle.summary;
    pointsData = bundle.points;
    assetsGeoJson = bundle.assets;
    infraBackdropGeoJson = bundle.infra;
    sinkholesGeoJson = bundle.sinkholes;

    resetSimulation(true);
    if (assetsGeoJson) tagAssetsToNearestDistrict(assetsGeoJson);
    updateBasinCalibrationCard();

    if (mapReady) {
      const dispSrc = map.getSource('nisar-disp');
      if (dispSrc && typeof dispSrc.updateImage === 'function') {
        dispSrc.updateImage({
          url: ui.rasterUrl,
          coordinates: [
            [ui.bbox[0], ui.bbox[3]],
            [ui.bbox[2], ui.bbox[3]],
            [ui.bbox[2], ui.bbox[1]],
            [ui.bbox[0], ui.bbox[1]],
          ],
        });
      }
      const ibSrc = map.getSource('infra-backdrop');
      if (ibSrc) ibSrc.setData(infraBackdropGeoJson || assetsGeoJson || { type: 'FeatureCollection', features: [] });
      const shSrc = map.getSource('karapinar-sinkholes');
      if (shSrc) shSrc.setData(sinkholesGeoJson || { type: 'FeatureCollection', features: [] });
      if (map.getLayer('karapinar-sinkholes-layer')) {
        map.setLayoutProperty('karapinar-sinkholes-layer', 'visibility', basinId === 'konya' ? 'visible' : 'none');
      }
      rebuildMapMarkers();
      refreshMapDynamicLayers();
      if (flyMap) {
        map.flyTo({ center: ui.center, zoom: ui.zoom, duration: 750 });
      }
    }
    syncUI();
  }

  let quickDemoTimer = null;
  let isQuickDemo = false;

  function stopQuickDemo() {
    if (quickDemoTimer) {
      clearInterval(quickDemoTimer);
      quickDemoTimer = null;
    }
    isQuickDemo = false;
    const pill = $('quickDemoStatusPill');
    if (pill) pill.style.display = 'none';
    const qBtn = $('quickDemoTopbarBtn');
    if (qBtn) qBtn.textContent = 'Quick demo (30 s) ⚡';
  }

  function startQuickDemo() {
    stopQuickDemo();
    isQuickDemo = true;
    if ($('startModal')) $('startModal').hidden = true;
    if ($('endModal')) $('endModal').hidden = true;
    if ($('classroomModal')) $('classroomModal').hidden = true;
    if ($('paramsModal')) $('paramsModal').hidden = true;

    const qBtn = $('quickDemoTopbarBtn');
    if (qBtn) qBtn.textContent = 'Stop demo ⏹';

    const pill = $('quickDemoStatusPill');
    if (pill) {
      pill.style.display = 'flex';
      const t = $('qdPillTitle');
      if (t) t.textContent = '⚡ QUICK DEMO · MONTH 1/24';
    }

    resetSimulation(true);
    activePreset = 'overpump';
    applyAll = true;
    if ($('applyAllChk')) $('applyAllChk').checked = true;
    const patch = presetPatch('overpump');
    if (patch) {
      ValleyModel.setDistrictControls(simState, 'ALL', patch);
      syncUI();
    }

    const urlFast = (new URLSearchParams(window.location.search)).get('fast') === '1';
    const intervalMs = urlFast ? 80 : 1170; // 24 * 1.17s = 28 seconds total (or fast mode for QA)
    quickDemoTimer = setInterval(() => {
      if (!simState || simState.finished) {
        stopQuickDemo();
        return;
      }
      advanceMonths(1);
      const t = $('qdPillTitle');
      if (t && simState) {
        t.textContent = `⚡ QUICK DEMO · MONTH ${simState.monthStep}/24`;
      }
      if (simState && simState.finished) {
        stopQuickDemo();
      }
    }, intervalMs);
  }

  function wireControls() {
    if ($('quickDemoBtn')) $('quickDemoBtn').addEventListener('click', startQuickDemo);
    if ($('quickDemoTopbarBtn')) {
      $('quickDemoTopbarBtn').addEventListener('click', () => {
        if (isQuickDemo) stopQuickDemo();
        else startQuickDemo();
      });
    }
    if ($('quickDemoStatusPill')) $('quickDemoStatusPill').addEventListener('click', stopQuickDemo);

    $('startBtn').addEventListener('click', () => {
      $('startModal').hidden = true;
      playTone('click');
    });

    const showTab = (tab) => {
      setSeg($('infoSeg'), tab);
      document.querySelectorAll('#infoSeg .seg-btn').forEach((b) => b.setAttribute('aria-selected', String(b.dataset.tab === tab)));
      $('paramsTableWrap').hidden = tab !== 'sources';
      $('testsWrap').hidden = tab !== 'tests';
      if (tab === 'tests') renderTests();
    };
    $('paramsBtn').addEventListener('click', () => {
      $('paramsTableWrap').innerHTML = buildParamsTableHtml();
      $('paramsModal').hidden = false;
      requestAnimationFrame(() => showTab('sources'));
    });
    document.querySelectorAll('#infoSeg .seg-btn').forEach((b) => b.addEventListener('click', () => showTab(b.dataset.tab)));
    $('closeParamsBtn').addEventListener('click', () => {
      $('paramsModal').hidden = true;
    });
    $('paramsModal').addEventListener('click', (e) => { if (e.target === $('paramsModal')) $('paramsModal').hidden = true; });

    if ($('classroomBtn')) {
      $('classroomBtn').addEventListener('click', () => {
        $('classroomModal').hidden = false;
      });
    }
    if ($('closeClassroomBtn')) {
      $('closeClassroomBtn').addEventListener('click', () => {
        $('classroomModal').hidden = true;
      });
    }
    if ($('classroomModal')) {
      $('classroomModal').addEventListener('click', (e) => {
        if (e.target === $('classroomModal')) $('classroomModal').hidden = true;
      });
    }
    document.querySelectorAll('.classroom-scen-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        playTone('click');
        runClassroomScenario(btn.dataset.classroom);
      });
    });

    let syncRafPending = false;
    const handleSlider = (key, val, labelId) => {
      activePreset = null; // a hand-set value is no longer one of the three scenarios
      const target = applyAll ? 'ALL' : selectedDistrictId;
      ValleyModel.setDistrictControls(simState, target, { [key]: Number(val) });
      if (labelId && $(labelId)) $(labelId).textContent = `${Number(val)}%`;
      if (!syncRafPending) {
        syncRafPending = true;
        requestAnimationFrame(() => {
          syncRafPending = false;
          syncUI();
        });
      }
    };
    $('pumpSlider').addEventListener('input', (e) => handleSlider('pumpingPct', e.target.value, 'pumpVal'));
    $('surfaceSlider').addEventListener('input', (e) => handleSlider('surfaceAllocPct', e.target.value, 'surfaceVal'));
    $('fallowSlider').addEventListener('input', (e) => handleSlider('fallowPct', e.target.value, 'fallowVal'));

    document.addEventListener('keydown', (e) => {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      if (e.key === 'Escape') {
        $('paramsModal').hidden = true;
        if ($('classroomModal')) $('classroomModal').hidden = true;
        $('endModal').hidden = true;
        $('startModal').hidden = true;
        return;
      }
      const modalOpen = !$('startModal').hidden || !$('endModal').hidden || !$('paramsModal').hidden || ($('classroomModal') && !$('classroomModal').hidden);
      if (modalOpen) return;

      const tag = document.activeElement ? document.activeElement.tagName : '';
      if (e.code === 'Space' && tag !== 'BUTTON' && tag !== 'SUMMARY' && tag !== 'A' && tag !== 'INPUT') {
        e.preventDefault();
        advanceMonths(1);
      } else if ((e.key === 'n' || e.key === 'N') && tag !== 'INPUT') {
        e.preventDefault();
        advanceMonths(1);
      } else if ((e.key === 'r' || e.key === 'R') && tag !== 'INPUT') {
        e.preventDefault();
        resetSimulation(true);
      } else if (/^[1-7]$/.test(e.key) && tag !== 'INPUT') {
        const idx = parseInt(e.key, 10) - 1;
        if (simState && simState.districts[idx]) {
          e.preventDefault();
          selectDistrict(simState.districts[idx].id, true);
        }
      }
    });

    document.querySelectorAll('.preset-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const patch = presetPatch(btn.dataset.preset);
        if (patch) {
          activePreset = btn.dataset.preset;
          ValleyModel.setDistrictControls(simState, applyAll ? 'ALL' : selectedDistrictId, patch);
          syncUI();
        }
      });
    });

    document.querySelectorAll('.layer-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.layer-btn').forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        overlayMode = btn.dataset.overlay;
        applyOverlayMode();
      });
    });

    $('nextMonthBtn').addEventListener('click', () => advanceMonths(1));
    $('fastForwardBtn').addEventListener('click', () => advanceMonths(6));
    $('resetBtn').addEventListener('click', () => resetSimulation(true));
    $('playAgainBtn').addEventListener('click', () => resetSimulation(true));
    $('closeEndBtn').addEventListener('click', () => {
      $('endModal').hidden = true;
    });

    $('copySummaryBtn').addEventListener('click', async () => {
      const ui = BASIN_UI[activeBasinId] || BASIN_UI.tulare;
      const worst = [...simState.districts].sort((a, b) => a.totalCm - b.totalCm)[0];
      const text = `NISAR Vision Groundwater Simulator (${ui.shortLabel}, 24-Mo NISAR Sim) — Peak: ${worst.totalCm.toFixed(1)} cm (${worst.inelasticCm.toFixed(1)} cm permanent) near ${worst.shortName}.`;
      try {
        if (navigator.clipboard) await navigator.clipboard.writeText(text);
        $('copySummaryBtn').textContent = 'Copied ✓';
        setTimeout(() => { $('copySummaryBtn').textContent = 'Copy Shareable Summary'; }, 1800);
      } catch (_e) {
        $('copySummaryBtn').textContent = 'Summary Ready';
      }
    });

    document.querySelectorAll('.basin-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        if (btn.dataset.basin && btn.dataset.basin !== activeBasinId) {
          playTone('click');
          switchBasin(btn.dataset.basin, true);
        }
      });
    });

  }

  function presetPatch(name) {
    const wyMax = ValleyModel.getWaterYearSpec(simState.currentWaterYear).maxSurfacePct;
    return {
      baseline: { pumpingPct: 100, surfaceAllocPct: Math.min(60, wyMax), fallowPct: 0 },
      overpump: { pumpingPct: 145, surfaceAllocPct: Math.min(20, wyMax), fallowPct: 0 },
      balance: { pumpingPct: 55, surfaceAllocPct: wyMax, fallowPct: 25 },
    }[name];
  }

  /* ---------- model verification report ---------- */
  let testsCache = null;
  async function renderTests() {
    const box = $('testsWrap');
    if (!window.ValleyTests) { box.innerHTML = '<p class="test-note">Test suite not loaded.</p>'; return; }
    if (!testsCache) {
      box.innerHTML = '<p class="test-note">Running the model checks in your browser…</p>';
      testsCache = await window.ValleyTests.run('..');
    }
    const r = testsCache;
    const esc = (s) => String(s).replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
    let group = '';
    const rows = r.cases.map((c) => {
      const head = c.group !== group ? `<tr class="test-group"><td colspan="4">${esc(c.group)}</td></tr>` : '';
      group = c.group;
      return `${head}<tr>
        <td class="test-id">${c.id}</td>
        <td><strong>${esc(c.name)}</strong><div class="test-crit">${esc(c.criterion)}</div></td>
        <td class="test-res">${esc(c.result)}</td>
        <td><span class="badge ${c.pass ? 'pass' : 'fail'}">${c.pass ? 'PASS' : 'FAIL'}</span></td>
      </tr>`;
    }).join('');
    box.innerHTML = `
      <div class="test-head">
        <div><span>Result</span><b class="${r.passed === r.total ? 'color-ok' : 'color-perm'}">${r.passed} / ${r.total} passed</b></div>
        <div><span>Model</span><b>model.js v2</b></div>
        <div><span>Reference data</span><b>NISAR 2026</b></div>
        <div><span>Run</span><b>${r.ranAt.toISOString().slice(0, 16).replace('T', ' ')} UTC</b></div>
      </div>
      <table class="test-table">
        <thead><tr><th>ID</th><th>Check and pass criterion</th><th>Measured result</th><th>Status</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>
      <p class="test-note">Each check runs the simulation model live in this browser against the repository's NISAR data files (data/central_valley, data/karapinar). Results are computed now, not stored.</p>`;
  }

  async function boot() {
    const bundle = await loadBasinData(activeBasinId);
    summaryData = bundle.summary;
    pointsData = bundle.points;
    assetsGeoJson = bundle.assets;
    infraBackdropGeoJson = bundle.infra;
    sinkholesGeoJson = bundle.sinkholes;

    resetSimulation(true);
    if (assetsGeoJson) tagAssetsToNearestDistrict(assetsGeoJson);
    updateBasinCalibrationCard();

    wireControls();
    initVSliders();
    wireChartPan();
    initMap();
    const placeSegs = () => {
      setSeg($('basinSeg'), activeBasinId);
      setSeg($('presetSeg'), activePreset);
      if (!$('paramsModal').hidden) setSeg($('infoSeg'), $('testsWrap').hidden ? 'sources' : 'tests');
    };
    syncUI();
    placeSegs();
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('quickdemo') === '1' || urlParams.has('quickdemo') || urlParams.has('demo')) {
      setTimeout(startQuickDemo, 300);
    }
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(placeSegs);
    // re-place the sliding bars whenever a control changes size (fonts, layout, modal opening)
    if (window.ResizeObserver) {
      const ro = new ResizeObserver(() => placeSegs());
      document.querySelectorAll('.seg').forEach((s) => ro.observe(s));
    }
    $('startBtn').addEventListener('click', () => requestAnimationFrame(placeSegs));
    let resizeRafPending = false;
    window.addEventListener('resize', () => {
      if (resizeRafPending) return;
      resizeRafPending = true;
      requestAnimationFrame(() => {
        resizeRafPending = false;
        placeSegs();
        const d = simState && simState.districts.find((x) => x.id === selectedDistrictId);
        if (d) renderStratigraphy(d);
      });
    });
  }

  boot();
})();
