// NISAR 3D — real orbit (SGP4 from CelesTrak TLE), left-looking SweepSAR swath,
// and the atlas measurement revealed as the swath passes. PC1, Team Aseltech.
import * as THREE from './vendor/three/three.module.min.js';
import { OrbitControls } from './vendor/three/OrbitControls.js';

const SAT = window.satellite;
const ROOT = location.pathname.includes('/web/') ? '../' : './';
const R_E = 6371.0;                 // km, spherical Earth for drawing
const INC_NEAR = 33, INC_FAR = 47;  // deg, NISAR L-band incidence range (mission spec)
const D2R = Math.PI / 180;
const MODEL_EXAG = 4000;            // spacecraft drawn 4000x real size so it is visible

// ---------- small math helpers (ECI/ECEF km  ->  three.js: x, z, -y) ----------
const v3 = (p) => new THREE.Vector3(p.x, p.z, -p.y);
const unitFromLatLon = (lat, lon) => {
  const la = lat * D2R, lo = lon * D2R;
  return new THREE.Vector3(Math.cos(la) * Math.cos(lo), Math.sin(la), -Math.cos(la) * Math.sin(lo));
};
const rotY = (v, a) => v.clone().applyAxisAngle(new THREE.Vector3(0, 1, 0), a);
const fmtUTC = (d) => d.toISOString().replace('T', ' ').slice(0, 19) + ' UTC';

function rateColor(rate){
  if (typeof rate !== 'number') return '#94a3b8';
  if (rate <= -6) return '#ef4444';
  if (rate <= -4) return '#f97316';
  if (rate <= -2) return '#f59e0b';
  return '#94a3b8';
}

// Sun direction in ECI (low-precision almanac, good to ~0.01 deg; enough for shading).
function sunEci(date){
  const jd = date.getTime() / 86400000 + 2440587.5, n = jd - 2451545.0;
  const L = (280.46 + 0.9856474 * n) % 360, g = ((357.528 + 0.9856003 * n) % 360) * D2R;
  const lam = (L + 1.915 * Math.sin(g) + 0.02 * Math.sin(2 * g)) * D2R, eps = (23.439 - 0.0000004 * n) * D2R;
  return v3({x: Math.cos(lam), y: Math.cos(eps) * Math.sin(lam), z: Math.sin(eps) * Math.sin(lam)}).normalize();
}

// Ground point at Earth-central angle `gamma` from nadir toward unit direction `side`.
const groundAt = (nadirU, sideU, gamma, r = R_E) =>
  nadirU.clone().multiplyScalar(Math.cos(gamma)).add(sideU.clone().multiplyScalar(Math.sin(gamma))).multiplyScalar(r);

// Incidence angle -> Earth-central angle for orbit radius rs.
function centralAngle(incDeg, rs){
  const th = incDeg * D2R, alpha = Math.asin(R_E * Math.sin(th) / rs);
  return th - alpha;
}

// ---------- module state ----------
let root, renderer, scene, camera, controls, earth, earthMat, atmo, stars, sunLight;
let satrec = null, tle = null, sat, satGlow, orbitLine, beamGroup, txFan, rxFan, foot, strip, stripEdge;
let cityGroup, cityDecal = null, cityMarker = null, cityDots;
let hud = {}, labelSat, labelCity;
let simMs = Date.now(), speed = 1, mode = 'live', camMode = 'orbit', running = false, lastT = 0;
let pass = null, region = null, regionMeta = null, revealState = null, stripBuf = [], lastStripMs = 0, orbitStamp = 0;
let sweepPhase = 0, snapFollow = false, snapCraft = false, lastSatPos = null, frameDt = 0.016;

// ---------- public API ----------
export async function open(container, reg){
  if (!root) await build(container);
  root.hidden = false;
  running = true; lastT = performance.now();
  resize();
  if (reg) await selectRegion(reg);
  requestAnimationFrame(loop);
}
export function close(){ running = false; if (root) root.hidden = true; if (document.fullscreenElement) document.exitFullscreen?.(); }
export function isOpen(){ return running; }
export async function selectRegion(reg){
  region = reg; regionMeta = null; pass = null; revealState = null;
  setCaption(`Computing NISAR's next real pass over ${reg.name}…`);
  try{ const r = await fetch(ROOT + (reg.path || `data/global/${reg.id}/`) + 'meta.json'); regionMeta = r.ok ? await r.json() : null; }catch(e){}
  placeCity();
  setTimeout(() => {
    pass = findNextPass(reg.lat, reg.lon, Date.now());
    if (pass){
      hud.pass.innerHTML = `Next imaging pass over <b>${esc(reg.name)}</b>: ${fmtUTC(new Date(pass.t))} · ${pass.asc ? 'ascending' : 'descending'} · incidence ${pass.inc.toFixed(1)}°`;
      const hrs = pass.leadMin / 60, lead = hrs >= 24 ? `${Math.floor(hrs / 24)} d ${Math.round(hrs % 24)} h` : `${Math.floor(hrs)} h ${Math.round(pass.leadMin % 60)} min`;
      setCaption(`NISAR will next image ${esc(reg.name)} in ${lead}. Press <b>Play next pass</b> to fly that real orbit and watch the radar swath record it.`);
    } else {
      hud.pass.textContent = `No pass with ${reg.name} inside the 33–47° swath found in the next 12.5 days.`;
      setCaption('');
    }
  }, 30);
}

