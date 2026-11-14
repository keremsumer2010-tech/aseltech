import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

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

const host = document.getElementById("canvasHost");
const epochSlider = document.getElementById("epochSlider");
const epochLabel = document.getElementById("epochLabel");
const exagSlider = document.getElementById("exagSlider");
const exagLabel = document.getElementById("exagLabel");
const playBtn = document.getElementById("playBtn");
const resetCamBtn = document.getElementById("resetCamBtn");
const wireToggle = document.getElementById("wireToggle");
const sinkholeToggle = document.getElementById("sinkholeToggle");
const sinkholeToggleWrap = document.getElementById("sinkholeToggleWrap");
const inspectorBox = document.getElementById("inspectorBox");

const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x0b1016, 0.012);

const camera = new THREE.PerspectiveCamera(45, host.clientWidth / host.clientHeight, 0.1, 200);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(host.clientWidth, host.clientHeight);
host.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.07;
controls.maxPolarAngle = Math.PI * 0.49;

scene.add(new THREE.AmbientLight(0xffffff, 0.72));
const dirLight = new THREE.DirectionalLight(0xffffff, 0.85);
dirLight.position.set(10, 18, 12);
scene.add(dirLight);
const rimLight = new THREE.DirectionalLight(0x60a5fa, 0.35);
rimLight.position.set(-12, 8, -10);
scene.add(rimLight);

const WORLD_SPAN = 14.0;
let bundle = null;
let activeSite = "central_valley";
let surfaceMesh = null;
let wireMesh = null;
let datumGrid = null;
let beaconGroup = new THREE.Group();
let sinkholeGroup = new THREE.Group();
scene.add(beaconGroup);
scene.add(sinkholeGroup);

let meshIndexMeta = [];
let playing = false;
let lastFrame = performance.now();

const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();

function setCameraDefault() {
  camera.position.set(0, 10.5, 13.5);
  controls.target.set(0, -0.3, 0);
  controls.update();
}
setCameraDefault();

function lonLatToWorld(lon, lat, region) {
  const [w, s, e, n] = region.bbox;
  const midLatRad = ((s + n) * 0.5 * Math.PI) / 180;
  const aspect = ((e - w) * Math.cos(midLatRad)) / (n - s || 1);
  const width = WORLD_SPAN;
  const depth = WORLD_SPAN / aspect;
  const u = (lon - w) / (e - w || 1) - 0.5;
  const v = (n - lat) / (n - s || 1) - 0.5;
  return { x: u * width, z: v * depth, width, depth };
}

function cmToWorldY(cm, region) {
  // Horizontal physical span in km -> real meters -> convert cm scaled by exaggeration into world units
  const [w, s, e] = region.bbox;
  const midLatRad = ((s + region.bbox[3]) * 0.5 * Math.PI) / 180;
  const realWidthMeters = (e - w) * 111320 * Math.cos(midLatRad);
  const metersPerWorldUnit = realWidthMeters / WORLD_SPAN;
  const exag = Number(exagSlider.value);
  return ((cm * 0.01) * exag) / metersPerWorldUnit;
}

