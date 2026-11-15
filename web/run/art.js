/* AQUIFER RUN — art module v2 (PC1). Modern illustrated style, everything drawn in code
 * (no external images except our own NISAR maps from this repository).
 * Contract: web/run/DESIGN.md §10 + §14 (window.RunArt). Tiles 48×48, Nisa ~48×84.
 */
(function (root) {
  'use strict';
  const T = 16, SC = 3, TS = T * SC;        // logical tile 16, drawn at 48 px
  const SS = 2;                              // supersampling factor for crisp anti-aliasing

  // ---------- palette ----------
  const P = {
    ink: '#1c2233', ink2: '#2e3650', white: '#ffffff', cream: '#fff7e8', shadow: 'rgba(20,24,40,.28)',
    skin: '#f5c7a1', skinS: '#dc9c72', hair: '#3a2417', cheek: '#f29a8a',
    hat: '#f2b447', hatS: '#c98a22', band: '#d9534f', shirt: '#3d93e0', shirtS: '#2a6cb0', pants: '#2f3d5c', boot: '#6b3f22',
    tank: '#56c8f5', tankS: '#2a8fca', gauge: '#ffe066',
    grass: '#62c254', grassL: '#9be06d', grassD: '#3e9440',
    soil: '#9a6b40', soilL: '#b9844f', soilD: '#6c4426', pebble: '#c9a27a',
    clay: '#d7ad74', clayL: '#ead0a0', clayD: '#b98a52',
    rock: '#8a93a6', rockL: '#b3bacb', rockD: '#5e6679',
    sand: '#ecc985', sandL: '#f8e2b4', sandD: '#cfa45f',
    asphalt: '#4e5366', asphaltL: '#666c82', line: '#f5d35a',
    brick: '#c0613f', brickL: '#dc7f5a', brickD: '#8f4229', mortar: '#e2cfb2',
    water: '#2f8fe6', waterL: '#7cc8ff', waterD: '#1b5fae', foam: '#e3f5ff',
    concrete: '#b5b1a7', concreteD: '#8b877e',
    metal: '#97a3b6', metalD: '#647086', metalL: '#d3dbe6', rust: '#b5651d',
    wood: '#b07a45', woodD: '#7d522c', woodL: '#d39b60',
    leaf: '#46a84f', leafL: '#7fd168', leafD: '#2c7437', trunk: '#73492b',
    wheat: '#f0c95c', wheatD: '#c99c34', cotton: '#fbf8f1',
    red: '#e8483c', redD: '#ad2e25', orange: '#f59230', yellow: '#ffd23f', green: '#3fc06c', gold: '#e8b33a',
    roof: '#cf5b3d', roofD: '#9c3d22', wall: '#f2e4ca', wallD: '#d4bf9a', glass: '#9ad7ff',
    dust: '#dcbc80', dustD: '#b8975c', sat: '#e8b33a', panel: '#2f6fd6', panelL: '#5d98ff',
  };

  // ---------- helpers ----------
  function mk(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d'); g.imageSmoothingEnabled = true; g.lineJoin = 'round'; g.lineCap = 'round'; return [c, g]; }
  function rnd(seed) { let s = (seed >>> 0) || 1; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }
  function rr(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
  function lin(g, x0, y0, x1, y1, stops) { const gr = g.createLinearGradient(x0, y0, x1, y1); stops.forEach((c, i) => gr.addColorStop(i / (stops.length - 1), c)); return gr; }
  function rad(g, x, y, r0, r1, stops) { const gr = g.createRadialGradient(x, y, r0, x, y, r1); stops.forEach((c, i) => gr.addColorStop(i / (stops.length - 1), c)); return gr; }
  function circle(g, x, y, r, fill, stroke, lw) { g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); if (fill) { g.fillStyle = fill; g.fill(); } if (stroke) { g.strokeStyle = stroke; g.lineWidth = lw || 2; g.stroke(); } }
  function ell(g, x, y, rx, ry, fill) { g.beginPath(); g.ellipse(x, y, rx, ry, 0, 0, Math.PI * 2); g.fillStyle = fill; g.fill(); }
  function down(src, w, h) { const [c, g] = mk(w, h); g.imageSmoothingQuality = 'high'; g.drawImage(src, 0, 0, w, h); return c; }
  // Render a tile function at 2x then downscale to 48 px.
  function tileCanvas(fn) { const S = TS * SS; const [c, g] = mk(S, S); fn(g, S); return down(c, TS, TS); }
  // Seamless periodic noise for backgrounds.
  function periodic(seed, W, terms) { const r = rnd(seed); const ks = []; for (let i = 0; i < terms; i++) ks.push({ k: 1 + Math.floor(r() * (2 + i * 2)), a: (1 / (i + 1)) * (0.6 + r() * 0.6), p: r() * Math.PI * 2 }); return (x) => ks.reduce((s, t) => s + t.a * Math.sin((x / W) * Math.PI * 2 * t.k + t.p), 0); }

  // ---------- tiles (drawn in an S×S space, S = 96) ----------
  function soilBase(g, S, top = 0, seed = 3) {
    g.fillStyle = lin(g, 0, top, 0, S, [P.soilL, P.soil, P.soilD]); g.fillRect(0, top, S, S - top);
    const r = rnd(seed); for (let i = 0; i < 9; i++) { const x = r() * S, y = top + 8 + r() * (S - top - 12), rx = 3 + r() * 5; ell(g, x, y + 1.5, rx, rx * 0.6, 'rgba(0,0,0,.18)'); ell(g, x, y, rx, rx * 0.6, r() < 0.5 ? P.pebble : P.soilL); }
  }
  function grassCap(g, S, h = 0.3) {
    const H = S * h;
    g.fillStyle = lin(g, 0, 0, 0, H + 8, [P.grassL, P.grass, P.grassD]);
    g.beginPath(); g.moveTo(0, 0); g.lineTo(S, 0); g.lineTo(S, H);
    for (let x = S; x >= 0; x -= S / 8) g.quadraticCurveTo(x - S / 16, H + 9, x - S / 8, H);
    g.closePath(); g.fill();
    g.fillStyle = P.grassL; for (let x = 4; x < S; x += 11) { g.beginPath(); g.moveTo(x, 6); g.lineTo(x + 3, -1); g.lineTo(x + 6, 6); g.fill(); }
    g.fillStyle = 'rgba(255,255,255,.35)'; g.fillRect(0, 0, S, 3);
  }
  function crack(g, pts, w) { g.strokeStyle = 'rgba(255,255,255,.35)'; g.lineWidth = w + 2; g.beginPath(); pts.forEach(([x, y], i) => (i ? g.lineTo(x + 1.5, y + 1) : g.moveTo(x + 1.5, y + 1))); g.stroke();
    g.strokeStyle = P.ink; g.lineWidth = w; g.beginPath(); pts.forEach(([x, y], i) => (i ? g.lineTo(x, y) : g.moveTo(x, y))); g.stroke(); }
  function treeShape(g, S, cx, base, rFol, fruit) {
    g.fillStyle = lin(g, 0, base - S * 0.35, 0, base, [P.trunk, '#5a3820']); rr(g, cx - S * 0.06, base - S * 0.42, S * 0.12, S * 0.42, 4); g.fill();
    const blobs = [[0, -0.62, 1], [-0.42, -0.48, 0.75], [0.42, -0.48, 0.75], [0, -0.38, 0.85]];
    for (const [dx, dy, k] of blobs) circle(g, cx + dx * rFol, base + dy * S * 0.9 + 2, rFol * 0.62 * k, P.leafD);
    for (const [dx, dy, k] of blobs) circle(g, cx + dx * rFol, base + dy * S * 0.9, rFol * 0.58 * k, rad(g, cx + dx * rFol - 6, base + dy * S * 0.9 - 8, 2, rFol * 0.6, [P.leafL, P.leaf, P.leafD]));
    if (fruit) { const r = rnd(9); for (let i = 0; i < 6; i++) circle(g, cx + (r() - 0.5) * rFol * 1.4, base - S * 0.55 + (r() - 0.5) * rFol, 4.5, P.orange, '#b8641a', 1.5); }
  }
  const TILE_FN = {
    grass(g, S) { soilBase(g, S, 0, 3); grassCap(g, S); },
    dirt(g, S) { soilBase(g, S, 0, 7); g.strokeStyle = 'rgba(60,35,18,.35)'; g.lineWidth = 2; g.beginPath(); g.moveTo(20, 10); g.quadraticCurveTo(30, 40, 22, 70); g.stroke(); },
    clay(g, S) { g.fillStyle = lin(g, 0, 0, 0, S, [P.clayL, P.clay, P.clayD]); g.fillRect(0, 0, S, S);
      for (let i = 0; i < 4; i++) { const y = 14 + i * 22; g.strokeStyle = 'rgba(140,95,50,.45)'; g.lineWidth = 4; g.beginPath(); g.moveTo(0, y); g.bezierCurveTo(S * 0.3, y - 5, S * 0.7, y + 5, S, y); g.stroke(); } },
    rock(g, S) { g.fillStyle = lin(g, 0, 0, 0, S, [P.rockD, '#4c5366']); g.fillRect(0, 0, S, S);
      [[24, 26, 22], [68, 30, 20], [46, 68, 24], [12, 76, 14], [86, 74, 13]].forEach(([x, y, r]) => { ell(g, x, y + 3, r, r * 0.8, 'rgba(0,0,0,.3)'); ell(g, x, y, r, r * 0.8, rad(g, x - r * 0.3, y - r * 0.4, 1, r, [P.rockL, P.rock, P.rockD])); }); },
    sand(g, S) { g.fillStyle = lin(g, 0, 0, 0, S, [P.sandL, P.sand, P.sandD]); g.fillRect(0, 0, S, S);
      g.strokeStyle = 'rgba(180,130,60,.35)'; g.lineWidth = 3; for (let i = 0; i < 3; i++) { const y = 26 + i * 26; g.beginPath(); g.moveTo(0, y); g.quadraticCurveTo(S / 2, y - 10, S, y); g.stroke(); } },
    road(g, S) { g.fillStyle = lin(g, 0, 0, 0, S, [P.asphaltL, P.asphalt]); g.fillRect(0, 0, S, S); g.fillStyle = '#c9c4b8'; g.fillRect(0, 0, S, 8); g.fillStyle = P.line; rr(g, 12, 44, 30, 7, 3); g.fill(); rr(g, 60, 44, 30, 7, 3); g.fill(); },
    brick(g, S) { g.fillStyle = P.mortar; g.fillRect(0, 0, S, S); for (let row = 0; row < 4; row++) { const off = row % 2 ? 24 : 0; for (let x = -off; x < S; x += 48) { const y = row * 24 + 3; rr(g, x + 3, y, 42, 18, 4); g.fillStyle = lin(g, 0, y, 0, y + 18, [P.brickL, P.brick, P.brickD]); g.fill(); } } },
    canal(g, S) { g.fillStyle = lin(g, 0, 0, 0, S, [P.concrete, P.concreteD]); g.fillRect(0, 0, S, S); rr(g, 8, 10, S - 16, S - 10, 8); g.fillStyle = lin(g, 0, 10, 0, S, [P.waterL, P.water, P.waterD]); g.fill(); g.strokeStyle = 'rgba(255,255,255,.6)'; g.lineWidth = 3; g.beginPath(); g.moveTo(16, 22); g.quadraticCurveTo(40, 16, 64, 22); g.stroke(); },
    water(g, S) { g.fillStyle = lin(g, 0, 0, 0, S, [P.waterL, P.water, P.waterD]); g.fillRect(0, 0, S, S); g.strokeStyle = 'rgba(255,255,255,.65)'; g.lineWidth = 3;
      for (let i = 0; i < 3; i++) { const y = 14 + i * 26; g.beginPath(); for (let x = 0; x <= S; x += 8) g.lineTo(x, y + Math.sin(x / 10 + i) * 3); g.stroke(); } },
    pipe_v(g, S) { g.fillStyle = lin(g, 22, 0, 74, 0, [P.metalD, P.metalL, P.metal, P.metalD]); g.fillRect(24, 0, 48, S); g.fillStyle = lin(g, 16, 0, 80, 0, [P.metalD, P.metalL, P.metalD]); rr(g, 16, 30, 64, 14, 5); g.fill(); circle(g, 26, 37, 3, P.ink2); circle(g, 70, 37, 3, P.ink2); },
    pipe_h(g, S) { g.fillStyle = lin(g, 0, 22, 0, 74, [P.metalD, P.metalL, P.metal, P.metalD]); g.fillRect(0, 24, S, 48); g.fillStyle = lin(g, 0, 16, 0, 80, [P.metalD, P.metalL, P.metalD]); rr(g, 34, 16, 14, 64, 5); g.fill(); },
    crate(g, S) { rr(g, 2, 2, S - 4, S - 4, 8); g.fillStyle = lin(g, 0, 0, 0, S, [P.woodL, P.wood, P.woodD]); g.fill(); g.strokeStyle = P.woodD; g.lineWidth = 5; g.stroke();
      g.lineWidth = 7; g.beginPath(); g.moveTo(12, 12); g.lineTo(S - 12, S - 12); g.moveTo(S - 12, 12); g.lineTo(12, S - 12); g.stroke(); [[12, 12], [S - 12, 12], [12, S - 12], [S - 12, S - 12]].forEach(([x, y]) => circle(g, x, y, 4, P.metal, P.metalD, 2)); },
    sign(g, S) { g.fillStyle = P.woodD; rr(g, 44, 46, 8, 50, 3); g.fill(); rr(g, 8, 10, S - 16, 42, 9); g.fillStyle = lin(g, 0, 10, 0, 52, [P.woodL, P.wood]); g.fill(); g.strokeStyle = P.woodD; g.lineWidth = 4; g.stroke();
      g.fillStyle = P.cream; g.beginPath(); g.moveTo(30, 26); g.lineTo(58, 26); g.lineTo(58, 18); g.lineTo(72, 31); g.lineTo(58, 44); g.lineTo(58, 36); g.lineTo(30, 36); g.closePath(); g.fill(); },
    sink1(g, S) { TILE_FN.grass(g, S); crack(g, [[30, 4], [38, 22], [34, 34]], 3); },
    sink2(g, S) { TILE_FN.grass(g, S); crack(g, [[22, 2], [34, 20], [28, 36], [40, 58]], 4); crack(g, [[64, 4], [58, 24], [70, 40]], 3); },
    sink3(g, S) { TILE_FN.grass(g, S); g.fillStyle = 'rgba(0,0,0,.18)'; g.fillRect(0, 0, S, S); crack(g, [[18, 0], [32, 22], [24, 44], [40, 70], [34, 92]], 6); crack(g, [[70, 0], [60, 26], [76, 48], [66, 80]], 5); crack(g, [[32, 22], [56, 34]], 3); },
    fissure(g, S) { TILE_FN.sand(g, S); g.fillStyle = lin(g, 0, 0, 0, S, ['#3a2a1c', P.ink]); g.beginPath(); g.moveTo(34, 0); g.lineTo(62, 0); g.lineTo(56, 30); g.lineTo(60, 60); g.lineTo(52, S); g.lineTo(42, S); g.lineTo(38, 62); g.lineTo(42, 30); g.closePath(); g.fill(); },
    sinkhole_edge(g, S) { g.fillStyle = rad(g, S / 2, S * 0.9, 4, S, ['#05060a', P.ink, '#3b2618']); g.fillRect(0, 0, S, S); g.fillStyle = P.soilD; g.beginPath(); g.moveTo(0, 0); g.lineTo(S, 0); g.lineTo(S, 14); for (let x = S; x >= 0; x -= 12) g.lineTo(x - 6, 14 + (x % 24 ? 8 : 2)); g.lineTo(0, 14); g.fill(); },
    bridge(g, S) { for (let x = 0; x < S; x += 24) { rr(g, x + 1, 10, 22, 22, 4); g.fillStyle = lin(g, 0, 10, 0, 32, [P.woodL, P.wood, P.woodD]); g.fill(); } g.strokeStyle = '#d7c49a'; g.lineWidth = 3; g.beginPath(); g.moveTo(0, 6); g.quadraticCurveTo(S / 2, 16, S, 6); g.stroke(); },
    bridge_broken(g, S) { for (let x = 0; x < 40; x += 24) { rr(g, x + 1, 10, 22, 22, 4); g.fillStyle = lin(g, 0, 10, 0, 32, [P.woodL, P.wood, P.woodD]); g.fill(); } g.save(); g.translate(72, 30); g.rotate(0.5); rr(g, -10, -10, 22, 22, 4); g.fillStyle = P.wood; g.fill(); g.restore(); },
    house_wall(g, S) { g.fillStyle = lin(g, 0, 0, 0, S, [P.wall, P.wallD]); g.fillRect(0, 0, S, S); rr(g, 24, 22, 48, 44, 5); g.fillStyle = P.woodD; g.fill(); rr(g, 29, 27, 38, 34, 3); g.fillStyle = lin(g, 29, 27, 67, 61, [P.white, P.glass, '#5fb2ea']); g.fill(); g.fillStyle = P.woodD; g.fillRect(46, 27, 4, 34); g.fillRect(29, 42, 38, 4); },
    house_roof(g, S) { g.fillStyle = lin(g, 0, 0, 0, S, [P.roof, P.roofD]); g.fillRect(0, 0, S, S); for (let y = 8; y < S; y += 18) for (let x = (y / 18 % 2) * 12 - 12; x < S; x += 24) { g.beginPath(); g.arc(x + 12, y, 12, 0, Math.PI); g.fillStyle = 'rgba(0,0,0,.15)'; g.fill(); } },
    tree(g, S) { treeShape(g, S, S / 2, S, S * 0.42, false); },
    bush(g, S) { [[30, 72, 22], [62, 70, 24], [46, 60, 22]].forEach(([x, y, r]) => circle(g, x, y + 3, r, P.leafD)); [[30, 72, 21], [62, 70, 23], [46, 60, 21]].forEach(([x, y, r]) => circle(g, x, y, r, rad(g, x - 6, y - 8, 2, r, [P.leafL, P.leaf, P.leafD]))); },
    wheat(g, S) { for (let x = 10; x < S; x += 15) { g.strokeStyle = P.wheatD; g.lineWidth = 3; g.beginPath(); g.moveTo(x, S); g.quadraticCurveTo(x + 4, S * 0.6, x + 2, S * 0.35); g.stroke(); for (let k = 0; k < 4; k++) { ell(g, x + 2 - 4, S * 0.35 - k * 7, 4, 6, P.wheat); ell(g, x + 2 + 4, S * 0.35 - k * 7 + 3, 4, 6, P.wheat); } } },
    cotton(g, S) { for (let x = 14; x < S; x += 26) { g.strokeStyle = P.leafD; g.lineWidth = 4; g.beginPath(); g.moveTo(x, S); g.lineTo(x, S * 0.45); g.stroke(); circle(g, x - 7, S * 0.5, 9, P.cotton, '#d9d2c2', 2); circle(g, x + 7, S * 0.42, 10, P.cotton, '#d9d2c2', 2); circle(g, x, S * 0.3, 9, P.cotton, '#d9d2c2', 2); } },
    orchard(g, S) { treeShape(g, S, S / 2, S, S * 0.4, true); },
    fence(g, S) { g.fillStyle = lin(g, 0, 0, 0, 12, [P.woodL, P.wood]); rr(g, 0, 34, S, 12, 4); g.fill(); rr(g, 0, 60, S, 12, 4); g.fill(); [16, 70].forEach((x) => { rr(g, x, 22, 12, S - 22, 4); g.fillStyle = lin(g, x, 0, x + 12, 0, [P.woodL, P.woodD]); g.fill(); }); },
    lamp(g, S) { g.fillStyle = rad(g, S / 2, 20, 2, 46, ['rgba(255,220,120,.7)', 'rgba(255,220,120,0)']); g.fillRect(0, 0, S, S); g.fillStyle = P.ink2; rr(g, 44, 24, 8, S - 24, 3); g.fill(); rr(g, 30, 10, 36, 16, 6); g.fill(); rr(g, 34, 22, 28, 8, 3); g.fillStyle = P.yellow; g.fill(); },
  };
  const TILE_NAMES = Object.keys(TILE_FN);

  // ---------- characters & objects (drawn at 2x in their own space, then downscaled) ----------
  function stroke(g, w = 3) { g.strokeStyle = P.ink; g.lineWidth = w; g.stroke(); }
  function limb(g, x, y, len, ang, w, col, footCol) {
    const ex = x + Math.sin(ang) * len, ey = y + Math.cos(ang) * len;
    g.strokeStyle = P.ink; g.lineWidth = w + 5; g.beginPath(); g.moveTo(x, y); g.lineTo(ex, ey); g.stroke();
    g.strokeStyle = col; g.lineWidth = w; g.beginPath(); g.moveTo(x, y); g.lineTo(ex, ey); g.stroke();
    if (footCol) { g.save(); g.translate(ex, ey); rr(g, -8, -4, 22, 11, 5); g.fillStyle = footCol; g.fill(); stroke(g, 2.5); g.restore(); }
    return [ex, ey];
  }
  // Nisa — 96×168 drawing space (final 48×84). pose: idle|run|jump|action, f = frame
  function nisa(g, pose, f, colors) {
    const C = Object.assign({ shirt: P.shirt, shirtS: P.shirtS, hat: P.hat, hatS: P.hatS, tank: true, pants: P.pants }, colors || {});
    let bob = 0, legA = 0.08, legB = -0.08, armF = 0.2, armB = -0.2;
    if (pose === 'idle') { bob = f ? 2 : 0; }
    if (pose === 'run') { const ph = (f / 6) * Math.PI * 2; legA = Math.sin(ph) * 0.75; legB = -legA; armF = -Math.sin(ph) * 0.8; armB = -armF; bob = Math.abs(Math.cos(ph)) * 5; }
    if (pose === 'jump') { legA = -0.7; legB = 0.5; armF = -2.4; armB = 2.6; bob = -2; }
    if (pose === 'action') { armF = -1.45; legA = 0.25; legB = -0.2; }
    const cx = 48, hipY = 112 - bob, shY = 78 - bob;
    ell(g, cx, 162, 26, 6, 'rgba(0,0,0,.22)');
    // back limbs
    limb(g, cx - 4, hipY, 40, legB, 12, '#24304a', P.boot);
    limb(g, cx - 12, shY + 4, 30, armB, 9, C.shirtS);
    // water tank
    if (C.tank) { rr(g, cx - 34, shY - 6, 22, 44, 10); g.fillStyle = lin(g, cx - 34, 0, cx - 12, 0, [P.tankS, P.tank, '#b9ecff']); g.fill(); stroke(g); rr(g, cx - 30, shY + 4, 8, 14, 3); g.fillStyle = P.gauge; g.fill(); }
    // torso
    rr(g, cx - 18, shY - 6, 38, 46, 14); g.fillStyle = lin(g, 0, shY - 6, 0, shY + 40, [C.shirt, C.shirt, C.shirtS]); g.fill(); stroke(g);
    g.fillStyle = C.pants; rr(g, cx - 18, hipY - 8, 38, 14, 6); g.fill(); stroke(g, 2.5);
    g.strokeStyle = P.tankS; g.lineWidth = 5; g.beginPath(); g.moveTo(cx - 10, shY - 4); g.lineTo(cx + 2, hipY - 8); g.stroke();
    // front leg
    limb(g, cx + 6, hipY, 40, legA, 12, C.pants, P.boot);
    // head
    circle(g, cx + 2, shY - 26, 23, lin(g, 0, shY - 50, 0, shY, [P.skin, P.skinS]));
    stroke(g);
    g.fillStyle = P.hair; g.beginPath(); g.ellipse(cx - 14, shY - 22, 10, 16, 0.3, 0, Math.PI * 2); g.fill();
    circle(g, cx + 12, shY - 28, 3.2, P.ink); circle(g, cx + 13, shY - 29, 1.1, P.white);
    circle(g, cx + 16, shY - 18, 4, 'rgba(242,154,138,.6)');
    g.strokeStyle = P.ink; g.lineWidth = 2.5; g.beginPath(); g.arc(cx + 10, shY - 18, 6, 0.2, Math.PI - 0.6); g.stroke();
    // hat
    ell(g, cx + 2, shY - 42, 36, 9, P.hatS); g.beginPath(); g.ellipse(cx + 2, shY - 42, 36, 9, 0, 0, Math.PI * 2); stroke(g);
    rr(g, cx - 16, shY - 66, 36, 26, 12); g.fillStyle = lin(g, 0, shY - 66, 0, shY - 40, [C.hat, C.hatS]); g.fill(); stroke(g);
    g.fillStyle = P.band; g.fillRect(cx - 16, shY - 48, 36, 6);
    // front arm (+ hose in action)
    const [hx, hy] = limb(g, cx + 12, shY + 2, 30, armF, 9, C.shirt);
    circle(g, hx, hy, 6, P.skin, P.ink, 2.5);
    if (pose === 'action') { rr(g, hx - 2, hy - 5, 20, 8, 3); g.fillStyle = P.metal; g.fill(); stroke(g, 2);
      if (f === 1) { g.fillStyle = P.waterL; for (let i = 0; i < 5; i++) circle(g, hx + 26 + i * 9, hy - 2 + i * i * 0.9, 4 - i * 0.4, P.waterL, P.water, 1.5); } }
  }
  function farmer(g, f) {
    nisa(g, f ? 'idle' : 'idle', f, { shirt: '#6aa84f', shirtS: '#4a7d35', hat: '#f0d58a', hatS: '#c9a94f', tank: false, pants: '#3d5a8a' });
    g.fillStyle = '#efefef'; g.beginPath(); g.ellipse(58, 62, 10, 7, 0, 0, Math.PI); g.fill();   // moustache
    if (f) { g.strokeStyle = P.ink; g.lineWidth = 3; g.beginPath(); g.moveTo(66, 70); g.lineTo(84, 40); g.stroke(); circle(g, 85, 37, 6, P.skin, P.ink, 2); }
  }
  function pumpjack(g, on, f) { // 96×96
    ell(g, 48, 90, 40, 5, 'rgba(0,0,0,.25)');
    rr(g, 6, 76, 84, 14, 4); g.fillStyle = lin(g, 0, 76, 0, 90, [P.concrete, P.concreteD]); g.fill(); stroke(g, 2.5);
    g.strokeStyle = P.ink; g.lineWidth = 7; g.beginPath(); g.moveTo(34, 78); g.lineTo(48, 36); g.lineTo(62, 78); g.stroke();
    g.strokeStyle = on ? P.red : P.metal; g.lineWidth = 4; g.beginPath(); g.moveTo(34, 78); g.lineTo(48, 36); g.lineTo(62, 78); g.stroke();
    const a = on ? (f ? -0.28 : 0.18) : 0;
    g.save(); g.translate(48, 36); g.rotate(a);
    rr(g, -44, -7, 76, 14, 6); g.fillStyle = lin(g, 0, -7, 0, 7, [on ? '#ff7a6c' : P.metalL, on ? P.red : P.metal]); g.fill(); stroke(g, 2.5);
    g.beginPath(); g.moveTo(-44, -7); g.quadraticCurveTo(-60, 0, -44, 22); g.lineTo(-38, 7); g.closePath(); g.fillStyle = on ? P.redD : P.metalD; g.fill(); stroke(g, 2.5);
    g.restore(); circle(g, 48, 36, 6, P.ink2);
    g.strokeStyle = P.ink2; g.lineWidth = 3; g.beginPath(); g.moveTo(8, 50 + (on ? (f ? -10 : 8) : 0)); g.lineTo(8, 78); g.stroke();
    rr(g, 66, 58, 22, 18, 4); g.fillStyle = P.metalD; g.fill(); stroke(g, 2);
    if (on) { circle(g, 77, 52 - f * 4, 5 + f * 2, 'rgba(120,120,130,.5)'); }
    else { circle(g, 78, 24, 14, P.green, P.ink, 3); g.strokeStyle = P.white; g.lineWidth = 4; g.beginPath(); g.moveTo(71, 24); g.lineTo(76, 30); g.lineTo(86, 18); g.stroke(); }
  }
  function cropSprite(g, green) {
    for (let i = 0; i < 4; i++) { const x = 14 + i * 22, droop = green ? 0 : 10;
      g.strokeStyle = green ? P.leafD : '#9a7f45'; g.lineWidth = 5; g.beginPath(); g.moveTo(x, 94); g.quadraticCurveTo(x + droop, 66, x + droop * 1.8, 50 + droop); g.stroke();
      ell(g, x - 8, 72, 9, 4, green ? P.leaf : '#b49a5c'); ell(g, x + 8, 64, 9, 4, green ? P.leafL : '#c7ad6c');
      if (green) { for (let k = 0; k < 3; k++) ell(g, x + (k % 2 ? 4 : -4), 44 - k * 8, 5, 8, P.wheat); } }
    if (!green) { rr(g, 30, 4, 36, 30, 12); g.fillStyle = P.white; g.fill(); stroke(g, 3); g.beginPath(); g.moveTo(44, 34); g.lineTo(48, 42); g.lineTo(52, 34); g.fillStyle = P.white; g.fill();
      g.fillStyle = P.water; g.beginPath(); g.moveTo(48, 10); g.quadraticCurveTo(58, 22, 48, 28); g.quadraticCurveTo(38, 22, 48, 10); g.fill(); }
  }
  function dropSprite(g, f) { const y = [0, -3, 0, 3][f % 4];
    g.beginPath(); g.moveTo(48, 14 + y); g.bezierCurveTo(74, 46 + y, 70, 78 + y, 48, 80 + y); g.bezierCurveTo(26, 78 + y, 22, 46 + y, 48, 14 + y);
    g.fillStyle = lin(g, 30, 20, 70, 80, ['#bfe8ff', P.water, P.waterD]); g.fill(); stroke(g, 3);
    ell(g, 40, 52 + y, 6, 11, 'rgba(255,255,255,.8)'); if (f % 2) { circle(g, 70, 24 + y, 3, P.white); } }
  function chipSprite(g, f) { // mini NISAR satellite (gold body, blue panels, reflector)
    const w = [1, 0.7, 0.25, 0.7][f % 4];
    circle(g, 48, 48, 40, 'rgba(255,214,90,.18)');
    g.save(); g.translate(48, 48);
    for (const s of [-1, 1]) { rr(g, s > 0 ? 14 : -14 - 30 * w, -9, 30 * w, 18, 3); g.fillStyle = lin(g, 0, -9, 0, 9, [P.panelL, P.panel]); g.fill(); stroke(g, 2.5); }
    rr(g, -14, -14, 28, 28, 6); g.fillStyle = lin(g, 0, -14, 0, 14, ['#ffe08a', P.sat, '#b98516']); g.fill(); stroke(g, 2.5);
    g.beginPath(); g.ellipse(0, 26, 22, 8, 0, 0, Math.PI * 2); g.fillStyle = '#e9edf3'; g.fill(); stroke(g, 2); g.strokeStyle = P.ink; g.lineWidth = 2; g.beginPath(); g.moveTo(0, 14); g.lineTo(0, 22); g.stroke();
    g.restore(); }
  function flagSprite(g, f) { // well-head goal: blue flag with a drop
    g.fillStyle = P.ink2; rr(g, 14, 4, 6, 90, 3); g.fill(); circle(g, 17, 4, 6, P.gold, P.ink, 2);
    const wv = f ? 6 : 0; g.beginPath(); g.moveTo(20, 10); g.bezierCurveTo(44, 4 + wv, 60, 22 - wv, 88, 12 + wv); g.lineTo(88, 50 + wv); g.bezierCurveTo(60, 60 - wv, 44, 42 + wv, 20, 48); g.closePath();
    g.fillStyle = lin(g, 20, 0, 88, 0, [P.waterL, P.water]); g.fill(); stroke(g, 3);
    g.fillStyle = P.white; g.beginPath(); g.moveTo(54, 18 + wv / 2); g.quadraticCurveTo(64, 32, 54, 40); g.quadraticCurveTo(44, 32, 54, 18 + wv / 2); g.fill(); }
  function devilSprite(g, f) {
    for (let i = 0; i < 9; i++) { const y = 88 - i * 9, w = 10 + i * 4.2, off = Math.sin(i * 0.9 + f * 1.6) * 7;
      g.globalAlpha = 0.85; ell(g, 48 + off, y, w, 5, i % 2 ? P.dust : P.dustD); }
    g.globalAlpha = 1; const r = rnd(40 + f); for (let i = 0; i < 10; i++) circle(g, 10 + r() * 76, 10 + r() * 70, 2 + r() * 2, P.dustD);
    circle(g, 40, 36, 6, P.white, P.ink, 2); circle(g, 58, 36, 6, P.white, P.ink, 2); circle(g, 41, 37, 2.5, P.ink); circle(g, 57, 37, 2.5, P.ink);
    g.strokeStyle = P.ink; g.lineWidth = 3; g.beginPath(); g.moveTo(33, 27); g.lineTo(45, 31); g.moveTo(65, 27); g.lineTo(53, 31); g.stroke(); }

  const SPRITES = {};
  const TILES = {};

  // ---------- backgrounds ----------
  const BIOMES = {
    tulare: { name: 'Tulare Basin, California', sky: ['#5fb6ff', '#bfe6ff', '#fff3d6'], sun: '#fff4b8', far2: '#c6d7e6', far: '#8fa9c4', snow: true, mid: ['#8cc66a', '#6fae52'], near: '#4f9a45', deco: 'orchard' },
    eloy:   { name: 'Eloy, Arizona', sky: ['#ff9a5c', '#ffcf8f', '#fff0d0'], sun: '#fff1c4', far2: '#e9b28e', far: '#c47d5e', mesa: true, mid: ['#e7c487', '#d6aa6a'], near: '#b88a50', deco: 'cactus' },
    konya:  { name: 'Karapınar, Konya', sky: ['#7fb0e8', '#cfe2f6', '#fbf4e4'], sun: '#fffbe2', far2: '#cfd0de', far: '#9d9bb2', mid: ['#e3c66e', '#cfae52'], near: '#b2923f', deco: 'wheat' },
    mexico: { name: 'Mexico City', sky: ['#5b67b8', '#c99ab8', '#ffc59a'], sun: '#ffe1b0', far2: '#9a9cc0', far: '#6f7298', snow: true, volcano: true, mid: ['#59607f', '#4a506d'], near: '#3c4159', deco: 'city' },
  };
  const BGW = 1920, BGH = 540, BG = {};
  function mountains(g, f, base, amp, col, light, snow) {
    let mx = 0; for (let x = 0; x <= BGW; x += 8) mx = Math.max(mx, Math.abs(f(x)));
    const yAt = (x) => base - (Math.abs(f(x)) / (mx || 1)) * amp;
    g.beginPath(); g.moveTo(0, BGH); for (let x = 0; x <= BGW; x += 8) g.lineTo(x, yAt(x)); g.lineTo(BGW, BGH); g.closePath();
    g.fillStyle = lin(g, 0, base - amp, 0, base + 60, [light, col]); g.fill();
    if (snow) { // snow only on the highest 25 % of the peaks, with a soft lower edge
      g.save(); g.clip(); const line = base - amp * 0.72;
      g.fillStyle = lin(g, 0, base - amp, 0, line + 14, ['rgba(255,255,255,.95)', 'rgba(255,255,255,.9)', 'rgba(255,255,255,0)']);
      g.fillRect(0, base - amp - 10, BGW, amp * 0.28 + 24); g.restore(); }
  }
  function buildBackgrounds() {
    for (const [id, b] of Object.entries(BIOMES)) {
      const layers = [];
      let [c, g] = mk(BGW, BGH);   // far range (pale)
      mountains(g, periodic(id.length * 11, BGW, 5), 300, 120, b.far2, b.sky[1], b.snow);
      layers.push({ c, k: 0.05 });
      [c, g] = mk(BGW, BGH);       // nearer range
      if (b.mesa) { g.fillStyle = lin(g, 0, 210, 0, 400, [b.far2, b.far]); const r = rnd(5); for (let x = 0; x < BGW; x += 260 + r() * 200) { const w = 140 + r() * 160, top = 250 + r() * 50; g.beginPath(); g.moveTo(x, 420); g.lineTo(x + 30, top); g.lineTo(x + w - 30, top); g.lineTo(x + w, 420); g.fill(); g.fillStyle = 'rgba(255,255,255,.18)'; g.fillRect(x + 30, top, w - 60, 6); g.fillStyle = lin(g, 0, 210, 0, 400, [b.far2, b.far]); }
        g.beginPath(); g.moveTo(900, 420); g.lineTo(960, 230); g.lineTo(985, 215); g.lineTo(1010, 250); g.lineTo(1070, 420); g.fill(); }
      else mountains(g, periodic(id.length * 23, BGW, 6), 350, 95, b.far, b.far2, b.snow && id === 'tulare');
      if (b.volcano) { g.beginPath(); g.moveTo(1200, 400); g.lineTo(1370, 190); g.lineTo(1420, 186); g.lineTo(1590, 400); g.fillStyle = lin(g, 0, 186, 0, 400, ['#c7c9e0', b.far]); g.fill(); g.fillStyle = '#ffffff'; g.beginPath(); g.moveTo(1338, 230); g.lineTo(1370, 190); g.lineTo(1420, 186); g.lineTo(1452, 230); g.quadraticCurveTo(1395, 246, 1338, 230); g.fill(); }
      // haze
      g.fillStyle = lin(g, 0, 300, 0, 430, ['rgba(255,255,255,0)', 'rgba(255,255,255,.45)']); g.fillRect(0, 300, BGW, 130);
      layers.push({ c, k: 0.12 });
      [c, g] = mk(BGW, BGH);       // mid: fields / city
      const r = rnd(id.length * 37);
      if (b.deco === 'city') {
        for (let x = 0; x < BGW; x += 46 + r() * 30) { const h = 90 + r() * 170, w = 40 + r() * 34, y = 430 - h;
          g.fillStyle = lin(g, x, 0, x + w, 0, [b.mid[0], b.mid[1]]); g.fillRect(x, y, w, h + 120); g.fillStyle = 'rgba(255,255,255,.12)'; g.fillRect(x, y, 4, h + 120);
          for (let wy = y + 10; wy < 420; wy += 16) for (let wx = x + 8; wx < x + w - 8; wx += 12) if (r() < 0.6) { g.fillStyle = r() < 0.75 ? '#ffd98a' : '#9fb6ff'; g.fillRect(wx, wy, 6, 8); } }
        // a tilted old building (sinking city)
        g.save(); g.translate(1500, 430); g.rotate(-0.06); g.fillStyle = '#8a7f9e'; g.fillRect(-40, -150, 80, 150); g.fillStyle = '#c9b8d9'; for (let i = 0; i < 5; i++) g.fillRect(-28, -138 + i * 28, 56, 12); g.restore();
      } else {
        const hf = periodic(id.length * 3, BGW, 4);
        g.beginPath(); g.moveTo(0, BGH); for (let x = 0; x <= BGW; x += 8) g.lineTo(x, 400 - hf(x) * 22); g.lineTo(BGW, BGH); g.fillStyle = lin(g, 0, 370, 0, BGH, [b.mid[0], b.mid[1]]); g.fill();
        for (let row = 0; row < 6; row++) { const y = 420 + row * 22; for (let x = (row % 2) * 60; x < BGW; x += 120 + r() * 80) { g.fillStyle = r() < 0.5 ? 'rgba(255,255,255,.12)' : 'rgba(0,0,0,.08)'; rr(g, x, y, 100 + r() * 60, 14, 6); g.fill(); } }
        for (let x = 20; x < BGW; x += 70 + r() * 60) {
          const y = 398 - hf(x) * 22;
          if (b.deco === 'orchard') { circle(g, x, y - 18, 16, rad(g, x - 5, y - 24, 2, 18, ['#7fc36a', '#3e8a3e'])); g.fillStyle = '#6b4428'; g.fillRect(x - 2, y - 4, 4, 8); }
          if (b.deco === 'cactus' && r() < 0.6) { g.fillStyle = '#4f8f44'; rr(g, x - 5, y - 42, 10, 44, 5); g.fill(); rr(g, x - 17, y - 30, 8, 16, 4); g.fill(); rr(g, x + 9, y - 34, 8, 14, 4); g.fill(); g.fillRect(x - 17, y - 18, 14, 6); g.fillRect(x + 3, y - 22, 14, 6); }
          if (b.deco === 'wheat' && r() < 0.3) { ell(g, x, y - 10, 16, 12, '#d9b65a'); ell(g, x, y - 16, 10, 7, '#e8c86c'); }
        }
        if (id === 'konya') { const mx = 760, my = 384; g.fillStyle = '#efe8d6'; rr(g, mx - 46, my - 26, 92, 30, 4); g.fill(); g.beginPath(); g.arc(mx, my - 26, 26, Math.PI, 0); g.fill(); rr(g, mx + 52, my - 86, 9, 90, 3); g.fill(); g.beginPath(); g.moveTo(mx + 50, my - 86); g.lineTo(mx + 56.5, my - 104); g.lineTo(mx + 63, my - 86); g.fill(); g.fillStyle = 'rgba(0,0,0,.08)'; g.fillRect(mx - 46, my - 6, 92, 10); }
        if (id === 'tulare') { for (let x = 300; x < BGW; x += 640) { g.fillStyle = '#d9d4c6'; g.fillRect(x, 352, 8, 60); g.fillStyle = '#ece7da'; g.beginPath(); g.ellipse(x + 4, 350, 26, 16, 0, 0, Math.PI * 2); g.fill(); } } // water towers
      }
      layers.push({ c, k: 0.3 });
      BG[id] = layers;
    }
  }
  function drawSky(ctx, b, w, h, t, camX) {
    ctx.fillStyle = (function () { const gr = ctx.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, b.sky[0]); gr.addColorStop(0.55, b.sky[1]); gr.addColorStop(1, b.sky[2]); return gr; })(); ctx.fillRect(0, 0, w, h);
    const sx = w * 0.8, sy = h * 0.2;
    ctx.fillStyle = rad(ctx, sx, sy, 10, 160, ['rgba(255,250,220,.9)', 'rgba(255,240,200,.25)', 'rgba(255,240,200,0)']); ctx.fillRect(sx - 160, sy - 160, 320, 320);
    circle(ctx, sx, sy, 36, b.sun);
    for (let i = 0; i < 5; i++) { const cx = ((i * 420 + 80 - camX * 0.04 + t * 8) % (w + 300)) - 150, cy = 60 + (i % 3) * 38, s = 0.7 + (i % 2) * 0.4;
      ctx.fillStyle = 'rgba(255,255,255,.88)'; [[0, 0, 34], [36, -14, 40], [76, 0, 30], [38, 8, 36]].forEach(([dx, dy, r]) => { ctx.beginPath(); ctx.arc(cx + dx * s, cy + dy * s, r * s, 0, Math.PI * 2); ctx.fill(); });
      ctx.fillStyle = 'rgba(200,215,235,.35)'; ctx.fillRect(cx - 30 * s, cy + 14 * s, 140 * s, 10 * s); }
  }
  function drawBackground(ctx, biome, camX, w, h, t) {
    const b = BIOMES[biome] || BIOMES.tulare; drawSky(ctx, b, w, h, t || 0, camX);
    for (const L of BG[biome] || BG.tulare) { const sw = L.c.width * (h / BGH), off = -((camX * L.k) % sw); for (let x = off; x < w; x += sw) ctx.drawImage(L.c, x, 0, sw, h); }
  }

  // ---------- real NISAR radar overlay ----------
  const RADAR = {};
  function loadImg(url) { return new Promise((res) => { const im = new Image(); im.onload = () => res(im); im.onerror = () => res(null); im.src = url; }); }
  function loadRadar(biome, url) { return loadImg(url).then((im) => { if (im) RADAR[biome] = im; return !!im; }); }
  function radarSweep(ctx, w, h, p, biome) {
    const front = p * (w + 400) - 200, a = Math.sin(Math.PI * Math.min(1, Math.max(0, p)));
    ctx.save(); ctx.beginPath(); ctx.rect(Math.max(0, front - 420), 0, Math.min(w, front) - Math.max(0, front - 420), h); ctx.clip();
    const im = RADAR[biome];
    if (im) { ctx.globalAlpha = 0.62 * a; ctx.drawImage(im, 0, 0, w, h); }
    else { ctx.globalAlpha = 0.3 * a; for (let x = Math.max(0, front - 420); x < front; x += 6) { ctx.fillStyle = `hsl(${(x * 2.5 + p * 360) % 360},85%,55%)`; ctx.fillRect(x, 0, 6, h); } }
    ctx.restore();
    ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = lin(ctx, front - 30, 0, front + 6, 0, ['rgba(255,255,255,0)', 'rgba(255,255,255,.9)']); ctx.fillRect(front - 30, 0, 36, h);
    ctx.restore();
    if (a > 0.2) { card(ctx, 18, h - 62, 360, 44, { bg: 'rgba(20,26,44,.86)', r: 14 }); text(ctx, im ? 'NISAR radar · real map, provisional' : 'NISAR radar scan', 34, h - 50, { size: 17, color: P.white, shadow: false }); }
  }

  // ---------- world map level select (our real atlas map) ----------
  let WORLD = null;
  function worldMap(ctx, w, h, t, pins, selected) {
    ctx.fillStyle = lin(ctx, 0, 0, 0, h, ['#0b1430', '#152451']); ctx.fillRect(0, 0, w, h);
    text(ctx, 'Choose a valley that NISAR measured', w / 2, 14, { size: 28, align: 'center', color: P.white });
    const mw = w - 120, mh = mw * 650 / 1800, mx = 60, my = 58;
    if (WORLD) ctx.drawImage(WORLD, mx, my, mw, mh); else { rr(ctx, mx, my, mw, mh, 16); ctx.fillStyle = '#1d3b6a'; ctx.fill(); }
    ctx.strokeStyle = 'rgba(255,255,255,.3)'; ctx.lineWidth = 2; rr(ctx, mx, my, mw, mh, 16); ctx.stroke();
    const n = (pins || []).length, cw = (w - 40 - (n - 1) * 14) / Math.max(1, n), cy = my + mh + 22;
    (pins || []).forEach((pn, i) => {
      const x = mx + (pn.lon + 130) / 280 * mw, y = my + (62 - pn.lat) / 107 * mh, sel = pn.id === selected, cx = 20 + i * (cw + 14);
      // leader line from pin to its card
      ctx.strokeStyle = sel ? P.yellow : 'rgba(255,255,255,.35)'; ctx.lineWidth = sel ? 3 : 1.5; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(cx + cw / 2, cy); ctx.stroke();
      if (!pn.locked) circle(ctx, x, y, 14 + 5 * Math.sin(t * 4 + i), 'rgba(255,210,63,.28)');
      circle(ctx, x, y, 13, pn.locked ? '#7c8396' : (sel ? P.yellow : '#ffe58a'), P.ink, 3);
      text(ctx, String(i + 1), x, y - 10, { size: 16, align: 'center', color: P.ink, shadow: false });
      card(ctx, cx, cy, cw, h - cy - 16, { bg: sel ? '#fff7e8' : 'rgba(255,247,232,.88)', r: 16, border: sel ? P.yellow : undefined });
      text(ctx, `${i + 1}. ${pn.name}`, cx + 14, cy + 10, { size: 17, color: P.ink, shadow: false });
      text(ctx, pn.locked ? 'Finish the previous valley' : (pn.rate != null ? `NISAR: ${pn.rate} cm per 100 days` : ''), cx + 14, cy + 36, { size: 13, color: pn.locked ? '#6b7286' : P.redD, shadow: false });
      for (let k = 0; k < 3; k++) icon(ctx, 'star', cx + 14 + k * 28, cy + 62, 22, k < (pn.stars || 0));
      if (sel && !pn.locked && Math.floor(t * 2) % 2) text(ctx, 'SPACE to play', cx + cw - 14, cy + 66, { size: 13, align: 'right', color: P.ink, shadow: false });
    });
  }

  // ---------- UI primitives ----------
  const FONT = '"Baloo 2", "Fredoka", "Trebuchet MS", system-ui, sans-serif';
  function text(ctx, s, x, y, o = {}) {
    ctx.font = `800 ${o.size || 16}px ${FONT}`; ctx.textAlign = o.align || 'left'; ctx.textBaseline = 'top';
    if (o.outline) { ctx.lineWidth = o.outline; ctx.strokeStyle = o.outlineColor || P.ink; ctx.lineJoin = 'round'; ctx.strokeText(s, x, y); }
    if (o.shadow !== false) { ctx.fillStyle = o.shadowColor || 'rgba(0,0,0,.35)'; ctx.fillText(s, x + 2, y + 3); }
    ctx.fillStyle = o.color || P.white; ctx.fillText(s, x, y);
  }
  function card(ctx, x, y, w, h, o = {}) {
    ctx.save(); ctx.shadowColor = 'rgba(0,0,0,.28)'; ctx.shadowBlur = 16; ctx.shadowOffsetY = 6;
    rr(ctx, x, y, w, h, o.r || 18); ctx.fillStyle = o.bg || P.cream; ctx.fill(); ctx.restore();
    if (!o.flat) { ctx.strokeStyle = o.border || 'rgba(255,255,255,.55)'; ctx.lineWidth = 2; rr(ctx, x + 1, y + 1, w - 2, h - 2, (o.r || 18) - 1); ctx.stroke(); }
  }
  function keycap(ctx, label, x, y) {
    ctx.font = `800 16px ${FONT}`; const w = Math.max(38, ctx.measureText(label).width + 22);
    rr(ctx, x, y + 4, w, 36, 9); ctx.fillStyle = '#9aa3b8'; ctx.fill();
    rr(ctx, x, y, w, 34, 9); ctx.fillStyle = lin(ctx, 0, y, 0, y + 34, ['#ffffff', '#e6eaf2']); ctx.fill(); ctx.strokeStyle = P.ink; ctx.lineWidth = 2.5; ctx.stroke();
    text(ctx, label, x + w / 2, y + 7, { size: 16, align: 'center', color: P.ink, shadow: false }); return w;
  }
  function tip(ctx, x, y, s, keys) {
    ctx.font = `800 19px ${FONT}`; const tw = ctx.measureText(s).width; let kw = 0; (keys || []).forEach((k) => { kw += Math.max(38, ctx.measureText(k).width + 22) + 8; });
    const w = Math.max(tw, kw) + 36, h = keys && keys.length ? 96 : 56, bx = Math.max(10, Math.min(x - w / 2, 950 - w));
    card(ctx, bx, y - h - 18, w, h, { bg: '#ffffff', r: 16 });
    ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.moveTo(x - 12, y - 19); ctx.lineTo(x, y - 2); ctx.lineTo(x + 12, y - 19); ctx.fill();
    text(ctx, s, bx + 18, y - h - 6, { size: 19, color: P.ink, shadow: false });
    let kx = bx + 18; (keys || []).forEach((k) => { kx += keycap(ctx, k, kx, y - 64) + 8; });
  }
  function icon(ctx, name, x, y, s, on = true) {
    ctx.save(); ctx.translate(x, y); const k = s / 24; ctx.scale(k, k); ctx.globalAlpha = on ? 1 : 0.3;
    if (name === 'heart') { ctx.beginPath(); ctx.moveTo(12, 21); ctx.bezierCurveTo(-4, 10, 2, -2, 12, 6); ctx.bezierCurveTo(22, -2, 28, 10, 12, 21); ctx.fillStyle = lin(ctx, 0, 0, 0, 22, ['#ff7f72', P.red]); ctx.fill(); ctx.strokeStyle = P.ink; ctx.lineWidth = 2; ctx.stroke(); }
    if (name === 'drop') { ctx.beginPath(); ctx.moveTo(12, 1); ctx.bezierCurveTo(22, 12, 21, 23, 12, 23); ctx.bezierCurveTo(3, 23, 2, 12, 12, 1); ctx.fillStyle = lin(ctx, 0, 0, 0, 24, ['#bfe8ff', P.water]); ctx.fill(); ctx.strokeStyle = P.ink; ctx.lineWidth = 2; ctx.stroke(); }
    if (name === 'star') { ctx.beginPath(); for (let i = 0; i < 10; i++) { const r = i % 2 ? 5 : 11, a = -Math.PI / 2 + i * Math.PI / 5; ctx.lineTo(12 + Math.cos(a) * r, 12 + Math.sin(a) * r); } ctx.closePath(); ctx.fillStyle = on ? P.yellow : '#c9ced8'; ctx.fill(); ctx.strokeStyle = P.ink; ctx.lineWidth = 2; ctx.stroke(); }
    if (name === 'chip' && SPRITES.chip) ctx.drawImage(SPRITES.chip[0], -6, -6, 36, 36);
    if (name === 'pump' && SPRITES.pump_on) ctx.drawImage(SPRITES.pump_on[0], 0, 0, 24, 24);
    if (name === 'crop' && SPRITES.crop_green) ctx.drawImage(SPRITES.crop_green[0], 0, 0, 24, 24);
    ctx.restore();
  }
  function hud(ctx, s, w, h) {
    card(ctx, 14, 12, 268, 62, { bg: 'rgba(20,26,44,.78)', r: 16 });
    for (let i = 0; i < 3; i++) icon(ctx, 'heart', 26 + i * 30, 18, 26, i < (s.hearts == null ? 3 : s.hearts));
    icon(ctx, 'drop', 26, 46, 20); const tm = s.tankMax || 10;
    for (let i = 0; i < tm; i++) { rr(ctx, 52 + i * 21, 48, 17, 16, 5); ctx.fillStyle = i < (s.tank || 0) ? lin(ctx, 0, 48, 0, 64, [P.waterL, P.water]) : 'rgba(255,255,255,.14)'; ctx.fill(); }
    const mx = w / 2 - 190, mw = 380, v = Math.max(0, Math.min(100, s.aquifer == null ? 70 : s.aquifer)), red = s.redLine == null ? 40 : s.redLine, low = v < red;
    card(ctx, mx, 12, mw, 62, { bg: 'rgba(20,26,44,.78)', r: 16 });
    text(ctx, 'UNDERGROUND WATER', mx + 16, 16, { size: 14, color: '#cfe9ff', shadow: false });
    rr(ctx, mx + 16, 40, mw - 32, 22, 11); ctx.fillStyle = '#3b2a1c'; ctx.fill();
    rr(ctx, mx + 16, 40, Math.max(22, (mw - 32) * v / 100), 22, 11); ctx.fillStyle = low ? lin(ctx, 0, 40, 0, 62, ['#ff8d80', P.red]) : lin(ctx, 0, 40, 0, 62, [P.waterL, P.water]); ctx.fill();
    const rx = mx + 16 + (mw - 32) * red / 100; ctx.fillStyle = P.yellow; rr(ctx, rx - 2, 34, 5, 34, 2); ctx.fill();
    ctx.fillStyle = P.yellow; ctx.beginPath(); ctx.moveTo(rx - 6, 30); ctx.lineTo(rx + 6, 30); ctx.lineTo(rx, 37); ctx.fill();
    if (low && Math.floor(Date.now() / 400) % 2) text(ctx, 'GROUND SINKING!', mx + mw / 2, 41, { size: 15, align: 'center', color: P.white, shadow: false });
    card(ctx, w - 300, 12, 286, 62, { bg: 'rgba(20,26,44,.78)', r: 16 });
    for (let i = 0; i < 3; i++) icon(ctx, 'chip', w - 288 + i * 30, 22, 24, i < (s.chips || 0));
    text(ctx, String(s.score || 0).padStart(6, '0'), w - 28, 18, { size: 26, align: 'right', color: P.yellow, shadow: false });
    if (s.level) text(ctx, s.level, w - 28, 50, { size: 12, align: 'right', color: '#cfe9ff', shadow: false });
  }
  function drawSatellite(ctx, x, y, s) {
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
    for (const d of [-1, 1]) { rr(ctx, d > 0 ? 18 : -78, -10, 60, 20, 4); ctx.fillStyle = lin(ctx, 0, -10, 0, 10, [P.panelL, P.panel]); ctx.fill(); ctx.strokeStyle = P.ink; ctx.lineWidth = 2.5; ctx.stroke(); ctx.strokeStyle = 'rgba(255,255,255,.35)'; ctx.lineWidth = 1.5; for (let i = 1; i < 4; i++) { const xx = (d > 0 ? 18 : -78) + i * 15; ctx.beginPath(); ctx.moveTo(xx, -10); ctx.lineTo(xx, 10); ctx.stroke(); } }
    rr(ctx, -18, -16, 36, 32, 7); ctx.fillStyle = lin(ctx, 0, -16, 0, 16, ['#ffe08a', P.sat, '#b98516']); ctx.fill(); ctx.strokeStyle = P.ink; ctx.lineWidth = 2.5; ctx.stroke();
    ctx.beginPath(); ctx.ellipse(0, 34, 34, 11, 0, 0, Math.PI * 2); ctx.fillStyle = '#eef1f6'; ctx.fill(); ctx.stroke(); ctx.beginPath(); ctx.moveTo(0, 16); ctx.lineTo(0, 26); ctx.stroke();
    ctx.restore();
  }
  function title(ctx, w, h, t) {
    drawBackground(ctx, 'tulare', t * 30, w, h, t);
    for (let x = -(t * 120 % TS); x < w; x += TS) { drawTile(ctx, 'grass', x, h - TS * 2); drawTile(ctx, 'dirt', x, h - TS); }
    const sx = ((t * 80) % (w + 300)) - 150, sy = 92 + Math.sin(t * 1.3) * 6;
    ctx.save(); ctx.globalAlpha = 0.22; ctx.fillStyle = lin(ctx, 0, sy, 0, h - TS * 2, ['#fff7c2', 'rgba(255,247,194,0)']); ctx.beginPath(); ctx.moveTo(sx - 10, sy + 40); ctx.lineTo(sx - 120, h - TS * 2); ctx.lineTo(sx + 120, h - TS * 2); ctx.lineTo(sx + 10, sy + 40); ctx.fill(); ctx.restore();
    drawSatellite(ctx, sx, sy, 0.9);
    const ly = h * 0.22 + Math.sin(t * 2) * 4;
    text(ctx, 'AQUIFER', w / 2, ly, { size: 96, align: 'center', color: '#7fd7ff', outline: 12, shadowColor: 'rgba(0,0,0,.35)' });
    text(ctx, 'RUN', w / 2, ly + 92, { size: 96, align: 'center', color: P.yellow, outline: 12, shadowColor: 'rgba(0,0,0,.35)' });
    card(ctx, w / 2 - 260, ly + 206, 520, 44, { bg: 'rgba(20,26,44,.8)', r: 22 });
    text(ctx, 'Save four real valleys from sinking ground', w / 2, ly + 214, { size: 20, align: 'center', color: P.white, shadow: false });
    drawSprite(ctx, 'nisa_run', Math.floor(t * 12), w / 2 - 24, h - TS * 2 - 84 + 2);
    if (Math.floor(t * 2) % 2) text(ctx, 'Press SPACE or tap to start', w / 2, h - 62, { size: 22, align: 'center', color: P.white, outline: 6 });
  }
  function fx(ctx, type, x, y, t) {
    if (type === 'splash') { for (let i = 0; i < 10; i++) { const a = -Math.PI * (i / 9), d = 8 + t * 46; circle(ctx, x + Math.cos(a) * d, y + Math.sin(a) * d * 0.8 + t * t * 30, 5 * (1 - t) + 1, P.waterL); } }
    else if (type === 'dust') { for (let i = 0; i < 7; i++) circle(ctx, x + (i - 3) * 9 * (1 + t), y - t * 22 - (i % 2) * 6, 9 * (1 - t * 0.6), `rgba(220,188,128,${0.7 * (1 - t)})`); }
    else if (type === 'crack') { ctx.strokeStyle = P.ink; ctx.lineWidth = 4; ctx.beginPath(); let cx = x, cy = y; ctx.moveTo(cx, cy); for (let i = 0; i < 7; i++) { cx += i % 2 ? 12 : -7; cy += 9; ctx.lineTo(cx, cy); } ctx.stroke(); }
    else if (type === 'sparkle') { ctx.fillStyle = P.yellow; const s = 6 + Math.sin(t * 10) * 3; ctx.beginPath(); ctx.moveTo(x, y - s * 2); ctx.lineTo(x + s * 0.5, y - s * 0.5); ctx.lineTo(x + s * 2, y); ctx.lineTo(x + s * 0.5, y + s * 0.5); ctx.lineTo(x, y + s * 2); ctx.lineTo(x - s * 0.5, y + s * 0.5); ctx.lineTo(x - s * 2, y); ctx.lineTo(x - s * 0.5, y - s * 0.5); ctx.fill(); }
  }

  function drawTile(ctx, name, x, y) { const c = TILES[name]; if (c) ctx.drawImage(c, Math.round(x), Math.round(y)); }
  function drawSprite(ctx, name, frame, x, y, flip) {
    const fr = SPRITES[name]; if (!fr) return; const c = fr[((frame | 0) % fr.length + fr.length) % fr.length];
    if (flip) { ctx.save(); ctx.translate(Math.round(x) + c.width, Math.round(y)); ctx.scale(-1, 1); ctx.drawImage(c, 0, 0); ctx.restore(); } else ctx.drawImage(c, Math.round(x), Math.round(y));
  }

  function build() {
    for (const n of TILE_NAMES) TILES[n] = tileCanvas(TILE_FN[n]);
    const person = (name, n, pose) => { SPRITES[name] = []; for (let f = 0; f < n; f++) { const [c, g] = mk(96, 168); nisa(g, pose, f); SPRITES[name].push(down(c, 48, 84)); } };
    person('nisa_idle', 2, 'idle'); person('nisa_run', 6, 'run'); person('nisa_jump', 1, 'jump'); person('nisa_action', 2, 'action');
    SPRITES.farmer = []; for (let f = 0; f < 2; f++) { const [c, g] = mk(96, 168); farmer(g, f); SPRITES.farmer.push(down(c, 48, 84)); }
    const obj = (name, n, fn) => { SPRITES[name] = []; for (let f = 0; f < n; f++) { const [c, g] = mk(96, 96); fn(g, f); SPRITES[name].push(down(c, 48, 48)); } };
    obj('pump_on', 2, (g, f) => pumpjack(g, true, f)); obj('pump_off', 1, (g) => pumpjack(g, false, 0));
    obj('crop_dry', 1, (g) => cropSprite(g, false)); obj('crop_green', 1, (g) => cropSprite(g, true));
    obj('drop', 4, dropSprite); obj('chip', 4, chipSprite); obj('flag', 2, flagSprite); obj('dust_devil', 4, devilSprite);
    buildBackgrounds();
  }

  const base = (typeof document !== 'undefined' && document.currentScript && document.currentScript.src) ? document.currentScript.src.replace(/[^/]*$/, '') : '';
  const ready = new Promise((res) => {
    const go = () => { build(); loadImg(base + '../assets/atlas_world.jpg').then((im) => { WORLD = im; res(); }); };
    if (document.fonts && document.fonts.load) Promise.all([document.fonts.load(`800 16px "Baloo 2"`)]).then(go, go); else go();
  });

  root.RunArt = { TILE: T, SCALE: SC, TS, P, BIOMES, TILE_NAMES, ready, drawTile, drawSprite, drawBackground, fx, radarSweep, loadRadar,
    worldMap, tip, keycap, icon, hud, title, card, text, drawSatellite, sprites: () => Object.keys(SPRITES), frames: (n) => (SPRITES[n] || []).length };
})(typeof window !== 'undefined' ? window : this);