// ---------- build ----------
async function build(container){
  root = document.createElement('div');
  root.className = 'n3d';
  root.innerHTML = `
    <canvas class="n3d-canvas"></canvas>
    <div class="n3d-hud">
      <div class="n3d-title"><span class="n3d-dot"></span>NISAR <small>NASA-ISRO SAR · NORAD 65053</small></div>
      <dl>
        <dt>Time</dt><dd id="h-time">—</dd>
        <dt>Position</dt><dd id="h-pos">—</dd>
        <dt>Altitude</dt><dd id="h-alt">—</dd>
        <dt>Speed</dt><dd id="h-vel">—</dd>
        <dt>Pass</dt><dd id="h-dir">—</dd>
        <dt>Radar</dt><dd>L-band 1.239 GHz · 40 MHz · left-looking</dd>
        <dt>Swath</dt><dd>incidence 33–47° · ≈242 km wide</dd>
      </dl>
      <p class="n3d-src" id="h-src">Orbit: SGP4 from CelesTrak TLE.</p>
    </div>
    <div class="n3d-pass" id="h-pass"></div>
    <div class="n3d-caption" id="h-cap"></div>
    <div class="n3d-bar">
      <button type="button" data-act="live" class="is-on">Live</button>
      <button type="button" data-act="pass">Play next pass</button>
      <span class="n3d-sep"></span>
      <button type="button" data-speed="1" class="is-on">1×</button>
      <button type="button" data-speed="60">60×</button>
      <button type="button" data-speed="600">600×</button>
      <span class="n3d-sep"></span>
      <button type="button" data-cam="orbit" class="is-on">Globe</button>
      <button type="button" data-cam="follow">Follow NISAR</button>
      <button type="button" data-cam="craft">Spacecraft</button>
      <span class="n3d-sep"></span>
      <button type="button" data-act="fs" title="Full screen">⛶</button>
      <button type="button" data-act="close" title="Back to atlas map">✕ Map</button>
    </div>
    <div class="n3d-label" id="lbl-sat">NISAR</div>
    <div class="n3d-label n3d-city" id="lbl-city"></div>
    <p class="n3d-note">Spacecraft modelled from NASA/JPL imagery, drawn ${MODEL_EXAG}× real size (12 m reflector, 9 m boom). Orbit, swath geometry and timing are computed, not illustrated.</p>`;
  container.appendChild(root);
  ['time','pos','alt','vel','dir','src','pass','cap'].forEach(k => hud[k] = root.querySelector('#h-' + k));
  labelSat = root.querySelector('#lbl-sat'); labelCity = root.querySelector('#lbl-city');
  root.querySelector('.n3d-bar').addEventListener('click', onBar);

  // TLE: local copy (always), CelesTrak live if the browser allows it.
  tle = await (await fetch(ROOT + 'data/nisar_tle.json')).json();
  try{
    const r = await fetch('https://celestrak.org/NORAD/elements/gp.php?CATNR=65053&FORMAT=TLE', {cache: 'no-store'});
    if (r.ok){ const L = (await r.text()).trim().split(/\r?\n/); if (L[1]?.startsWith('1 65053')){ tle.line1 = L[1].trim(); tle.line2 = L[2].trim(); tle.live = true; } }
  }catch(e){}
  satrec = SAT.twoline2satrec(tle.line1, tle.line2);
  const ep = tleEpoch(tle.line1);
  hud.src.innerHTML = `Orbit: SGP4 from CelesTrak TLE, epoch ${fmtUTC(ep)}${tle.live ? ' (live)' : ''}. Look direction, frequency and bandwidth from NISAR GUNW product metadata.`;

  // renderer + scene
  const canvas = root.querySelector('canvas');
  renderer = new THREE.WebGLRenderer({canvas, antialias: true, alpha: false});
  renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x01030a);
  camera = new THREE.PerspectiveCamera(42, 1, 0.05, 400000);
  camera.position.set(0, 9000, 21000);
  controls = new OrbitControls(camera, canvas);
  controls.enableDamping = true; controls.dampingFactor = 0.08;
  controls.minDistance = 6700; controls.maxDistance = 90000; controls.rotateSpeed = 0.5;

  scene.add(new THREE.AmbientLight(0xffffff, 0.3));
  scene.add(new THREE.HemisphereLight(0xcfe3ff, 0x4a3512, 0.75));   // earthshine fill so the spacecraft reads on the night side
  sunLight = new THREE.DirectionalLight(0xffffff, 2.2); scene.add(sunLight);

  buildStars(); buildEarth(); buildSat(); buildBeam();
  window.addEventListener('resize', resize);
  new ResizeObserver(resize).observe(root);
}

function tleEpoch(line1){
  const yy = +line1.slice(18, 20), doy = +line1.slice(20, 32);
  const y = yy < 57 ? 2000 + yy : 1900 + yy;
  return new Date(Date.UTC(y, 0, 1) + (doy - 1) * 86400000);
}

function buildStars(){
  const n = 3000, pos = new Float32Array(n * 3);
  for (let i = 0; i < n; i++){
    const u = Math.random() * 2 - 1, t = Math.random() * Math.PI * 2, r = 150000;
    const s = Math.sqrt(1 - u * u);
    pos.set([r * s * Math.cos(t), r * u, r * s * Math.sin(t)], i * 3);
  }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  stars = new THREE.Points(g, new THREE.PointsMaterial({color: 0xcfd8ea, size: 1.3, sizeAttenuation: false, transparent: true, opacity: 0.8}));
  scene.add(stars);
}

