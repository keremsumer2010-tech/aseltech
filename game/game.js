/* Valley Under Pressure v2 — Interactive Satellite & Hydrogeology Simulation */
(function () {
  'use strict';

  const CV_BBOX = [-120.2, 35.6, -119.0, 36.6];
  const CV_CENTER = [-119.62, 36.08];

  let simState = null;
  let selectedDistrictId = 'p01';
  let applyAll = false;
  let overlayMode = 'sim'; // 'sim' | 'blend' | 'nisar'
  let audioEnabled = false;
  let audioCtx = null;

  let map = null;
  let mapReady = false;
  let districtMarkers = {};
  let assetsGeoJson = null;
  let infraBackdropGeoJson = null;
  let summaryData = null;
  let pointsData = null;
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
    if (gradMmKm >= ValleyModel.CONFIG.thresholds.canalHighGradientMmKm) return '#ff6b57';
    if (gradMmKm >= ValleyModel.CONFIG.thresholds.canalMediumGradientMmKm) return '#f5b942';
    return '#3ddc97';
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
    simState.districts.forEach((d) => {
      const coords = [];
      const radLon = 0.082;
      const radLat = 0.064;
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
      .filter((f) => f.properties && f.properties.type === 'canal')
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

  /**
   * Initialize MapLibre 4.7.1 with Esri World Imagery + NISAR Raster + Real OSM Canals/Roads + District Markers.
   */
  function initMap() {
    map = new maplibregl.Map({
      container: 'map',
      center: CV_CENTER,
      zoom: 8.6,
      minZoom: 7.5,
      maxZoom: 14,
      attributionControl: true,
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
            url: '../data/central_valley/disp/2026-10-14.png',
            coordinates: [
              [CV_BBOX[0], CV_BBOX[3]],
              [CV_BBOX[2], CV_BBOX[3]],
              [CV_BBOX[2], CV_BBOX[1]],
              [CV_BBOX[0], CV_BBOX[1]],
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

      // Roads/rails & canals backdrop from data/central_valley/assets.json (Pages-safe; full risk/ geojson optionally added locally)
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

      // Evaluated dynamic canals from assets.json (green -> yellow -> red live risk)
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

      // Interactive District Place Labels (zero missing glyph server errors)
      simState.districts.forEach((d) => {
        const el = document.createElement('button');
        el.type = 'button';
        el.style.cssText =
          'background:rgba(11,15,20,0.88);border:1px solid #2f4259;color:#e6edf3;padding:3px 7px;border-radius:4px;font-size:11px;font-weight:600;cursor:pointer;white-space:nowrap;font-family:inherit;box-shadow:0 2px 8px rgba(0,0,0,0.5);';
        el.innerHTML = `<span>${d.shortName}</span> <span class="mval mono" style="color:#ff6b57;">0.0 cm</span>`;
        el.addEventListener('click', () => selectDistrict(d.id, false));
        const mk = new maplibregl.Marker({ element: el, anchor: 'bottom' })
          .setLngLat([d.lon, d.lat])
          .addTo(map);
        districtMarkers[d.id] = { marker: mk, el };
      });

      // Woodlake stable reference marker from points.json
      if (Array.isArray(pointsData)) {
        const refPt = pointsData.find((p) => p.kind === 'near_reference');
        if (refPt) {
          const refEl = document.createElement('div');
          refEl.style.cssText =
            'background:rgba(15,21,29,0.82);border:1px dashed #3ddc97;color:#3ddc97;padding:2px 6px;border-radius:4px;font-size:10px;font-family:ui-monospace,monospace;';
          refEl.textContent = `REF: ${refPt.name}`;
          new maplibregl.Marker({ element: refEl, anchor: 'top' })
            .setLngLat([refPt.lon, refPt.lat])
            .addTo(map);
        }
      }

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
        valSpan.style.color = d.totalCm < -4 ? '#ff6b57' : d.totalCm < -1 ? '#f5b942' : '#3ddc97';
      }
      m.el.style.borderColor = d.id === selectedDistrictId ? '#4da3ff' : '#2f4259';
      m.el.style.background = d.id === selectedDistrictId ? 'rgba(19, 36, 56, 0.94)' : 'rgba(11,15,20,0.88)';
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
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const rect = canvas.getBoundingClientRect();
    const w = Math.max(260, Math.round(rect.width || 360));
    const h = 132;
    if (canvas.width !== w * dpr || canvas.height !== h * dpr) {
      canvas.width = w * dpr;
      canvas.height = h * dpr;
    }
    const ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);

    // Sky / Surface Datum
    ctx.fillStyle = '#090d12';
    ctx.fillRect(0, 0, w, h);

    const datumY = 20;
    // Exaggerate visual sag linearly so 0..30 cm is clearly legible
    const sagPx = Math.min(18, Math.max(-2, -d.totalCm * 0.65));
    const permPx = Math.min(16, Math.max(0, -d.inelasticCm * 0.65));
    const elastPx = Math.max(0, sagPx - permPx);

    // Dashed original ground datum
    ctx.save();
    ctx.setLineDash([4, 3]);
    ctx.strokeStyle = '#3b4f68';
    ctx.beginPath();
    ctx.moveTo(0, datumY);
    ctx.lineTo(w, datumY);
    ctx.stroke();
    ctx.restore();

    // Unconfined alluvium layer (sagging surface)
    const sagMidY = datumY + sagPx;
    ctx.fillStyle = '#202b38';
    ctx.beginPath();
    ctx.moveTo(0, datumY + 2);
    ctx.quadraticCurveTo(w * 0.5, sagMidY + 6, w, datumY + 2);
    ctx.lineTo(w, 74);
    ctx.lineTo(0, 74);
    ctx.closePath();
    ctx.fill();

    // Ground surface crest stroke
    ctx.strokeStyle = '#8b9bb0';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    ctx.moveTo(0, datumY + 2);
    ctx.quadraticCurveTo(w * 0.5, sagMidY + 6, w, datumY + 2);
    ctx.stroke();

    // Water table depth line mapped cleanly between -25m and -90m
    const mapDepthY = (headM) => {
      const depth = -headM;
      return Math.max(24, Math.min(100, 26 + ((depth - 25) / 70) * 70));
    };
    const wtY = mapDepthY(d.headM);
    const hpcY = mapDepthY(d.preconsolidationHeadM);

    // Saturated water zone tint below water table
    ctx.fillStyle = 'rgba(77, 163, 255, 0.14)';
    ctx.fillRect(0, wtY, w, 108 - wtY);

    // Corcoran Clay Aquitard Layer (visual thickness scales with district b0)
    const clayTop = 74 + sagPx * 0.3;
    const baseClayPx = Math.max(12, Math.min(34, d.clayThicknessM * 0.4));
    const currentClayPx = Math.max(7, baseClayPx - sagPx * 0.55);

    // Remaining uncompacted clay
    ctx.fillStyle = '#37302a';
    ctx.fillRect(0, clayTop, w, currentClayPx);
    // Elastic reversible compression zone (cyan)
    if (elastPx > 0.3) {
      ctx.fillStyle = 'rgba(77, 163, 255, 0.65)';
      ctx.fillRect(0, clayTop, w, Math.min(10, elastPx + 1.5));
    }
    // Irreversible permanent compaction scar (coral-red)
    if (permPx > 0.3) {
      ctx.fillStyle = 'rgba(255, 107, 87, 0.80)';
      ctx.fillRect(0, clayTop + currentClayPx - Math.min(14, permPx), w, Math.min(14, permPx));
    }

    // Bedrock / Lower Sand
    ctx.fillStyle = '#121821';
    ctx.fillRect(0, clayTop + currentClayPx, w, h - (clayTop + currentClayPx));

    // Preconsolidation Head h_pc dashed line
    ctx.save();
    ctx.setLineDash([5, 4]);
    ctx.strokeStyle = '#f5b942';
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    ctx.moveTo(0, hpcY);
    ctx.lineTo(w, hpcY);
    ctx.stroke();
    ctx.restore();

    // Current Water Table h line
    ctx.strokeStyle = '#4da3ff';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, wtY);
    ctx.lineTo(w, wtY);
    ctx.stroke();

    // Draw up to 5 representative wells along transect
    const sampleWells = d.wellDepthsM.slice(0, 5);
    sampleWells.forEach((wd, idx) => {
      const wx = 42 + idx * ((w - 84) / Math.max(1, sampleWells.length - 1));
      const wellBotY = mapDepthY(-wd);
      const isDry = -d.headM >= wd;
      ctx.strokeStyle = isDry ? '#ff6b57' : '#3ddc97';
      ctx.lineWidth = 2.2;
      ctx.beginPath();
      ctx.moveTo(wx, datumY + 2);
      ctx.lineTo(wx, wellBotY);
      ctx.stroke();

      ctx.fillStyle = isDry ? '#ff6b57' : '#3ddc97';
      ctx.fillRect(wx - 3, datumY - 2, 6, 4);
    });

    // Crisp Mono Telemetry Annotations
    ctx.font = '10px ui-monospace, SFMono-Regular, Menlo, monospace';
    ctx.fillStyle = '#8b9bb0';
    ctx.fillText('Datum 0 cm', 6, 12);
    ctx.fillStyle = '#e6edf3';
    ctx.fillText(`Surface ${d.totalCm.toFixed(1)} cm`, w - 118, 12);

    ctx.fillStyle = '#4da3ff';
    ctx.fillText(`Water Table ${d.headM.toFixed(1)} m`, 6, Math.max(36, wtY - 4));
    ctx.fillStyle = '#f5b942';
    ctx.fillText(`h_pc ${d.preconsolidationHeadM.toFixed(1)} m`, w - 98, Math.max(46, hpcY + 11));
    ctx.fillStyle = '#c4b5a5';
    ctx.fillText(`Compressible clay interbeds (b0=${d.clayThicknessM}m, illustr.)`, 6, Math.min(h - 6, clayTop + currentClayPx + 12));

    const pill = $('stratRegimePill');
    if (pill) {
      const inVirgin = d.headM <= d.preconsolidationHeadM + 0.05;
      pill.textContent = inVirgin ? 'PERMANENT COLLAPSE (< h_pc)' : 'ELASTIC RECOVERABLE (> h_pc)';
      pill.style.color = inVirgin ? '#ff6b57' : '#4da3ff';
      pill.style.borderColor = inVirgin ? 'rgba(255,107,87,0.5)' : 'rgba(77,163,255,0.45)';
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

    if (!timelineChart) {
      timelineChart = new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Total Subsidence (cm)',
              data: totalSeries,
              borderColor: '#4da3ff',
              backgroundColor: 'rgba(77, 163, 255, 0.12)',
              borderWidth: 2.2,
              tension: 0.25,
              pointRadius: 2.5,
            },
            {
              label: 'Permanent Clay Collapse (cm)',
              data: permSeries,
              borderColor: '#ff6b57',
              backgroundColor: 'rgba(255, 107, 87, 0.22)',
              fill: true,
              borderWidth: 2.2,
              tension: 0.25,
              pointRadius: 2,
            },
            {
              label: '2026 NISAR Ref (-10.1 cm)',
              data: nisarRefLine,
              borderColor: '#f5b942',
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
              display: true,
              position: window.innerWidth < 760 ? 'bottom' : 'right',
              labels: { color: '#8b9bb0', boxWidth: 11, font: { size: 10 }, padding: 8 },
            },
          },
          scales: {
            x: {
              ticks: { color: '#8b9bb0', maxTicksLimit: 13, font: { size: 10 } },
              grid: { color: 'rgba(34, 48, 65, 0.5)' },
            },
            y: {
              title: { display: true, text: 'cm', color: '#8b9bb0', font: { size: 10 } },
              ticks: { color: '#8b9bb0', font: { size: 10 } },
              grid: { color: 'rgba(34, 48, 65, 0.5)' },
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
      timelineChart.data.datasets[2].label = `2026 NISAR (${nisarVertRef} cm vert)`;
      timelineChart.options.plugins.legend.position = window.innerWidth < 760 ? 'bottom' : 'right';
      timelineChart.update('none');
    }

    $('chartTitle').textContent = `District Trajectory: ${d.name} vs 2026 NISAR`;
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
    $('monthPill').textContent = `Month ${moIdx} of ${simState.totalMonths} · ${calLabel} · ${seasonTag}`;

    const wyYearNum = moIdx < 12 ? 1 : 2;
    const wyPill = $('wyPill');
    wyPill.textContent = `WY${wyYearNum}: ${wySpec.label} (${wySpec.maxSurfacePct}% Surface Cap)`;
    wyPill.className = 'pill ' + (
      wySpec.id === 'Wet' ? 'wy-wet' :
      wySpec.id === 'Above Normal' ? 'wy-above' :
      wySpec.id === 'Dry' ? 'wy-dry' :
      wySpec.id === 'Critical' ? 'wy-critical' : 'wy-below'
    );

    // Basin HUD
    const worst = [...simState.districts].sort((a, b) => a.totalCm - b.totalCm)[0];
    const totalDry = simState.districts.reduce((s, x) => s + x.dryWells, 0);
    $('valleyHeadlineHud').innerHTML =
      `Peak Subsidence: <strong class="color-perm">${worst.totalCm.toFixed(1)} cm</strong> (${worst.shortName}) · Dry Wells: <strong>${totalDry}</strong>`;

    // District Tabs
    const tabsEl = $('districtTabs');
    tabsEl.innerHTML = simState.districts
      .map((dist) => {
        const activeCls = dist.id === d.id ? 'active' : '';
        return `<button type="button" class="district-chip ${activeCls}" data-did="${dist.id}">
          <span>${dist.shortName}</span>
          <span class="val">${dist.totalCm.toFixed(1)} cm</span>
        </button>`;
      })
      .join('');
    tabsEl.querySelectorAll('.district-chip').forEach((btn) => {
      btn.addEventListener('click', () => selectDistrict(btn.dataset.did, true));
    });

    $('districtCoordsPill').textContent = `${d.lat.toFixed(2)}°N, ${Math.abs(d.lon).toFixed(2)}°W`;

    // Sliders & Dynamic Surface Cap
    $('pumpSlider').value = d.controls.pumpingPct;
    $('pumpVal').textContent = `${d.controls.pumpingPct}%`;
    $('surfaceSlider').max = wySpec.maxSurfacePct;
    const cappedSurface = Math.min(d.controls.surfaceAllocPct, wySpec.maxSurfacePct);
    $('surfaceSlider').value = cappedSurface;
    $('surfaceVal').textContent = `${cappedSurface}%`;
    $('surfaceCapHint').textContent = `Max ${wySpec.maxSurfacePct}% in ${wySpec.label} water year (CVP/SWP constraint).`;
    $('fallowSlider').value = d.controls.fallowPct;
    $('fallowVal').textContent = `${d.controls.fallowPct}%`;

    // District KPIs: 3 primary readouts + quiet secondary strip
    const isVirgin = d.headM <= d.preconsolidationHeadM + 0.05;
    $('kpiDistrictTitle').textContent = `Readout: ${d.shortName} (${d.canalCorridor})`;
    $('kpiTotalCm').textContent = `${d.totalCm.toFixed(2)} cm`;
    $('kpiSplitCm').textContent = `Elastic: ${d.elasticCm.toFixed(2)} cm`;
    $('kpiPermCm').textContent = `${d.inelasticCm.toFixed(2)} cm`;
    $('kpiRegimeSub').textContent = isVirgin ? 'Virgin collapse' : 'Elastic Safe';
    $('kpiRegimeSub').style.color = isVirgin ? '#ff6b57' : '#3ddc97';
    $('kpiRevenue').textContent = `$${d.cumulativeRevenueMUsd.toFixed(1)}M`;
    $('kpiRevSub').textContent = `${100 - d.controls.fallowPct}% cropped`;

    $('kpiHeadM').textContent = `${d.headM.toFixed(1)} m`;
    $('kpiHpcM').textContent = `Low: ${d.preconsolidationHeadM.toFixed(1)} m`;
    $('kpiHpcM').style.color = isVirgin ? '#ff6b57' : 'var(--muted)';
    $('kpiCanalLoss').textContent = `${d.canalCapacityLossPct.toFixed(1)}%`;
    $('kpiGradient').textContent = `${d.currentGradientMmKm.toFixed(1)} mm/km`;
    $('kpiWells').textContent = `${d.dryWells} / ${d.wellDepthsM.length}`;

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

    const measuredLos = summaryData ? summaryData.max_subsidence_cm : -7.8;
    const measuredVert = summaryData ? summaryData.max_subsidence_vertical_cm_estimate : -10.1;
    const rate = summaryData ? summaryData.rate_cm_per_yr_estimate : -26.4;
    $('endNisarLos').textContent = `${measuredLos} cm`;
    $('endNisarVert').textContent = `~${measuredVert} cm`;
    $('endNisarRate').textContent = `${rate} cm/yr LOS`;

    let takeaway = '';
    if (Math.abs(worst.inelasticCm) >= 12) {
      takeaway = `What this means: Heavy groundwater pumping dropped levels past historical lows, locking in ${worst.inelasticCm.toFixed(1)} cm of permanent clay collapse near ${worst.shortName}. Even future wet winters cannot restore that lost underground pore storage.`;
    } else if (Math.abs(worst.inelasticCm) <= 4) {
      takeaway = `What this means: Limiting groundwater extraction balanced winter recharge and kept permanent collapse to ${worst.inelasticCm.toFixed(1)} cm across the basin. Canal conveyance gradients stayed within safe design limits.`;
    } else {
      takeaway = `What this means: Summer irrigation temporarily pushed hotspots past historical lows, causing ${worst.inelasticCm.toFixed(1)} cm of permanent clay collapse near ${worst.shortName}. Reducing summer pumping peaks before dry years protects canal capacity and wells.`;
    }
    $('endMeaning').textContent = takeaway;
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

    endCompareChart = new Chart(canvas.getContext('2d'), {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Your 24-Mo Total Sink (cm)',
            data: simTotal,
            backgroundColor: 'rgba(77, 163, 255, 0.78)',
            borderColor: '#4da3ff',
            borderWidth: 1,
          },
          {
            label: 'Your Permanent Collapse (cm)',
            data: simPerm,
            backgroundColor: 'rgba(255, 107, 87, 0.85)',
            borderColor: '#ff6b57',
            borderWidth: 1,
          },
          {
            label: '2026 NISAR 108-Day Est. (cm)',
            data: nisarVert,
            backgroundColor: 'rgba(245, 185, 66, 0.85)',
            borderColor: '#f5b942',
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
            labels: { color: '#e6edf3', boxWidth: 11, font: { size: 10.5 }, padding: 8 },
          },
        },
        scales: {
          x: {
            ticks: { color: '#8b9bb0', font: { size: 10.5 } },
            grid: { display: false },
          },
          y: {
            beginAtZero: true,
            title: { display: true, text: 'Subsidence magnitude (cm)', color: '#8b9bb0', font: { size: 10.5 } },
            ticks: { color: '#8b9bb0', font: { size: 10 } },
            grid: { color: 'rgba(34, 48, 65, 0.5)' },
          },
        },
      },
    });
  }

  function advanceMonths(count) {
    if (!simState || simState.finished) return;
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
    const cal = ValleyModel.runCalibrationCheck(summaryData);
    const p = ValleyModel.CONFIG.physics;
    const rows = [
      ['Model Check Factor (k)', `${cal.calibrationFactor}`, 'Multiplier (108-day NISAR summer benchmark)', 'Calibrated to data/central_valley/summary.json (-10.1 cm vert / -7.8 cm LOS)', false],
      ['Specific Yield (S_y)', `${p.specificYield.value}`, p.specificYield.unit, p.specificYield.source, p.specificYield.illustrative],
      ['Elastic Skeletal Storage (S_ske)', `${p.elasticSpecificStorage.value}`, p.elasticSpecificStorage.unit, p.elasticSpecificStorage.source, p.elasticSpecificStorage.illustrative],
      ['Inelastic Skeletal Storage (S_skv)', `${p.inelasticSpecificStorage.value}`, p.inelasticSpecificStorage.unit, p.inelasticSpecificStorage.source, p.inelasticSpecificStorage.illustrative],
      ['Compressible Clay Interbeds (b0)', '12–82 m across districts', 'Aggregate thickness', 'CVHM SUB aggregate interbeds (Corcoran Clay alone <= 61 m per Page 1986)', true],
      ['Water Year Probabilities & Caps', 'DWR 5-class weights (15–100% cap)', 'Probability / %', 'Formula from DWR WSIHIST; class probabilities illustrative', true],
      ['Baseline Demand / Recharge', `${p.baselineAnnualDemandM.value} / ${p.baselineAnnualRechargeM.value}`, 'm/yr eq', p.baselineAnnualDemandM.source, true],
      ['Canal Capacity Loss Curve', 'Up to 60% above 10 mm/km', '% conveyance drop', 'Friant-Kern >60% capacity loss verified (FWA/KVPR); onset threshold illustrative', true],
      ['Well Failure Depths & Crop Prices', 'Representative depths & $/ha', 'wells / USD', 'Stylized regional baseline per district', true],
    ];
    return `<table class="param-table">
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

  function resetSimulation(keepModalHidden) {
    const hydrated = ValleyModel.hydrateFromRepoData(pointsData, summaryData);
    simState = ValleyModel.createSimulationState({
      districts: hydrated.districts,
      summaryData: hydrated.summaryData,
      year1WaterYear: 'Below Normal',
    });
    if (keepModalHidden) $('endModal').hidden = true;
    $('eventList').innerHTML = `<div class="event-item">
      <div class="event-title">Simulation Reset — Oct 2026 Water Year Start</div>
      <div>Calibrated to NASA-ISRO NISAR provisional measurements (2026-06-28 → 2026-10-14).</div>
      <div class="event-src">Source: ../data/central_valley/summary.json</div>
    </div>`;
    syncUI();
  }

  function wireControls() {
    $('startBtn').addEventListener('click', () => {
      $('startModal').hidden = true;
      playTone('click');
    });

    $('audioToggleBtn').addEventListener('click', () => {
      audioEnabled = !audioEnabled;
      const btn = $('audioToggleBtn');
      btn.setAttribute('aria-pressed', String(audioEnabled));
      btn.textContent = audioEnabled ? 'Audio: On' : 'Audio: Off';
      if (audioEnabled) playTone('click');
    });

    $('paramsBtn').addEventListener('click', () => {
      $('paramsTableWrap').innerHTML = buildParamsTableHtml();
      $('paramsModal').hidden = false;
    });
    $('closeParamsBtn').addEventListener('click', () => {
      $('paramsModal').hidden = true;
    });

    $('applyAllChk').addEventListener('change', (e) => {
      applyAll = e.target.checked;
    });

    const handleSlider = (key, val) => {
      const target = applyAll ? 'ALL' : selectedDistrictId;
      ValleyModel.setDistrictControls(simState, target, { [key]: Number(val) });
      syncUI();
    };
    $('pumpSlider').addEventListener('input', (e) => handleSlider('pumpingPct', e.target.value));
    $('surfaceSlider').addEventListener('input', (e) => handleSlider('surfaceAllocPct', e.target.value));
    $('fallowSlider').addEventListener('input', (e) => handleSlider('fallowPct', e.target.value));

    document.querySelectorAll('.preset-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const wyMax = ValleyModel.getWaterYearSpec(simState.currentWaterYear).maxSurfacePct;
        const presets = {
          baseline: { pumpingPct: 100, surfaceAllocPct: Math.min(60, wyMax), fallowPct: 0 },
          overpump: { pumpingPct: 145, surfaceAllocPct: Math.min(20, wyMax), fallowPct: 0 },
          balance: { pumpingPct: 55, surfaceAllocPct: wyMax, fallowPct: 25 },
        };
        const patch = presets[btn.dataset.preset];
        if (patch) {
          ValleyModel.setDistrictControls(simState, applyAll ? 'ALL' : selectedDistrictId, patch);
          playTone('click');
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
      const worst = [...simState.districts].sort((a, b) => a.totalCm - b.totalCm)[0];
      const text = `Valley Under Pressure (24-Mo NISAR Sim) — Peak: ${worst.totalCm.toFixed(1)} cm (${worst.inelasticCm.toFixed(1)} cm permanent) near ${worst.shortName} vs 2026 NISAR 108-day baseline (-7.8 cm LOS / -10.1 cm vertical).`;
      try {
        if (navigator.clipboard) await navigator.clipboard.writeText(text);
        $('copySummaryBtn').textContent = 'Copied ✓';
        setTimeout(() => { $('copySummaryBtn').textContent = 'Copy Shareable Summary'; }, 1800);
      } catch (_e) {
        $('copySummaryBtn').textContent = 'Summary Ready';
      }
    });
  }

  async function boot() {
    const fetchSafe = async (url) => {
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
    const [sRes, pRes, aRes, iRes] = await Promise.all([
      fetchSafe('../data/central_valley/summary.json'),
      fetchSafe('../data/central_valley/points.json'),
      fetchSafe('../data/central_valley/assets.json'),
      isLocal ? fetchSafe('../risk/central_valley_infra.geojson') : Promise.resolve(null),
    ]);
    summaryData = sRes;
    pointsData = pRes;
    assetsGeoJson = aRes;
    infraBackdropGeoJson = iRes;

    resetSimulation(true);
    if (assetsGeoJson) tagAssetsToNearestDistrict(assetsGeoJson);

    const cal = ValleyModel.runCalibrationCheck(summaryData);
    $('startCalibrationBox').innerHTML =
      `<strong>Model check against NISAR (${cal.within10Pct ? 'PASS ±10%' : 'CHECK'}):</strong>
      Under baseline summer pumping for the 108-day NISAR window (Jun–Oct 2026), the model simulates
      <span class="mono color-ok">${cal.simulatedVertCm} cm</span> vertical (<span class="mono">${cal.simulatedLosCm} cm</span> LOS) at Terra Bella vs
      <span class="mono">${cal.measuredVertCm} cm</span> vertical (<span class="mono">${cal.measuredLosCm} cm</span> LOS; ref range −4.7…−7.8 cm LOS) measured by NISAR
      (<span class="mono">error: ${cal.errorPct}%</span>, extraction scale factor <span class="mono">k=${cal.calibrationFactor}</span>).`;

    wireControls();
    initMap();
    window.addEventListener('resize', () => {
      const d = simState && simState.districts.find((x) => x.id === selectedDistrictId);
      if (d) renderStratigraphy(d);
    });
  }

  boot();
})();
