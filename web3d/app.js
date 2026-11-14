import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

/* ---------- colour ramp (same RdBu scale as the site maps) ---------- */
const RDBU_STOPS = [
  [0.0, [103, 0, 31]],
  [0.16, [178, 24, 43]],
  [0.32, [214, 96, 77]],
  [0.5, [247, 247, 247]],
  [0.68, [67, 147, 195]],
  [0.84, [33, 102, 172]],
  [1.0, [5, 48, 97]],
];

function rdbuColor(val, vmin, vmax) {
  const t = Math.max(0, Math.min(1, (val - vmin) / (vmax - vmin || 1)));
  for (let i = 0; i < RDBU_STOPS.length - 1; i++) {
    const [t0, c0] = RDBU_STOPS[i];
    const [t1, c1] = RDBU_STOPS[i + 1];
    if (t >= t0 && t <= t1) {
      const f = (t - t0) / (t1 - t0);
      return [
        (c0[0] + (c1[0] - c0[0]) * f) / 255,
        (c0[1] + (c1[1] - c0[1]) * f) / 255,
        (c0[2] + (c1[2] - c0[2]) * f) / 255,
      ];
    }
  }
  return [0.97, 0.97, 0.97];
}

/* ---------- page elements ---------- */
const $ = (id) => document.getElementById(id);
const host = $("canvasHost");
const epochSlider = $("epochSlider");
const exagSlider = $("exagSlider");
const exagLabel = $("exagLabel");
const playBtn = $("playBtn");
const sinkholeToggle = $("sinkholeToggle");
const sinkholeToggleWrap = $("sinkholeToggleWrap");
const inspectorBox = $("inspectorBox");