function buildEarth(){
  earth = new THREE.Group(); scene.add(earth);
  const tex = new THREE.TextureLoader().load(ROOT + 'web/assets/bluemarble_2k.jpg');
  tex.anisotropy = 8;
  earthMat = new THREE.ShaderMaterial({
    uniforms: {day: {value: tex}, sunDir: {value: new THREE.Vector3(1, 0, 0)}},
    vertexShader: `varying vec2 vUv; varying vec3 vN;
      void main(){ vUv = uv; vN = normalize(mat3(modelMatrix) * normal); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `uniform sampler2D day; uniform vec3 sunDir; varying vec2 vUv; varying vec3 vN;
      void main(){
        vec3 c = texture2D(day, vUv).rgb;
        float d = dot(normalize(vN), sunDir);
        float k = smoothstep(-0.12, 0.22, d);
        vec3 night = c * vec3(0.34, 0.40, 0.52) + vec3(0.01, 0.02, 0.045);
        vec3 col = mix(night, c * 1.08, k);
        col += vec3(0.9, 0.45, 0.2) * 0.10 * (1.0 - abs(d * 6.0 - 0.3)) * step(-0.17, d) * step(d, 0.17);
        gl_FragColor = vec4(col, 1.0);
      }`
  });
  earth.add(new THREE.Mesh(new THREE.SphereGeometry(R_E, 160, 80), earthMat));

  atmo = new THREE.Mesh(new THREE.SphereGeometry(R_E * 1.025, 96, 48), new THREE.ShaderMaterial({
    side: THREE.BackSide, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false,
    vertexShader: `varying vec3 vN; void main(){ vN = normalize(normalMatrix * normal); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `varying vec3 vN; void main(){ float i = pow(0.68 - dot(vN, vec3(0.0, 0.0, 1.0)), 4.0); gl_FragColor = vec4(0.32, 0.6, 1.0, 1.0) * i; }`
  }));
  scene.add(atmo);

  // Imaged swath strip (Earth-fixed, grows behind the spacecraft).
  strip = new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshBasicMaterial({color: 0x38bdf8, transparent: true, opacity: 0.22, side: THREE.DoubleSide, depthWrite: false}));
  stripEdge = new THREE.LineSegments(new THREE.BufferGeometry(), new THREE.LineBasicMaterial({color: 0x7dd3fc, transparent: true, opacity: 0.75}));
  earth.add(strip, stripEdge);

  cityGroup = new THREE.Group(); earth.add(cityGroup);
  cityDots = new THREE.Group(); earth.add(cityDots);
  const regions = (typeof atlasData !== 'undefined' && atlasData?.regions) || [];
  regions.forEach(r => {
    if (typeof r.lat !== 'number') return;
    const m = new THREE.Mesh(new THREE.SphereGeometry(18, 12, 8), new THREE.MeshBasicMaterial({color: rateColor(r.rate_cm_per_100d)}));
    m.position.copy(unitFromLatLon(r.lat, r.lon).multiplyScalar(R_E + 4));
    cityDots.add(m);
  });
}

function canvasTex(draw, w = 256, h = 256){
  const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}