function buildSurfaceForSite(siteKey) {
  activeSite = siteKey;
  const region = bundle.regions[siteKey];

  if (surfaceMesh) {
    scene.remove(surfaceMesh);
    surfaceMesh.geometry.dispose();
    surfaceMesh.material.dispose();
    surfaceMesh = null;
  }
  if (wireMesh) {
    scene.remove(wireMesh);
    wireMesh.geometry.dispose();
    wireMesh.material.dispose();
    wireMesh = null;
  }
  if (datumGrid) {
    scene.remove(datumGrid);
    datumGrid = null;
  }
  beaconGroup.clear();
  sinkholeGroup.clear();

  const { rows, cols, step_deg, bbox, grids } = region;
  const [w, , , n] = bbox;
  const refGrid = grids[grids.length - 1];

  const posArr = [];
  const colArr = [];
  const gridToVert = new Int32Array(rows * cols).fill(-1);
  meshIndexMeta = [];

  for (let r = 0; r < rows; r++) {
    const lat = n - (r + 0.5) * step_deg;
    for (let c = 0; c < cols; c++) {
      const idx = r * cols + c;
      if (refGrid[idx] === null) continue;
      const lon = w + (c + 0.5) * step_deg;
      const pt = lonLatToWorld(lon, lat, region);
      const vIdx = posArr.length / 3;
      gridToVert[idx] = vIdx;
      posArr.push(pt.x, 0, pt.z);
      colArr.push(0.8, 0.8, 0.8);
      meshIndexMeta.push({ r, c, idx, lon, lat });
    }
  }

  const indices = [];
  for (let r = 0; r < rows - 1; r++) {
    for (let c = 0; c < cols - 1; c++) {
      const a = gridToVert[r * cols + c];
      const b = gridToVert[r * cols + c + 1];
      const d = gridToVert[(r + 1) * cols + c];
      const e = gridToVert[(r + 1) * cols + c + 1];
      if (a >= 0 && b >= 0 && d >= 0) indices.push(a, d, b);
      if (b >= 0 && d >= 0 && e >= 0) indices.push(b, d, e);
    }
  }

  const geom = new THREE.BufferGeometry();
  geom.setAttribute("position", new THREE.Float32BufferAttribute(posArr, 3));
  geom.setAttribute("color", new THREE.Float32BufferAttribute(colArr, 3));
  geom.setIndex(indices);
  geom.userData.gridToVert = gridToVert;

  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.62,
    metalness: 0.08,
    side: THREE.DoubleSide,
  });
  surfaceMesh = new THREE.Mesh(geom, mat);
  scene.add(surfaceMesh);

  const wireMat = new THREE.MeshBasicMaterial({
    color: 0xffffff,
    wireframe: true,
    transparent: true,
    opacity: 0.14,
  });
  wireMesh = new THREE.Mesh(geom, wireMat);
  wireMesh.visible = wireToggle.checked;
  scene.add(wireMesh);

  const dims = lonLatToWorld(region.bbox[2], region.bbox[1], region);
  datumGrid = new THREE.GridHelper(Math.max(dims.width, dims.depth) * 1.05, 16, 0x334155, 0x1e293b);
  datumGrid.position.y = -0.005;
  scene.add(datumGrid);

  // Reference & Peak Subsidence pins
  addPin(region.reference_point.lon, region.reference_point.lat, 0x22c55e, {
    title: "InSAR Reference Window",
    lon: region.reference_point.lon,
    lat: region.reference_point.lat,
    detail: `Mean coherence: ${region.reference_point.mean_coh}`,
  });
  addPin(region.max_subsidence_location.lon, region.max_subsidence_location.lat, 0xfbbf24, {
    title: `Peak LOS Subsidence (${region.max_subsidence_location.label})`,
    lon: region.max_subsidence_location.lon,
    lat: region.max_subsidence_location.lat,
    detail: `${region.max_subsidence_cm} cm LOS (${region.dates[0]} → ${region.dates.at(-1)})`,
  });

  // Karapinar verified sinkhole 3D columns
  const hasSinkholes = Array.isArray(region.sinkholes) && region.sinkholes.length > 0;
  sinkholeToggleWrap.classList.toggle("hidden", !hasSinkholes);
  sinkholeGroup.visible = hasSinkholes && sinkholeToggle.checked;
  if (hasSinkholes) {
    region.sinkholes.forEach((sk) => {
      const wp = lonLatToWorld(sk.lon, sk.lat, region);
      const colHeight = Math.max(0.35, 0.25 + (Number(sk.depth_m) || 2) * 0.025);
      const isWater = sk.status === "water-bearing";
      const color = isWater ? 0x38bdf8 : 0xf43f5e;
      const cylGeo = new THREE.CylinderGeometry(0.055, 0.03, colHeight, 12);
      const cylMat = new THREE.MeshStandardMaterial({
        color,
        emissive: isWater ? 0x0c4a6e : 0x4c0519,
        roughness: 0.35,
      });
      const colMesh = new THREE.Mesh(cylGeo, cylMat);
      colMesh.position.set(wp.x, 0.35 - colHeight * 0.5, wp.z);
      colMesh.userData.sinkhole = sk;
      sinkholeGroup.add(colMesh);
    });
  }

  // UI headers & slider setup
  document.getElementById("regionSubtitle").textContent = `${region.title} — ${region.subtitle}`;
  document.getElementById("statDates").textContent = `${region.dates[0]} → ${region.dates.at(-1)} (${region.days} d)`;
  document.getElementById("statPeak").textContent =
    `${region.max_subsidence_cm} cm LOS (${region.max_subsidence_location.label})`;
  document.getElementById("statPercentiles").textContent =
    `${region.p2_cm} / ${region.median_cm} / ${region.p98_cm} cm`;
  document.getElementById("minLbl").textContent = `${region.vmin} cm`;
  document.getElementById("maxLbl").textContent = `+${region.vmax} cm`;
  document.getElementById("metaRef").textContent =
    `${region.reference_point.lat}°N, ${region.reference_point.lon}°E (coh ${region.reference_point.mean_coh})`;
  document.getElementById("metaCov").textContent =
    `${Math.round(region.valid_frac * 100)}% unmasked · ${cols}×${rows} 3D grid`;
  document.getElementById("metaNotes").textContent = region.notes;

  const maxIdx = region.dates.length - 1;
  epochSlider.max = String(maxIdx);
  epochSlider.value = String(maxIdx);
  const ticks = document.getElementById("dateTicks");
  ticks.innerHTML = region.dates.map((d) => `<span>${d.slice(5)}</span>`).join("");

  updateSurfaceEpoch(maxIdx);
}