/* ---------- scene ---------- */
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(42, host.clientWidth / host.clientHeight, 0.1, 200);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(host.clientWidth, host.clientHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
host.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.07;
controls.maxPolarAngle = Math.PI * 0.47;
controls.minDistance = 4;
controls.maxDistance = 48;

scene.add(new THREE.AmbientLight(0xffffff, 0.95));
const dirLight = new THREE.DirectionalLight(0xffffff, 0.7);
dirLight.position.set(8, 16, 10);
scene.add(dirLight);

const WORLD_SPAN = 14.0;
const SURFACE_ALPHA = 0.88;
let bundle = null;
let activeSite = "central_valley";
let surfaceMesh = null;
let basePlane = null;
let frameLine = null;
const beaconGroup = new THREE.Group();
const sinkholeGroup = new THREE.Group();
scene.add(beaconGroup, sinkholeGroup);

let cache = null; // per-region precomputed arrays: { mask, fill[], smooth[] }
let lift = 0.2; // surface base height above the imagery so sinking never goes under it
let playing = false;
let lastFrame = performance.now();
const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();
const textures = {};

function setCameraDefault() {
  // narrow (phone) screens: step back so the whole scene fits
  const f = Math.min(2.2, Math.max(1, 1.1 / (host.clientWidth / host.clientHeight)));
  camera.position.set(0, 10.5 * f, 12.5 * f);
  controls.target.set(0, 0, 0);
  controls.update();
}
setCameraDefault();

/* ---------- geometry helpers ---------- */
function regionDims(region) {
  const [w, s, e, n] = region.bbox;
  const midLatRad = ((s + n) * 0.5 * Math.PI) / 180;
  const aspect = ((e - w) * Math.cos(midLatRad)) / (n - s || 1);
  return { width: WORLD_SPAN, depth: WORLD_SPAN / aspect, aspect };
}

function lonLatToWorld(lon, lat, region) {
  const [w, s, e, n] = region.bbox;
  const { width, depth } = regionDims(region);
  const u = (lon - w) / (e - w || 1) - 0.5;
  const v = (n - lat) / (n - s || 1) - 0.5;
  return { x: u * width, z: v * depth, width, depth };
}

function cmToWorldY(cm, region) {
  const [w, s, e, n] = region.bbox;
  const midLatRad = ((s + n) * 0.5 * Math.PI) / 180;
  const realWidthMeters = (e - w) * 111320 * Math.cos(midLatRad);
  const metersPerWorldUnit = realWidthMeters / WORLD_SPAN;
  return (cm * 0.01 * Number(exagSlider.value)) / metersPerWorldUnit;
}

function fmtLatLon(lat, lon) {
  return `${Math.abs(lat).toFixed(4)}°${lat >= 0 ? "N" : "S"}, ${Math.abs(lon).toFixed(4)}°${lon >= 0 ? "E" : "W"}`;
}

/* ---------- precompute: mask, light smoothing, gap filling (heights only) ---------- */
function prepare(region) {
  const { rows, cols, grids } = region;
  const n = rows * cols;
  const mask = new Uint8Array(n);
  for (let i = 0; i < n; i++) mask[i] = grids.every((g) => g[i] !== null) ? 1 : 0;

  const K = [1, 2, 1, 2, 4, 2, 1, 2, 1];
  const smooth = grids.map((g) => {
    const out = new Float32Array(n).fill(NaN);
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const i = r * cols + c;
        if (!mask[i]) continue;
        let sum = 0, wsum = 0, k = 0;
        for (let dr = -1; dr <= 1; dr++) {
          for (let dc = -1; dc <= 1; dc++, k++) {
            const rr = r + dr, cc = c + dc;
            if (rr < 0 || rr >= rows || cc < 0 || cc >= cols) continue;
            const j = rr * cols + cc;
            if (!mask[j]) continue;
            sum += g[j] * K[k];
            wsum += K[k];
          }
        }
        out[i] = sum / wsum;
      }
    }
    return out;
  });

  // fill gaps for geometry only (they stay invisible): repeat "average of filled neighbours"
  const fill = smooth.map((sm) => {
    const out = Float32Array.from(sm);
    let remaining = true;
    for (let pass = 0; pass < rows + cols && remaining; pass++) {
      remaining = false;
      const snap = Float32Array.from(out);
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          const i = r * cols + c;
          if (!Number.isNaN(snap[i])) continue;
          let sum = 0, cnt = 0;
          for (let dr = -1; dr <= 1; dr++) {
            for (let dc = -1; dc <= 1; dc++) {
              const rr = r + dr, cc = c + dc;
              if (rr < 0 || rr >= rows || cc < 0 || cc >= cols) continue;
              const v = snap[rr * cols + cc];
              if (!Number.isNaN(v)) { sum += v; cnt++; }
            }
          }
          if (cnt) out[i] = sum / cnt; else remaining = true;
        }
      }
    }
    for (let i = 0; i < n; i++) if (Number.isNaN(out[i])) out[i] = 0;
    return out;
  });
  return { mask, smooth, fill };
}

function valueAt(idx, epochFloat) {
  const i0 = Math.min(cache.fill.length - 1, Math.floor(epochFloat));
  const i1 = Math.min(cache.fill.length - 1, i0 + 1);
  const a = epochFloat - i0;
  return cache.fill[i0][idx] * (1 - a) + cache.fill[i1][idx] * a;
}

/* ---------- satellite imagery under the surface ---------- */
function loadBasemap(siteKey, region) {
  if (textures[siteKey]) return Promise.resolve(textures[siteKey]);
  const [w, s, e, n] = region.bbox;
  const { aspect } = regionDims(region);
  const size = `${1280},${Math.round(1280 / aspect)}`;
  const url = `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export?bbox=${w},${s},${e},${n}&bboxSR=4326&imageSR=4326&size=${size}&format=jpg&f=image`;
  return new Promise((resolve) => {
    const loader = new THREE.TextureLoader();
    loader.setCrossOrigin("anonymous");
    loader.load(
      url,
      (tex) => {
        tex.colorSpace = THREE.SRGBColorSpace;
        tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
        textures[siteKey] = tex;
        resolve(tex);
      },
      undefined,
      () => resolve(null)
    );
  });
}