function buildSat(){
  // NISAR, modelled from NASA/JPL imagery (PIA26285 and the Aug 2025 deployed-reflector rendering).
  // Local frame: +X along-track, +Y left (radar look side), +Z zenith. Units: metres.
  sat = new THREE.Group();
  const body = new THREE.Group(); sat.add(body);

  // --- materials ---
  const mli = canvasTex((g, w, h) => {            // crinkled gold multi-layer insulation
    g.fillStyle = '#b8860b'; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 900; i++){
      const x = Math.random() * w, y = Math.random() * h, l = 6 + Math.random() * 26, a = Math.random() * Math.PI;
      g.strokeStyle = `rgba(${Math.random() < 0.5 ? '255,226,140' : '120,80,10'},${0.15 + Math.random() * 0.35})`;
      g.lineWidth = 1 + Math.random() * 2; g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); g.stroke();
    }
  }, 256, 256);
  const foil = new THREE.MeshStandardMaterial({map: mli, color: 0xffd36b, metalness: 0.9, roughness: 0.28});
  const silverFoil = new THREE.MeshStandardMaterial({color: 0xd8dde6, metalness: 0.85, roughness: 0.3});
  const radiator = new THREE.MeshStandardMaterial({color: 0xf3f4f6, metalness: 0.1, roughness: 0.45});
  const graphite = new THREE.MeshStandardMaterial({color: 0x2a2d33, metalness: 0.35, roughness: 0.55});
  const strut = new THREE.MeshStandardMaterial({color: 0x1b1d22, metalness: 0.3, roughness: 0.6});
  const node = new THREE.MeshStandardMaterial({color: 0xe5e7eb, metalness: 0.2, roughness: 0.5});

  // --- spacecraft bus (ISRO I-3K class) + radar payload box with radiators ---
  const bus = new THREE.Mesh(new THREE.BoxGeometry(1.9, 1.9, 2.1), foil); bus.position.set(-1.6, 0, 0); body.add(bus);
  const payload = new THREE.Mesh(new THREE.BoxGeometry(4.6, 1.25, 1.1), foil); payload.position.set(1.4, 0, 0.35); body.add(payload);
  for (let i = 0; i < 5; i++){            // white radiator panels along the payload, both sides
    [-1, 1].forEach(sgn => {
      const r = new THREE.Mesh(new THREE.BoxGeometry(0.72, 0.02, 0.62), radiator);
      r.position.set(-0.35 + i * 0.86, sgn * 0.64, 0.3); body.add(r);
    });
  }
  const deck = new THREE.Mesh(new THREE.BoxGeometry(4.4, 1.1, 0.06), silverFoil); deck.position.set(1.4, 0, 0.93); body.add(deck);

  // L-band / S-band feed apertures on top of the payload, facing the reflector.
  const feedTex = canvasTex((g, w, h) => {
    g.fillStyle = '#c9ced8'; g.fillRect(0, 0, w, h);
    g.fillStyle = '#8b93a3';
    for (let i = 0; i < 12; i++) for (let j = 0; j < 3; j++) g.fillRect(6 + i * 20.6, 10 + j * 38, 15, 30);
  }, 256, 128);
  const feed = new THREE.Mesh(new THREE.BoxGeometry(3.4, 0.9, 0.12), new THREE.MeshStandardMaterial({map: feedTex, metalness: 0.4, roughness: 0.5}));
  feed.position.set(1.5, 0.05, 1.02); feed.rotation.x = -0.22; body.add(feed);
  const feedPos = new THREE.Vector3(1.5, 0.05, 1.1);

  // Small Ka/S-band communications dish and GPS mast below the bus.
  const kaProf = []; for (let i = 0; i <= 10; i++){ const r = 0.45 * i / 10; kaProf.push(new THREE.Vector2(r, r * r / 0.9)); }
  const ka = new THREE.Mesh(new THREE.LatheGeometry(kaProf, 24), new THREE.MeshStandardMaterial({color: 0xf1f5f9, metalness: 0.3, roughness: 0.4, side: THREE.DoubleSide}));
  ka.rotation.x = Math.PI; ka.position.set(-1.6, 0.3, -1.45); body.add(ka);
  const kaArm = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.4, 6), node); kaArm.rotation.x = Math.PI / 2; kaArm.position.set(-1.6, 0.3, -1.2); body.add(kaArm);

  // --- two solar-array wings, three panels each ---
  const cells = canvasTex((g, w, h) => {
    g.fillStyle = '#141a2b'; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 16; i++) for (let j = 0; j < 22; j++){
      g.fillStyle = `rgb(${28 + Math.random() * 10},${38 + Math.random() * 10},${70 + Math.random() * 20})`;
      g.fillRect(4 + i * 15.6, 4 + j * 11.4, 14, 10);
    }
    g.strokeStyle = '#9aa4b8'; g.lineWidth = 3; g.strokeRect(1, 1, w - 2, h - 2);
  }, 256, 256);
  const panelMat = new THREE.MeshStandardMaterial({map: cells, metalness: 0.55, roughness: 0.32, side: THREE.DoubleSide});
  const backMat = new THREE.MeshStandardMaterial({color: 0x9ca3af, metalness: 0.3, roughness: 0.7});
  [-1, 1].forEach(sgn => {
    const wing = new THREE.Group();
    const yoke = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 1.2, 6), node);
    yoke.rotation.x = Math.PI / 2; yoke.position.set(0, sgn * 0.6, 0); wing.add(yoke);
    for (let i = 0; i < 3; i++){
      const p = new THREE.Mesh(new THREE.BoxGeometry(1.5, 2.1, 0.04), [backMat, backMat, backMat, backMat, panelMat, backMat]);
      p.position.set(0, sgn * (2.25 + i * 2.15), 0); wing.add(p);
    }
    wing.position.set(-1.6, sgn * 0.95, 0.2);
    wing.rotation.y = 0.35;                   // sun-tracking tilt
    body.add(wing);
  });

  // --- 12 m AstroMesh-type reflector: ring truss drum + gold mesh dish ---
  const R = 6.0, H = 1.5, N = 24;                       // radius, truss depth, bays
  const refl = new THREE.Group();
  const cyl = (a, b, r, mat) => {
    const d = b.clone().sub(a), m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, d.length(), 5), mat);
    m.position.copy(a).add(b).multiplyScalar(0.5); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize()); return m;
  };
  const top = [], bot = [];
  for (let i = 0; i < N; i++){ const a = i / N * Math.PI * 2; top.push(new THREE.Vector3(R * Math.cos(a), H, R * Math.sin(a))); bot.push(new THREE.Vector3(R * Math.cos(a), 0, R * Math.sin(a))); }
  for (let i = 0; i < N; i++){
    const j = (i + 1) % N;
    refl.add(cyl(top[i], top[j], 0.035, strut), cyl(bot[i], bot[j], 0.035, strut), cyl(bot[i], top[i], 0.035, strut));
    refl.add(cyl(i % 2 ? bot[i] : top[i], i % 2 ? top[j] : bot[j], 0.025, strut));       // diagonals
    [top[i], bot[i]].forEach(p => { const s = new THREE.Mesh(new THREE.SphereGeometry(0.07, 8, 6), node); s.position.copy(p); refl.add(s); });
  }
  const meshTex = canvasTex((g, w, h) => {              // gold-plated wire mesh with tension-tie net
    g.fillStyle = '#b07a3a'; g.fillRect(0, 0, w, h);
    g.strokeStyle = 'rgba(255,214,150,.35)'; g.lineWidth = 1;
    for (let i = 0; i < w; i += 4){ g.beginPath(); g.moveTo(i, 0); g.lineTo(i, h); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(w, i); g.stroke(); }
    g.strokeStyle = 'rgba(60,35,10,.55)'; g.lineWidth = 2;
    for (let i = 0; i <= 8; i++){ g.beginPath(); g.moveTo(i * w / 8, 0); g.lineTo(i * w / 8, h); g.stroke(); g.beginPath(); g.moveTo(0, i * h / 8); g.lineTo(w, i * h / 8); g.stroke(); }
  }, 512, 512);
  meshTex.wrapS = meshTex.wrapT = THREE.RepeatWrapping; meshTex.repeat.set(3, 3);
  const prof = []; const depth = 1.1;
  for (let i = 0; i <= 32; i++){ const r = (R - 0.05) * i / 32; prof.push(new THREE.Vector2(r, H * 0.85 - depth + depth * (r / R) * (r / R))); }
  const dish = new THREE.Mesh(new THREE.LatheGeometry(prof, 96), new THREE.MeshStandardMaterial({map: meshTex, color: 0xffc98a, metalness: 0.75, roughness: 0.42, side: THREE.DoubleSide, transparent: true, opacity: 0.93}));
  refl.add(dish);
  // tension ties from the dish to the truss (front net)
  for (let i = 0; i < N; i += 2){ refl.add(cyl(new THREE.Vector3(0, H * 0.85 - depth, 0).lerp(bot[i], 0.55).setY(H * 0.85 - depth + depth * 0.3), bot[i], 0.012, node)); }

  // Reflector pose: concave side faces down toward the feed and the left-hand ground (~37° off nadir).
  const look = new THREE.Vector3(0, Math.sin(37 * D2R), -Math.cos(37 * D2R)).normalize();
  const reflCenter = new THREE.Vector3(1.2, -2.4, 9.8);
  refl.quaternion.setFromUnitVectors(new THREE.Vector3(0, -1, 0), look);   // lathe axis (+Y up) -> concave toward `look`
  refl.position.copy(reflCenter);
  body.add(refl);
  sat.userData.dishCenter = reflCenter.clone();

  // --- 9 m articulated boom from the bus top to the reflector rim (offset feed) ---
  const busTop = new THREE.Vector3(-0.9, -0.5, 1.15);
  refl.updateMatrix();
  let best = null;
  for (const p of bot){ const w = p.clone().applyMatrix4(refl.matrix); if (!best || w.distanceTo(busTop) < best.distanceTo(busTop)) best = w; }
  const elbow1 = busTop.clone().lerp(best, 0.38).add(new THREE.Vector3(0.5, 0.3, 0.2));
  const elbow2 = busTop.clone().lerp(best, 0.72).add(new THREE.Vector3(0.2, 0.15, 0.1));
  [[busTop, elbow1], [elbow1, elbow2], [elbow2, best]].forEach(([a, b]) => body.add(cyl(a, b, 0.13, graphite)));
  [busTop, elbow1, elbow2, best].forEach((p, i) => {
    const h = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.32, 12), i === 1 ? node : graphite);
    h.position.copy(p); body.add(h);
  });
  const disc = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 0.08, 20), node);     // hinge cover seen in JPL renders
  disc.position.copy(elbow2.clone().lerp(best, 0.25)); disc.rotation.z = Math.PI / 2; body.add(disc);

  sat.scale.setScalar(0.001 * MODEL_EXAG);  // metres -> km, exaggerated
  scene.add(sat);

  const glowTex = canvasTex((g, w, h) => {
    const gr = g.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2);
    gr.addColorStop(0, 'rgba(255,240,200,1)'); gr.addColorStop(0.25, 'rgba(125,211,252,.55)'); gr.addColorStop(1, 'rgba(56,189,248,0)');
    g.fillStyle = gr; g.fillRect(0, 0, w, h);
  }, 128, 128);
  satGlow = new THREE.Sprite(new THREE.SpriteMaterial({map: glowTex, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending}));
  scene.add(satGlow);

  orbitLine = new THREE.Line(new THREE.BufferGeometry(), new THREE.LineBasicMaterial({color: 0xfbbf24, transparent: true, opacity: 0.55}));
  scene.add(orbitLine);
}