function addPin(lon, lat, colorHex, info) {
  const region = bundle.regions[activeSite];
  const wp = lonLatToWorld(lon, lat, region);
  const sphere = new THREE.Mesh(
    new THREE.SphereGeometry(0.14, 16, 16),
    new THREE.MeshStandardMaterial({ color: colorHex, emissive: colorHex, emissiveIntensity: 0.35 })
  );
  sphere.position.set(wp.x, 0.38, wp.z);
  sphere.userData.pinInfo = info;
  const stem = new THREE.Mesh(
    new THREE.CylinderGeometry(0.02, 0.02, 0.4, 8),
    new THREE.MeshBasicMaterial({ color: colorHex })
  );
  stem.position.set(wp.x, 0.18, wp.z);
  beaconGroup.add(sphere, stem);
}

function interpolateValue(region, idx, epochFloat) {
  const i0 = Math.floor(epochFloat);
  const i1 = Math.min(region.grids.length - 1, i0 + 1);
  const alpha = epochFloat - i0;
  const v0 = region.grids[i0][idx];
  const v1 = region.grids[i1][idx];
  if (v0 === null || v1 === null) return null;
  return v0 + (v1 - v0) * alpha;
}

function updateSurfaceEpoch(epochFloat) {
  if (!surfaceMesh || !bundle) return;
  const region = bundle.regions[activeSite];
  const pos = surfaceMesh.geometry.attributes.position;
  const col = surfaceMesh.geometry.attributes.color;

  for (let v = 0; v < meshIndexMeta.length; v++) {
    const val = interpolateValue(region, meshIndexMeta[v].idx, epochFloat);
    if (val === null) continue;
    pos.setY(v, cmToWorldY(val, region));
    const [r, g, b] = rdbuColor(val, region.vmin, region.vmax);
    col.setXYZ(v, r, g, b);
  }
  pos.needsUpdate = true;
  col.needsUpdate = true;
  surfaceMesh.geometry.computeVertexNormals();

  const i0 = Math.floor(epochFloat);
  const i1 = Math.min(region.dates.length - 1, i0 + 1);
  epochLabel.textContent = i0 === i1 ? region.dates[i0] : `${region.dates[i0]} → ${region.dates[i1]}`;
}

function showInspectorHTML(html) {
  inspectorBox.className = "inspector-card";
  inspectorBox.innerHTML = html;
}