/* ---------- build the scene for one region ---------- */
function clearScene() {
  for (const obj of [surfaceMesh, basePlane, frameLine]) {
    if (!obj) continue;
    scene.remove(obj);
    obj.geometry.dispose();
    if (obj.material.dispose) obj.material.dispose();
  }
  surfaceMesh = basePlane = frameLine = null;
  beaconGroup.clear();
  sinkholeGroup.clear();
}

function buildSurfaceForSite(siteKey) {
  activeSite = siteKey;
  const region = bundle.regions[siteKey];
  clearScene();
  cache = prepare(region);
  hideInspector();

  const { rows, cols, step_deg, bbox } = region;
  const [w, , , n] = bbox;
  const { width, depth } = regionDims(region);

  // imagery plane (flat, at height 0)
  const planeMat = new THREE.MeshBasicMaterial({ color: 0xcfd6df });
  basePlane = new THREE.Mesh(new THREE.PlaneGeometry(width, depth), planeMat);
  basePlane.rotation.x = -Math.PI / 2;
  scene.add(basePlane);
  loadBasemap(siteKey, region).then((tex) => {
    if (!tex || activeSite !== siteKey || !basePlane) return;
    basePlane.material.map = tex;
    basePlane.material.color.set(0xe9e9e9); // slightly toned down so the radar colours stand out
    basePlane.material.needsUpdate = true;
  });

  // thin frame around the scene
  const frameGeo = new THREE.EdgesGeometry(new THREE.BoxGeometry(width, 0.001, depth));
  frameLine = new THREE.LineSegments(frameGeo, new THREE.LineBasicMaterial({ color: 0x0b3d91, transparent: true, opacity: 0.45 }));
  scene.add(frameLine);

  // full-grid surface: gaps stay in the mesh but fade out (alpha 0)
  const pos = new Float32Array(rows * cols * 3);
  const col = new Float32Array(rows * cols * 4);
  for (let r = 0; r < rows; r++) {
    const lat = n - (r + 0.5) * step_deg;
    for (let c = 0; c < cols; c++) {
      const i = r * cols + c;
      const lon = w + (c + 0.5) * step_deg;
      const p = lonLatToWorld(lon, lat, region);
      pos[i * 3] = p.x;
      pos[i * 3 + 2] = p.z;
    }
  }
  const indices = [];
  for (let r = 0; r < rows - 1; r++) {
    for (let c = 0; c < cols - 1; c++) {
      const a = r * cols + c, b = a + 1, d = a + cols, e = d + 1;
      indices.push(a, d, b, b, d, e);
    }
  }
  const geom = new THREE.BufferGeometry();
  geom.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  geom.setAttribute("color", new THREE.BufferAttribute(col, 4));
  geom.setIndex(indices);
  surfaceMesh = new THREE.Mesh(
    geom,
    new THREE.MeshStandardMaterial({ vertexColors: true, transparent: true, roughness: 0.75, metalness: 0, side: THREE.DoubleSide })
  );
  scene.add(surfaceMesh);

  // pins
  addPin(region.reference_point.lon, region.reference_point.lat, 0x1f7a35, {
    title: "Reference area",
    lon: region.reference_point.lon,
    lat: region.reference_point.lat,
    detail: `Motion is measured relative to this stable area (mean coherence ${region.reference_point.mean_coh}).`,
  });
  addPin(region.max_subsidence_location.lon, region.max_subsidence_location.lat, 0xe69f00, {
    title: `Largest sinking · ${region.max_subsidence_location.label}`,
    lon: region.max_subsidence_location.lon,
    lat: region.max_subsidence_location.lat,
    detail: `${region.max_subsidence_cm} cm along the line of sight, ${region.dates[0]} to ${region.dates.at(-1)}.`,
  });

  // Karapınar sinkholes
  const hasSinkholes = Array.isArray(region.sinkholes) && region.sinkholes.length > 0;
  sinkholeToggleWrap.hidden = !hasSinkholes;
  sinkholeGroup.visible = hasSinkholes && sinkholeToggle.checked;
  if (hasSinkholes) {
    const [bw, bs, be, bn] = region.bbox;
    const inside = region.sinkholes.filter((sk) => sk.lon >= bw && sk.lon <= be && sk.lat >= bs && sk.lat <= bn);
    $("sinkCount").textContent = `Show ${inside.length} of ${region.sinkholes.length} mapped sinkholes in view`;
    inside.forEach((sk) => {
      const wp = lonLatToWorld(sk.lon, sk.lat, region);
      // short marker standing on the surface; depth and size are shown when it is clicked
      const colHeight = 0.2;
      const isWater = sk.status === "water-bearing";
      const color = isWater ? 0x2f7fd1 : 0xc8321f;
      const mesh = new THREE.Mesh(
        new THREE.CylinderGeometry(0.07, 0.07, colHeight, 16),
        new THREE.MeshStandardMaterial({ color, roughness: 0.4 })
      );
      mesh.position.set(wp.x, 0.2, wp.z);
      mesh.userData.sinkhole = sk;
      mesh.userData.anchor = { lon: sk.lon, lat: sk.lat, offsetY: colHeight * 0.5 };
      sinkholeGroup.add(mesh);
    });
  }

  // page text
  $("regionTitle").textContent = region.title;
  $("regionSubtitle").textContent = `${region.n_pairs} radar pairs · ${region.dates[0]} to ${region.dates.at(-1)} (${region.days} days)`;
  $("minLbl").textContent = `${region.vmin} cm`;
  $("maxLbl").textContent = `+${region.vmax} cm`;
  $("legendNote").textContent =
    "Red = moved away from the satellite (sinking). Bare satellite image = no reliable radar signal.";
  $("metaRef").textContent = `${fmtLatLon(region.reference_point.lat, region.reference_point.lon)} (coherence ${region.reference_point.mean_coh})`;
  $("metaCov").textContent = `${Math.round(region.valid_frac * 100)}% of the area has a reliable signal in every pair. Surface lightly smoothed (3×3). ${cols}×${rows} grid.`;
  $("metaNotes").textContent = region.notes;

  const maxIdx = region.dates.length - 1;
  epochSlider.max = String(maxIdx);
  epochSlider.value = String(maxIdx);
  $("dateTicks").innerHTML = region.dates.map((d) => `<span>${d.slice(5)}</span>`).join("");

  updateSurfaceEpoch(maxIdx);
}