function buildBeam(){
  beamGroup = new THREE.Group(); scene.add(beamGroup);
  const mk = (color, opacity) => new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshBasicMaterial({color, transparent: true, opacity, side: THREE.DoubleSide, depthWrite: false, blending: THREE.AdditiveBlending}));
  txFan = mk(0x38bdf8, 0.10);   // transmit: whole swath illuminated
  rxFan = mk(0xe0f2fe, 0.33);   // SweepSAR receive beam scanning near -> far range
  foot = mk(0x7dd3fc, 0.45);
  beamGroup.add(txFan, rxFan, foot);
}

// ---------- orbit / geometry ----------
function stateAt(ms){
  const d = new Date(ms);
  const pv = SAT.propagate(satrec, d);
  if (!pv.position) return null;
  const gmst = SAT.gstime(d);
  return {d, gmst, r: v3(pv.position), v: v3(pv.velocity), eci: pv.position, vel: pv.velocity};
}

// Swath corners at time state s, for along-track half-length L (km).
function swathQuad(s, L, f0 = 0, f1 = 1){
  const rs = s.r.length(), up = s.r.clone().normalize(), fwd = s.v.clone().normalize();
  const left = new THREE.Vector3().crossVectors(up, fwd).normalize();     // up x forward = left
  const gN = centralAngle(INC_NEAR, rs), gF = centralAngle(INC_FAR, rs);
  const g0 = gN + (gF - gN) * f0, g1 = gN + (gF - gN) * f1;
  const a = L / R_E;
  const back = groundAt(up, fwd, -a, 1).normalize(), ahead = groundAt(up, fwd, a, 1).normalize();
  return [groundAt(back, left, g0, R_E + 3), groundAt(back, left, g1, R_E + 3), groundAt(ahead, left, g1, R_E + 3), groundAt(ahead, left, g0, R_E + 3)];
}