function handlePointerPick(ev) {
  if (!bundle) return;
  const rect = renderer.domElement.getBoundingClientRect();
  pointer.x = ((ev.clientX - rect.left) / rect.width) * 2 - 1;
  pointer.y = -((ev.clientY - rect.top) / rect.height) * 2 + 1;
  raycaster.setFromCamera(pointer, camera);

  if (sinkholeGroup.visible) {
    const skHits = raycaster.intersectObjects(sinkholeGroup.children, false);
    if (skHits.length > 0) {
      const sk = skHits[0].object.userData.sinkhole;
      showInspectorHTML(`
        <strong>${sk.name}</strong>
        <div class="chip-row">
          <span class="chip">Formed: ${sk.year_formed}</span>
          <span class="chip">Depth: ${sk.depth_m} m</span>
          <span class="chip">Dia: ${sk.diameter_m} m</span>
          <span class="chip">${sk.status}</span>
        </div>
        <div>Coords: <span class="mono">${sk.lat}°N, ${sk.lon}°E</span></div>
        <div>Source: <a href="${sk.source_url}" target="_blank" rel="noopener">${sk.source_title}</a></div>
      `);
      return;
    }
  }

  const pinHits = raycaster.intersectObjects(beaconGroup.children, false);
  for (const h of pinHits) {
    if (h.object.userData.pinInfo) {
      const p = h.object.userData.pinInfo;
      showInspectorHTML(`
        <strong>${p.title}</strong>
        <div>Coords: <span class="mono">${p.lat}, ${p.lon}</span></div>
        <div>${p.detail}</div>
      `);
      return;
    }
  }

  if (surfaceMesh) {
    const hits = raycaster.intersectObject(surfaceMesh, false);
    if (hits.length > 0 && hits[0].face) {
      const vIdx = hits[0].face.a;
      const meta = meshIndexMeta[vIdx];
      const region = bundle.regions[activeSite];
      const val = interpolateValue(region, meta.idx, Number(epochSlider.value));
      showInspectorHTML(`
        <strong>Radar Grid Sample</strong>
        <div>Coords: <span class="mono">${meta.lat.toFixed(4)}°, ${meta.lon.toFixed(4)}°</span></div>
        <div>LOS Displacement: <strong class="mono">${val !== null ? val.toFixed(2) : "—"} cm</strong></div>
        <div class="hint">${val < 0 ? "Negative LOS = motion away from radar (subsidence)." : "Positive LOS = motion toward radar."}</div>
      `);
    }
  }
}

renderer.domElement.addEventListener("click", handlePointerPick);

epochSlider.addEventListener("input", () => {
  playing = false;
  playBtn.textContent = "Play Breathing Loop";
  updateSurfaceEpoch(Number(epochSlider.value));
});

exagSlider.addEventListener("input", () => {
  exagLabel.textContent = `${Number(exagSlider.value).toLocaleString()}×`;
  updateSurfaceEpoch(Number(epochSlider.value));
});

wireToggle.addEventListener("change", () => {
  if (wireMesh) wireMesh.visible = wireToggle.checked;
});

sinkholeToggle.addEventListener("change", () => {
  sinkholeGroup.visible = sinkholeToggle.checked;
});

playBtn.addEventListener("click", () => {
  playing = !playing;
  playBtn.textContent = playing ? "Pause Loop" : "Play Breathing Loop";
});

resetCamBtn.addEventListener("click", setCameraDefault);

document.querySelectorAll(".tab").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((b) => {
      b.classList.remove("active");
      b.setAttribute("aria-selected", "false");
    });
    btn.classList.add("active");
    btn.setAttribute("aria-selected", "true");
    playing = false;
    playBtn.textContent = "Play Breathing Loop";
    buildSurfaceForSite(btn.dataset.site);
  });
});

window.addEventListener("resize", () => {
  camera.aspect = host.clientWidth / host.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(host.clientWidth, host.clientHeight);
});

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

const backLink = document.getElementById("backLink");
if (backLink) {
  fetch("../index.html", { method: "HEAD", cache: "no-cache" })
    .then((r) => {
      if (r.ok) backLink.setAttribute("href", "../");
    })
    .catch(() => {});
}

fetch("surfaces.json")
  .then((r) => r.json())
  .then((data) => {
    bundle = data;
    buildSurfaceForSite("central_valley");
    requestAnimationFrame(animate);
  })
  .catch((err) => {
    inspectorBox.textContent = `Failed to load 3D surfaces: ${err.message}`;
  });