function addPin(lon, lat, colorHex, info) {
  const region = bundle.regions[activeSite];
  const wp = lonLatToWorld(lon, lat, region);
  const sphere = new THREE.Mesh(
    new THREE.SphereGeometry(0.12, 16, 16),
    new THREE.MeshStandardMaterial({ color: colorHex, roughness: 0.35 })
  );
  sphere.position.set(wp.x, 0.4, wp.z);
  sphere.userData.pinInfo = info;
  sphere.userData.anchor = { lon, lat, offsetY: 0.4 };
  const stem = new THREE.Mesh(
    new THREE.CylinderGeometry(0.018, 0.018, 0.4, 8),
    new THREE.MeshBasicMaterial({ color: colorHex })
  );
  stem.position.set(wp.x, 0.2, wp.z);
  stem.userData.anchor = { lon, lat, offsetY: 0.2 };
  beaconGroup.add(sphere, stem);
}

function cellAt(lon, lat, region) {
  const [w, s, e, n] = region.bbox;
  const c = Math.max(0, Math.min(region.cols - 1, Math.floor(((lon - w) / (e - w || 1)) * region.cols)));
  const r = Math.max(0, Math.min(region.rows - 1, Math.floor(((n - lat) / (n - s || 1)) * region.rows)));
  return r * region.cols + c;
}