// Next time the city sits inside the left-looking 33-47° swath (closest approach on track).
function findNextPass(lat, lon, fromMs){
  const cityE = unitFromLatLon(lat, lon);
  let prev = null;
  for (let t = fromMs; t < fromMs + 12.5 * 86400000; t += 15000){
    const s = stateAt(t); if (!s) continue;
    const c = rotY(cityE, s.gmst);                 // city in inertial frame
    const fwd = s.v.clone().normalize(), up = s.r.clone().normalize();
    const along = c.dot(fwd);
    if (prev && prev.along > 0 && along <= 0 && c.dot(up) > 0.5){
      const tc = prev.t + (t - prev.t) * prev.along / (prev.along - along);
      const sc = stateAt(tc), cc = rotY(cityE, sc.gmst);
      const upc = sc.r.clone().normalize(), fwdc = sc.v.clone().normalize();
      const left = new THREE.Vector3().crossVectors(upc, fwdc).normalize();
      const gamma = Math.atan2(cc.dot(left), cc.dot(upc));
      const rs = sc.r.length();
      if (gamma >= centralAngle(INC_NEAR, rs) && gamma <= centralAngle(INC_FAR, rs)){
        const alpha = Math.atan2(R_E * Math.sin(gamma), rs - R_E * Math.cos(gamma));
        return {t: tc, inc: (alpha + gamma) / D2R, asc: sc.eci.z !== undefined ? sc.vel.z > 0 : true, leadMin: (tc - fromMs) / 60000, gamma};
      }
    }
    prev = {t, along};
  }
  return null;
}

// ---------- city overlay ----------
function placeCity(){
  cityGroup.clear(); cityDecal = null; cityMarker = null;
  if (!region) return;
  const u = unitFromLatLon(region.lat, region.lon);
  cityMarker = new THREE.Mesh(new THREE.RingGeometry(28, 40, 48), new THREE.MeshBasicMaterial({color: 0xfbbf24, transparent: true, opacity: 0.9, side: THREE.DoubleSide, depthWrite: false}));
  cityMarker.position.copy(u.clone().multiplyScalar(R_E + 6)); cityMarker.lookAt(u.clone().multiplyScalar(R_E * 2));
  cityGroup.add(cityMarker);
  labelCity.textContent = region.name;

  const bb = regionMeta?.bbox, last = regionMeta?.dates?.[regionMeta.dates.length - 1];
  if (bb && last){
    const [w, s, e, n] = bb, nx = 40, ny = 40, pos = [], uv = [], idx = [];
    for (let j = 0; j <= ny; j++) for (let i = 0; i <= nx; i++){
      const lo = w + (e - w) * i / nx, la = s + (n - s) * j / ny;
      const p = unitFromLatLon(la, lo).multiplyScalar(R_E + 2.5); pos.push(p.x, p.y, p.z); uv.push(i / nx, j / ny);
    }
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++){ const a = j * (nx + 1) + i; idx.push(a, a + 1, a + nx + 2, a, a + nx + 2, a + nx + 1); }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); g.setIndex(idx);
    const tex = new THREE.TextureLoader().load(ROOT + (region.path || `data/global/${region.id}/`) + `disp/${last}.png`);
    const mat = new THREE.ShaderMaterial({
      transparent: true, depthWrite: false, side: THREE.DoubleSide,
      uniforms: {map: {value: tex}, frac: {value: 0}, asc: {value: 1}, glow: {value: 0}},
      vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
      fragmentShader: `uniform sampler2D map; uniform float frac; uniform float asc; uniform float glow; varying vec2 vUv;
        void main(){
          float v = asc > 0.5 ? vUv.y : 1.0 - vUv.y;
          if (v > frac) discard;
          vec4 c = texture2D(map, vUv);
          float edge = smoothstep(0.035, 0.0, frac - v) * glow;
          gl_FragColor = vec4(mix(c.rgb, vec3(0.85, 0.95, 1.0), edge), max(c.a * 0.92, edge));
        }`
    });
    cityDecal = new THREE.Mesh(g, mat); cityGroup.add(cityDecal);
  }
}

function updateReveal(s){
  if (!cityDecal || !region || !regionMeta) return;
  const [w, so, e, n] = regionMeta.bbox;
  const q = swathQuad(s, 0, 0, 1);
  // swath centre-line point in Earth-fixed frame
  const mid = q[0].clone().add(q[1]).multiplyScalar(0.5);
  const fixed = rotY(mid, -s.gmst).normalize();
  const lat = Math.asin(fixed.y) / D2R, lon = Math.atan2(-fixed.z, fixed.x) / D2R;
  const asc = s.vel.z > 0;
  const lonOk = lon > w - 3 && lon < e + 3;
  const t = asc ? (lat - so) / (n - so) : (n - lat) / (n - so);
  const u = cityDecal.material.uniforms;
  if (!revealState) revealState = {frac: 0};
  if (mode === 'pass' && lonOk && t > -3 && t < 1 && !revealState.slowed){ revealState.slowed = true; setSpeed(1); setCam('city'); }
  if (lonOk && t > revealState.frac && t < 1.6){
    revealState.frac = Math.max(0, Math.min(1.001, t)); u.asc.value = asc ? 1 : 0;
  }
  u.frac.value = revealState.frac;
  u.glow.value = revealState.frac > 0 && revealState.frac < 1 ? 1 : 0;
  if (revealState.frac >= 1 && !revealState.done){
    revealState.done = true;
    setCaption(`Recorded. This is the ground motion our pipeline measured over ${esc(region.name)} from NISAR pairs taken on this same track, 12 days apart: comparing the phase of the radar echoes from each visit gives centimetre-scale motion. Red = moving away from the satellite (sinking). <span class="n3d-q">PROVISIONAL</span>`);
  }
}