/* ---------- per-frame surface update ---------- */
function updateSurfaceEpoch(epochFloat) {
  if (!surfaceMesh || !bundle || !cache) return;
  const region = bundle.regions[activeSite];
  const pos = surfaceMesh.geometry.attributes.position;
  const col = surfaceMesh.geometry.attributes.color;
  const n = region.rows * region.cols;

  // keep the whole sheet above the imagery even at the deepest sinking
  lift = Math.abs(cmToWorldY(region.vmin, region)) + 0.12;

  for (let i = 0; i < n; i++) {
    const v = valueAt(i, epochFloat);
    pos.setY(i, lift + cmToWorldY(v, region));
    const [r, g, b] = rdbuColor(v, region.vmin, region.vmax);
    col.setXYZW(i, r, g, b, cache.mask[i] ? SURFACE_ALPHA : 0);
  }
  pos.needsUpdate = true;
  col.needsUpdate = true;
  surfaceMesh.geometry.computeVertexNormals();

  for (const group of [beaconGroup, sinkholeGroup]) {
    for (const obj of group.children) {
      const a = obj.userData.anchor;
      if (!a) continue;
      const idx = cellAt(a.lon, a.lat, region);
      // on the radar surface where there is a measurement, otherwise on the satellite image
      const ground = cache.mask[idx] ? lift + cmToWorldY(valueAt(idx, epochFloat), region) : 0;
      obj.position.y = ground + a.offsetY;
    }
  }

  const i0 = Math.min(region.dates.length - 1, Math.round(epochFloat));
  $("stampDate").textContent = new Date(region.dates[i0] + "T00:00:00Z")
    .toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric", timeZone: "UTC" })
    .toUpperCase();
  $("stampSub").textContent = `Sinking since ${region.dates[0].slice(5)} · pair ${i0} of ${region.dates.length - 1}`;
}

/* ---------- inspector ---------- */
function showInspectorHTML(html) {
  inspectorBox.hidden = false;
  inspectorBox.innerHTML = `<button class="x" type="button" aria-label="Close">×</button>${html}`;
  inspectorBox.querySelector(".x").addEventListener("click", hideInspector);
}
function hideInspector() { inspectorBox.hidden = true; }

let downAt = null;
renderer.domElement.addEventListener("pointerdown", (e) => { downAt = { x: e.clientX, y: e.clientY }; });
renderer.domElement.addEventListener("pointerup", (e) => {
  if (downAt && Math.hypot(e.clientX - downAt.x, e.clientY - downAt.y) < 5) handlePointerPick(e); // a click, not a drag
  downAt = null;
});

function handlePointerPick(ev) {
  if (!bundle) return;
  const rect = renderer.domElement.getBoundingClientRect();
  pointer.x = ((ev.clientX - rect.left) / rect.width) * 2 - 1;
  pointer.y = -((ev.clientY - rect.top) / rect.height) * 2 + 1;
  raycaster.setFromCamera(pointer, camera);
  const region = bundle.regions[activeSite];

  if (sinkholeGroup.visible) {
    const hit = raycaster.intersectObjects(sinkholeGroup.children, false)[0];
    if (hit) {
      const sk = hit.object.userData.sinkhole;
      showInspectorHTML(`
        <strong>${sk.name}</strong>
        <div class="chip-row">
          <span class="chip">Formed ${sk.year_formed}</span>
          <span class="chip">Depth ${sk.depth_m} m</span>
          <span class="chip">Width ${sk.diameter_m} m</span>
          <span class="chip">${sk.status}</span>
        </div>
        <div class="mono">${fmtLatLon(sk.lat, sk.lon)}</div>
        <div>Source: <a href="${sk.source_url}" target="_blank" rel="noopener">${sk.source_title}</a></div>`);
      return;
    }
  }

  for (const h of raycaster.intersectObjects(beaconGroup.children, false)) {
    const p = h.object.userData.pinInfo;
    if (p) {
      showInspectorHTML(`<strong>${p.title}</strong><div class="mono">${fmtLatLon(p.lat, p.lon)}</div><div>${p.detail}</div>`);
      return;
    }
  }

  const hit = raycaster.intersectObjects([surfaceMesh, basePlane], false)[0];
  if (hit) {
    const [w, s, e, n] = region.bbox;
    const { width, depth } = regionDims(region);
    const lon = w + (hit.point.x / width + 0.5) * (e - w);
    const lat = n - (hit.point.z / depth + 0.5) * (n - s);
    const idx = cellAt(lon, lat, region);
    if (cache.mask[idx]) {
      const i0 = Math.min(region.dates.length - 1, Math.round(Number(epochSlider.value)));
      const v = region.grids[i0][idx];
      showInspectorHTML(`
        <strong>Radar measurement</strong>
        <div class="mono">${fmtLatLon(lat, lon)}</div>
        <div>Line-of-sight motion: <strong class="mono">${v.toFixed(2)} cm</strong></div>
        <div class="hint">${v < 0 ? "Negative = moved away from the satellite (sinking)." : "Positive = moved toward the satellite."}</div>`);
    } else {
      showInspectorHTML(`
        <strong>No reliable radar signal</strong>
        <div class="mono">${fmtLatLon(lat, lon)}</div>
        <div class="hint">Fields changed between radar passes, so motion cannot be measured here. This is not the same as no sinking.</div>`);
    }
  }
}

/* ---------- controls ---------- */
function setPlaying(on) {
  playing = on;
  playBtn.classList.toggle("on", on);
  playBtn.setAttribute("aria-label", on ? "Pause" : "Play");
}
epochSlider.addEventListener("input", () => { setPlaying(false); updateSurfaceEpoch(Number(epochSlider.value)); });
exagSlider.addEventListener("input", () => {
  exagLabel.textContent = Number(exagSlider.value).toLocaleString("en-US");
  updateSurfaceEpoch(Number(epochSlider.value));
});
sinkholeToggle.addEventListener("change", () => { sinkholeGroup.visible = sinkholeToggle.checked; });
playBtn.addEventListener("click", () => setPlaying(!playing));
$("resetCamBtn").addEventListener("click", setCameraDefault);

// sliding bar for the region switch
function placeSeg() {
  const seg = $("regionSeg");
  const on = seg.querySelector(".seg-btn.active");
  const thumb = seg.querySelector(".seg-thumb");
  if (!on || !thumb || !on.offsetWidth) return;
  const first = !seg.dataset.placed;
  if (first) thumb.style.transition = "none";
  thumb.style.width = `${on.offsetWidth - 6}px`;
  thumb.style.transform = `translateX(${on.offsetLeft + 3}px)`;
  if (first) { void thumb.offsetWidth; thumb.style.transition = ""; seg.dataset.placed = "1"; }
}
document.querySelectorAll(".tab").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((b) => {
      b.classList.toggle("active", b === btn);
      b.setAttribute("aria-selected", String(b === btn));
    });
    placeSeg();
    setPlaying(false);
    buildSurfaceForSite(btn.dataset.site);
    setCameraDefault();
  });
});

// info window
$("infoBtn").addEventListener("click", () => { $("infoModal").hidden = false; });
$("closeInfo").addEventListener("click", () => { $("infoModal").hidden = true; });
$("infoModal").addEventListener("click", (e) => { if (e.target === $("infoModal")) $("infoModal").hidden = true; });
document.addEventListener("keydown", (e) => { if (e.key === "Escape") $("infoModal").hidden = true; });

window.addEventListener("resize", () => {
  camera.aspect = host.clientWidth / host.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(host.clientWidth, host.clientHeight);
  placeSeg();
});
if (window.ResizeObserver) new ResizeObserver(placeSeg).observe($("regionSeg"));
if (document.fonts && document.fonts.ready) document.fonts.ready.then(placeSeg);

function animate(now) {
  requestAnimationFrame(animate);
  const dt = Math.min(0.1, (now - lastFrame) * 0.001);
  lastFrame = now;
  if (playing && bundle) {
    const maxIdx = bundle.regions[activeSite].dates.length - 1;
    let next = Number(epochSlider.value) + dt * 0.75;
    if (next > maxIdx) next = 0;
    epochSlider.value = String(next);
    updateSurfaceEpoch(next);
  }
  controls.update();
  renderer.render(scene, camera);
}

fetch("surfaces.json")
  .then((r) => r.json())
  .then((data) => {
    bundle = data;
    buildSurfaceForSite("central_valley");
    placeSeg();
    requestAnimationFrame(animate);
  })
  .catch((err) => {
    $("regionTitle").textContent = `Could not load the 3D data: ${err.message}`;
  });