// ---------- per-frame ----------
function loop(now){
  if (!running) return;
  requestAnimationFrame(loop);
  const dt = Math.min(0.1, (now - lastT) / 1000); lastT = now; frameDt = dt;
  simMs += dt * 1000 * speed;
  if (mode === 'live' && speed === 1 && Math.abs(simMs - Date.now()) > 2000) simMs = Date.now();
  const s = stateAt(simMs); if (!s) return;

  earth.rotation.y = s.gmst;
  const sun = sunEci(s.d);
  earthMat.uniforms.sunDir.value.copy(sun);
  sunLight.position.copy(sun.clone().multiplyScalar(50000));

  // spacecraft attitude: X along-track, Y left, Z zenith
  const up = s.r.clone().normalize(), fwd = s.v.clone().normalize();
  const left = new THREE.Vector3().crossVectors(up, fwd).normalize();
  const fwdOrtho = new THREE.Vector3().crossVectors(left, up).normalize();
  sat.position.copy(s.r);
  sat.quaternion.setFromRotationMatrix(new THREE.Matrix4().makeBasis(fwdOrtho, left, up));
  const camDist = camera.position.distanceTo(s.r);
  satGlow.position.copy(s.r); satGlow.scale.setScalar(Math.max(60, camDist * 0.035));
  satGlow.material.opacity = camMode === 'craft' ? 0 : camMode === 'follow' ? 0.25 : 0.9;

  // orbit line: one revolution centred on now (inertial frame)
  if (Math.abs(simMs - orbitStamp) > 20000){
    orbitStamp = simMs; const pts = [];
    for (let k = -52; k <= 52; k += 1){ const o = stateAt(simMs + k * 60000); if (o) pts.push(o.r); }
    orbitLine.geometry.dispose(); orbitLine.geometry = new THREE.BufferGeometry().setFromPoints(pts);
  }

  // SweepSAR beams
  const apex = sat.localToWorld(sat.userData.dishCenter.clone());
  sweepPhase = (sweepPhase + dt * 0.9) % 1;
  setFan(txFan, apex, swathQuad(s, 45, 0, 1));
  const f0 = sweepPhase * 0.88;
  setFan(rxFan, apex, swathQuad(s, 45, f0, f0 + 0.12));
  setQuad(foot, swathQuad(s, 45, 0, 1));

  // imaged strip (Earth-fixed), sampled every 4 s of simulated time
  if (Math.abs(simMs - lastStripMs) > 4000){
    lastStripMs = simMs;
    const q = swathQuad(s, 0, 0, 1);
    stripBuf.push([rotY(q[0], -s.gmst), rotY(q[1], -s.gmst)]);
    if (stripBuf.length > 900) stripBuf.shift();
    rebuildStrip();
  }

  updateReveal(s);
  updateCamera(s, up, fwdOrtho, left);
  controls.update();
  renderer.render(scene, camera);
  updateHud(s);
  if (camMode === 'craft') labelSat.style.opacity = '0'; else placeLabel(labelSat, s.r);
  const close = camMode === 'craft';
  txFan.material.opacity = close ? 0.035 : 0.10; rxFan.material.opacity = close ? 0.10 : 0.33;
  if (region) placeLabel(labelCity, rotY(unitFromLatLon(region.lat, region.lon).multiplyScalar(R_E + 10), s.gmst));
  if (cityMarker){ const k = 1 + 0.25 * Math.sin(now / 300); cityMarker.scale.setScalar(k); }

  if (mode === 'pass' && pass && simMs > pass.t + 150000){ mode = 'done'; setSpeed(1); }
}

function setFan(mesh, apex, q){
  const p = [apex, q[0], q[1], apex, q[1], q[2], apex, q[2], q[3], apex, q[3], q[0]];
  mesh.geometry.dispose(); mesh.geometry = new THREE.BufferGeometry().setFromPoints(p);
}
function setQuad(mesh, q){ mesh.geometry.dispose(); mesh.geometry = new THREE.BufferGeometry().setFromPoints([q[0], q[1], q[2], q[0], q[2], q[3]]); }

function rebuildStrip(){
  if (stripBuf.length < 2) return;
  const tri = [], edge = [];
  for (let i = 1; i < stripBuf.length; i++){
    const [a0, a1] = stripBuf[i - 1], [b0, b1] = stripBuf[i];
    if (a0.distanceTo(b0) > 400) continue;   // gap (time jump)
    tri.push(a0, a1, b1, a0, b1, b0); edge.push(a0, b0, a1, b1);
  }
  strip.geometry.dispose(); strip.geometry = new THREE.BufferGeometry().setFromPoints(tri);
  stripEdge.geometry.dispose(); stripEdge.geometry = new THREE.BufferGeometry().setFromPoints(edge);
}

const camTmp = new THREE.Vector3();
function updateCamera(s, up, fwd, left){
  if (camMode === 'craft'){
    const mid = sat.localToWorld(new THREE.Vector3(0.5, -1.0, 4.5));
    if (snapCraft || !lastSatPos){
      camera.up.copy(up);
      camera.position.copy(mid).addScaledVector(fwd, 92).addScaledVector(left, -52).addScaledVector(up, -22);
      controls.target.copy(mid); snapCraft = false;
    } else {
      const d = s.r.clone().sub(lastSatPos); camera.position.add(d); controls.target.add(d);
    }
    lastSatPos = s.r.clone();
    return;
  }
  lastSatPos = null;
  if (camMode === 'city' && region){
    const cu = rotY(unitFromLatLon(region.lat, region.lon), s.gmst);
    const cityW = cu.clone().multiplyScalar(R_E);
    const side = s.r.clone().normalize().sub(cu).normalize();     // lean toward the spacecraft so the beam stays in frame
    const done = revealState && revealState.done;
    const bb = regionMeta?.bbox, spanKm = bb ? Math.max(bb[2] - bb[0], bb[3] - bb[1]) * 111 : 60;
    camTmp.copy(cu).multiplyScalar(R_E + (done ? Math.max(60, spanKm * 1.9) : 1700)).addScaledVector(side, done ? spanKm * 0.35 : 900);
    if (cityMarker) cityMarker.visible = !done;
    const k = 1 - Math.exp(-frameDt * (done ? 1.1 : 1.6));
    camera.up.set(0, 1, 0);
    camera.position.lerp(camTmp, k); controls.target.lerp(cityW, k);
    return;
  }
  if (camMode !== 'follow') return;
  const q = swathQuad(s, 0, 0, 1), target = q[0].clone().add(q[1]).multiplyScalar(0.5).lerp(s.r, 0.78);
  camTmp.copy(s.r).addScaledVector(fwd, -300).addScaledVector(up, 120).addScaledVector(left, -190);
  if (snapFollow){   // start high above the spacecraft and swoop in, never through the Earth
    camera.position.copy(camTmp).addScaledVector(up, 2600).addScaledVector(fwd, -1800);
    controls.target.copy(target); snapFollow = false;
  }
  camera.up.copy(up);
  const k = 1 - Math.exp(-frameDt * 2.2);
  camera.position.lerp(camTmp, k);
  controls.target.lerp(target, Math.min(1, k * 1.6));
}

function updateHud(s){
  const g = SAT.eciToGeodetic(s.eci, s.gmst);
  const lat = SAT.degreesLat(g.latitude), lon = SAT.degreesLong(g.longitude);
  const vel = Math.hypot(s.vel.x, s.vel.y, s.vel.z);
  hud.time.textContent = fmtUTC(s.d) + (speed > 1 ? `  ·  ${speed}×` : '');
  hud.pos.textContent = `${Math.abs(lat).toFixed(2)}°${lat >= 0 ? 'N' : 'S'}  ${Math.abs(lon).toFixed(2)}°${lon >= 0 ? 'E' : 'W'}`;
  hud.alt.textContent = `${g.height.toFixed(0)} km`;
  hud.vel.textContent = `${vel.toFixed(2)} km/s`;
  hud.dir.textContent = s.vel.z > 0 ? 'ascending (northbound)' : 'descending (southbound)';
}

function placeLabel(el, world){
  const p = world.clone().project(camera);
  const behind = world.clone().normalize().dot(camera.position.clone().normalize()) < 0.1 && world.length() < R_E + 50;
  if (p.z > 1 || behind){ el.style.opacity = '0'; return; }
  const w = root.clientWidth, h = root.clientHeight;
  el.style.opacity = '1';
  el.style.transform = `translate(${(p.x + 1) / 2 * w}px, ${(1 - p.y) / 2 * h}px)`;
}

// ---------- UI ----------
function onBar(e){
  const b = e.target.closest('button'); if (!b) return;
  if (b.dataset.speed){ setSpeed(+b.dataset.speed); if (mode === 'live' && +b.dataset.speed > 1) mode = 'free'; }
  if (b.dataset.cam){ setCam(b.dataset.cam); }
  const a = b.dataset.act;
  if (a === 'live'){ mode = 'live'; simMs = Date.now(); setSpeed(1); stripBuf = []; rebuildStrip(); mark('[data-act]', b); }
  if (a === 'pass') playPass(b);
  if (a === 'fs'){ if (document.fullscreenElement) document.exitFullscreen(); else root.requestFullscreen?.(); }
  if (a === 'close') close();
}
function playPass(btn){
  if (!pass && region) pass = findNextPass(region.lat, region.lon, Date.now());
  if (!pass) return;
  mode = 'pass'; simMs = pass.t - 240000; stripBuf = []; rebuildStrip(); revealState = null;
  if (cityDecal) cityDecal.material.uniforms.frac.value = 0;
  setSpeed(12); setCam('follow'); mark('[data-act]', btn);
  setCaption(`Replaying the real orbit: ${fmtUTC(new Date(pass.t))}, ${pass.asc ? 'ascending' : 'descending'} pass, ${region.name} at ${pass.inc.toFixed(1)}° incidence. The pale fan is the transmitted pulse lighting the whole 242 km swath; the bright band is the SweepSAR receive beam scanning from near to far range. NISAR flies a dawn–dusk orbit and its radar images through darkness and cloud.`);
}
function setSpeed(x){ speed = x; root.querySelectorAll('[data-speed]').forEach(b => b.classList.toggle('is-on', +b.dataset.speed === x)); }
function setCam(c){
  camMode = c; root.querySelectorAll('[data-cam]').forEach(b => b.classList.toggle('is-on', b.dataset.cam === c));
  controls.minDistance = c === 'orbit' ? 6700 : 8;
  if (c === 'craft') snapCraft = true;
  if (c === 'follow') snapFollow = true;
  controls.enableRotate = c === 'orbit' || c === 'craft';
  if (c === 'orbit'){ camera.up.set(0, 1, 0); controls.target.set(0, 0, 0); if (camera.position.length() < 12000) camera.position.setLength(21000); }
}
function mark(sel, btn){ root.querySelectorAll(sel).forEach(b => b.classList.toggle('is-on', b === btn)); }
function setCaption(html){ hud.cap.innerHTML = html; hud.cap.hidden = !html; }
function esc(s){ return String(s ?? '').replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c])); }
function resize(){
  if (!renderer || !root) return;
  const w = root.clientWidth || 800, h = root.clientHeight || 500;
  renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
}
