/* AQUIFER RUN — art module (PC1). Everything is drawn in code: original pixel art, no external
 * images. Contract: see web/run/DESIGN.md §10 (window.RunArt).
 *   RunArt.TILE = 16, RunArt.SCALE = 3, RunArt.ready (Promise)
 *   drawTile(ctx, name, x, y) · drawSprite(ctx, name, frame, x, y, flipX)
 *   drawBackground(ctx, biome, camX, w, h, t) · fx(ctx, type, x, y, t) · radarSweep(ctx, w, h, p)
 *   hud(ctx, state, w, h) · title(ctx, w, h, t) · card(ctx, x, y, w, h) · text(ctx, str, x, y, opts)
 */
(function (root) {
  'use strict';
  const T = 16, SC = 3;

  // ---------- palette (original, warm earth + water) ----------
  const P = {
    ink: '#1b1f2e', ink2: '#2c3247', white: '#fffaf0', cream: '#f6e7c8',
    skin: '#f2c49b', skinS: '#d79a6c', hair: '#3b2416',
    hat: '#e2a33b', hatS: '#b8781f', shirt: '#3f8fd2', shirtS: '#2d68a1', pants: '#33415c', boot: '#5a3a22',
    tank: '#4fc3f7', tankS: '#2b8bc4', gauge: '#ffe066',
    grass: '#5cbf4a', grassL: '#86dc5e', grassD: '#3a8f37',
    dirt: '#8a5a33', dirtL: '#a8733f', dirtD: '#6b4226',
    clay: '#c9a06a', clayL: '#ddb985', clayD: '#a87f4e',
    rock: '#7d8597', rockL: '#9aa2b2', rockD: '#5c6375',
    sand: '#e7c27d', sandL: '#f3d79c', sandD: '#c9a15c',
    road: '#55596a', roadL: '#6c7184', line: '#f2d26b',
    brick: '#b65a3c', brickL: '#cf7352', brickD: '#8e4128', mortar: '#d9c5a8',
    water: '#2f8de4', waterL: '#6fc0ff', waterD: '#1d5fb0', foam: '#d8f1ff',
    concrete: '#a9a59b', concreteD: '#86827a',
    metal: '#8d99ab', metalD: '#5e6878', metalL: '#c3ccd8', rust: '#b5651d',
    wood: '#a8713f', woodD: '#7a4f29', woodL: '#c78d55',
    leaf: '#3f9d48', leafL: '#6cc75a', leafD: '#2a6e34', trunk: '#6b4428',
    wheat: '#e8c25a', wheatD: '#c49a33', cotton: '#f4f1ea',
    red: '#e2463a', redD: '#a92d25', orange: '#f28c28', yellow: '#ffd23f', green: '#3fbf6a',
    roofT: '#c4553a', roofTD: '#93391f', wall: '#ecdcc0', wallD: '#cdb795', glass: '#8fd0ff',
    dust: '#d8b87a', dustD: '#b8975c',
  };

  // ---------- tiny helpers ----------
  function mk(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; const x = c.getContext('2d'); x.imageSmoothingEnabled = false; return [c, x]; }
  function rnd(seed) { let s = seed >>> 0 || 1; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }
  function px(g, x, y, c) { g.fillStyle = c; g.fillRect(x, y, 1, 1); }
  function rect(g, x, y, w, h, c) { g.fillStyle = c; g.fillRect(x, y, w, h); }
  function speck(g, x0, y0, w, h, cols, n, seed) { const r = rnd(seed); for (let i = 0; i < n; i++) px(g, x0 + Math.floor(r() * w), y0 + Math.floor(r() * h), cols[Math.floor(r() * cols.length)]); }
  function scaleUp(src) { const [c, g] = mk(src.width * SC, src.height * SC); g.drawImage(src, 0, 0, c.width, c.height); return c; }

  // ---------- tiles (16x16 base) ----------
  const TILE_FN = {
    grass(g) { rect(g, 0, 0, T, T, P.dirt); speck(g, 0, 5, T, 11, [P.dirtL, P.dirtD], 26, 11); rect(g, 0, 0, T, 4, P.grass); rect(g, 0, 4, T, 1, P.grassD);
      const r = rnd(7); for (let x = 0; x < T; x++) { if (r() < 0.55) px(g, x, 0, P.grassL); if (r() < 0.35) px(g, x, 4 + Math.floor(r() * 2), P.grassD); } px(g, 3, 1, P.grassL); px(g, 11, 2, P.grassL); },
    dirt(g) { rect(g, 0, 0, T, T, P.dirt); speck(g, 0, 0, T, T, [P.dirtL, P.dirtD, P.dirtD], 34, 21); px(g, 5, 9, P.rockL); px(g, 6, 9, P.rock); },
    clay(g) { rect(g, 0, 0, T, T, P.clay); for (let y = 2; y < T; y += 5) rect(g, 0, y, T, 1, P.clayD); speck(g, 0, 0, T, T, [P.clayL], 14, 31); },
    rock(g) { rect(g, 0, 0, T, T, P.rock); rect(g, 0, 0, T, 1, P.rockL); rect(g, 0, 15, T, 1, P.rockD); speck(g, 0, 0, T, T, [P.rockL, P.rockD], 20, 41); rect(g, 7, 3, 1, 6, P.rockD); rect(g, 8, 8, 5, 1, P.rockD); },
    sand(g) { rect(g, 0, 0, T, T, P.sand); speck(g, 0, 0, T, T, [P.sandL, P.sandD], 30, 51); rect(g, 0, 0, T, 1, P.sandL); },
    road(g) { rect(g, 0, 0, T, T, P.road); rect(g, 0, 0, T, 2, P.roadL); for (let x = 2; x < T; x += 8) rect(g, x, 7, 4, 1, P.line); speck(g, 0, 2, T, 14, [P.roadL], 8, 61); },
    brick(g) { rect(g, 0, 0, T, T, P.mortar); for (let row = 0; row < 4; row++) { const off = row % 2 ? 4 : 0; for (let x = -off; x < T; x += 8) { rect(g, x + 1, row * 4 + 1, 6, 3, P.brick); rect(g, x + 1, row * 4 + 1, 6, 1, P.brickL); } } },
    canal(g) { rect(g, 0, 0, T, T, P.concrete); rect(g, 0, 0, T, 2, P.concreteD); rect(g, 2, 3, 12, 13, P.water); rect(g, 2, 3, 12, 1, P.foam); speck(g, 2, 4, 12, 11, [P.waterL, P.waterD], 12, 71); },
    water(g) { rect(g, 0, 0, T, T, P.water); for (let x = 0; x < T; x += 4) { px(g, x, 1, P.waterL); px(g, x + 1, 0, P.foam); px(g, x + 2, 1, P.waterL); } speck(g, 0, 3, T, 13, [P.waterD, P.waterL], 14, 81); },
    pipe_v(g) { rect(g, 4, 0, 8, T, P.metal); rect(g, 4, 0, 2, T, P.metalL); rect(g, 10, 0, 2, T, P.metalD); rect(g, 3, 6, 10, 2, P.metalD); px(g, 6, 11, P.rust); px(g, 9, 13, P.rust); },
    pipe_h(g) { rect(g, 0, 4, T, 8, P.metal); rect(g, 0, 4, T, 2, P.metalL); rect(g, 0, 10, T, 2, P.metalD); rect(g, 6, 3, 2, 10, P.metalD); },
    crate(g) { rect(g, 0, 0, T, T, P.wood); rect(g, 0, 0, T, 1, P.woodL); rect(g, 0, 15, T, 1, P.woodD); rect(g, 0, 0, 1, T, P.woodD); rect(g, 15, 0, 1, T, P.woodD);
      for (let i = 1; i < 15; i++) { px(g, i, i, P.woodD); px(g, 15 - i, i, P.woodD); } rect(g, 1, 7, 14, 2, P.woodD); },
    sign(g) { rect(g, 7, 8, 2, 8, P.woodD); rect(g, 1, 2, 14, 7, P.woodL); rect(g, 1, 8, 14, 1, P.woodD); rect(g, 3, 4, 8, 1, P.woodD); rect(g, 3, 6, 6, 1, P.woodD); },
    sink1(g) { TILE_FN.grass(g); rect(g, 6, 1, 1, 4, P.ink2); px(g, 7, 5, P.ink2); px(g, 7, 6, P.dirtD); },
    sink2(g) { TILE_FN.grass(g); rect(g, 5, 0, 1, 3, P.ink2); px(g, 6, 3, P.ink2); rect(g, 7, 4, 1, 4, P.ink2); px(g, 8, 8, P.ink2); rect(g, 10, 0, 1, 2, P.ink2); px(g, 11, 2, P.ink2); },
    sink3(g) { TILE_FN.grass(g); rect(g, 4, 0, 2, 3, P.ink); rect(g, 6, 3, 1, 4, P.ink); rect(g, 7, 6, 2, 1, P.ink); rect(g, 8, 7, 1, 5, P.ink); rect(g, 11, 0, 1, 3, P.ink); rect(g, 12, 3, 1, 3, P.ink2); rect(g, 2, 9, 3, 1, P.ink2); },
    fissure(g) { rect(g, 0, 0, T, T, P.sand); speck(g, 0, 0, T, T, [P.sandD], 12, 91); rect(g, 6, 0, 4, T, P.ink); rect(g, 5, 0, 1, 5, P.sandD); rect(g, 10, 4, 1, 6, P.sandD); },
    sinkhole_edge(g) { rect(g, 0, 0, T, T, P.ink); rect(g, 0, 0, T, 3, P.dirtD); for (let x = 0; x < T; x += 3) px(g, x, 3, P.dirtD); },
    bridge(g) { rect(g, 0, 2, T, 4, P.wood); rect(g, 0, 2, T, 1, P.woodL); rect(g, 0, 5, T, 1, P.woodD); for (let x = 3; x < T; x += 5) rect(g, x, 2, 1, 4, P.woodD); rect(g, 1, 6, 1, 6, P.woodD); rect(g, 14, 6, 1, 6, P.woodD); },
    bridge_broken(g) { rect(g, 0, 2, 6, 4, P.wood); rect(g, 0, 2, 6, 1, P.woodL); rect(g, 11, 3, 5, 3, P.wood); px(g, 6, 3, P.woodD); px(g, 7, 5, P.woodD); rect(g, 1, 6, 1, 6, P.woodD); },
    house_wall(g) { rect(g, 0, 0, T, T, P.wall); rect(g, 0, 15, T, 1, P.wallD); rect(g, 4, 4, 8, 7, P.ink2); rect(g, 5, 5, 6, 5, P.glass); rect(g, 7, 5, 1, 5, P.ink2); rect(g, 5, 7, 6, 1, P.ink2); px(g, 6, 6, P.white); },
    house_roof(g) { for (let y = 0; y < T; y++) { const w = Math.min(T, 2 + y); rect(g, 0, y, T, 1, y < 2 ? P.roofTD : P.roofT); } for (let y = 3; y < T; y += 4) rect(g, 0, y, T, 1, P.roofTD); },
    tree(g) { rect(g, 7, 9, 2, 7, P.trunk); for (let y = 0; y < 11; y++) { const r = y < 5 ? 2 + y : 12 - y; rect(g, 8 - r, y, r * 2, 1, P.leaf); } speck(g, 2, 1, 12, 8, [P.leafL, P.leafD], 22, 101); },
    bush(g) { for (let y = 8; y < T; y++) { const r = Math.min(7, (y - 7) * 2); rect(g, 8 - r, y, r * 2, 1, P.leaf); } speck(g, 2, 9, 12, 7, [P.leafL, P.leafD], 16, 111); },
    wheat(g) { for (let x = 1; x < T; x += 3) { rect(g, x, 5, 1, 11, P.wheatD); rect(g, x - 1, 2, 3, 4, P.wheat); px(g, x, 1, P.wheat); } },
    cotton(g) { for (let x = 2; x < T; x += 5) { rect(g, x + 1, 7, 1, 9, P.leafD); rect(g, x, 4, 3, 3, P.cotton); px(g, x + 3, 8, P.cotton); px(g, x - 1, 9, P.cotton); } },
    orchard(g) { rect(g, 7, 10, 2, 6, P.trunk); for (let y = 2; y < 11; y++) { const r = y < 6 ? y : 11 - y; rect(g, 8 - r - 1, y, (r + 1) * 2, 1, P.leaf); } px(g, 5, 5, P.orange); px(g, 10, 6, P.orange); px(g, 8, 8, P.orange); },
    fence(g) { rect(g, 0, 7, T, 2, P.woodL); rect(g, 0, 11, T, 2, P.woodL); rect(g, 2, 5, 2, 11, P.wood); rect(g, 11, 5, 2, 11, P.wood); },
    lamp(g) { rect(g, 7, 3, 2, 13, P.ink2); rect(g, 5, 1, 6, 3, P.ink2); rect(g, 6, 2, 4, 2, P.yellow); },
  };
  const TILE_NAMES = Object.keys(TILE_FN);

  // ---------- sprites ----------
  // Nisa, 16x24, drawn part by part so frames stay consistent.
  function nisa(g, pose, f) {
    const bob = (pose === 'run' && (f % 2)) || (pose === 'idle' && f === 1) ? 1 : 0;
    const y0 = 2 + bob;
    // backpack tank (behind)
    rect(g, 2, y0 + 9, 4, 8, P.tankS); rect(g, 2, y0 + 9, 3, 7, P.tank); px(g, 3, y0 + 11, P.gauge); px(g, 3, y0 + 12, P.white);
    // legs
    const legs = { idle: [[6, 0], [9, 0]], jump: [[5, -2], [10, 1]], action: [[6, 0], [9, 0]] };
    let L = legs[pose] || [[6, 0], [9, 0]];
    if (pose === 'run') L = [[[5, -1], [10, 1]], [[6, 0], [9, 0]], [[8, 1], [7, -1]], [[6, 0], [9, 0]]][f % 4];
    for (const [lx, dy] of L) { rect(g, lx, y0 + 16 + Math.min(0, dy), 2, 5 - Math.abs(dy) + Math.max(0, dy), P.pants); rect(g, lx - (dy < 0 ? 1 : 0), y0 + 20 + Math.max(0, dy) - (dy < 0 ? 1 : 0), 3, 2, P.boot); }
    // torso
    rect(g, 5, y0 + 9, 7, 8, P.shirt); rect(g, 5, y0 + 15, 7, 2, P.shirtS); rect(g, 5, y0 + 9, 1, 8, P.shirtS); px(g, 8, y0 + 10, P.white);
    // strap
    rect(g, 7, y0 + 9, 1, 7, P.tankS);
    // arms
    if (pose === 'action') { rect(g, 11, y0 + 10, 4, 2, P.shirt); rect(g, 15, y0 + 10, 1, 2, P.skin); rect(g, 14, y0 + 9, 2, 1, P.metal); }
    else if (pose === 'jump') { rect(g, 11, y0 + 7, 2, 4, P.shirt); px(g, 12, y0 + 6, P.skin); }
    else { const sw = pose === 'run' ? [1, 0, -1, 0][f % 4] : 0; rect(g, 11, y0 + 10 + sw, 2, 5, P.shirt); rect(g, 11, y0 + 15 + sw, 2, 1, P.skin); }
    // head
    rect(g, 6, y0 + 3, 6, 6, P.skin); rect(g, 6, y0 + 8, 6, 1, P.skinS); px(g, 10, y0 + 5, P.ink); px(g, 11, y0 + 7, P.skinS);
    rect(g, 5, y0 + 4, 2, 4, P.hair); rect(g, 4, y0 + 6, 2, 3, P.hair);
    // hat (wide brim)
    rect(g, 3, y0 + 2, 12, 2, P.hat); rect(g, 6, y0, 6, 2, P.hat); rect(g, 6, y0 + 1, 6, 1, P.hatS); rect(g, 3, y0 + 3, 12, 1, P.hatS);
  }
  function farmer(g, f) { nisa(g, 'idle', f); rect(g, 5, 11, 7, 6, '#6a8f3c'); rect(g, 3, 2, 12, 2, P.wheat); rect(g, 6, 0, 6, 2, P.wheat); rect(g, 2, 11, 4, 8, '#00000000'); g.clearRect(2, 11, 3, 8); rect(g, 6, 9, 6, 2, '#9b6b43'); }
  function pump(g, on, f) {
    rect(g, 2, 12, 12, 4, P.concrete); rect(g, 2, 12, 12, 1, P.concreteD);
    rect(g, 6, 3, 4, 9, on ? P.red : P.metal); rect(g, 6, 3, 1, 9, on ? P.redD : P.metalD);
    const a = on ? (f ? -2 : 1) : 3; // walking beam
    rect(g, 1, 3 + a, 14, 2, P.ink2); rect(g, 1, 3 + a, 2, 4, P.ink2);
    rect(g, 11, 6, 3, 3, P.metalD); px(g, 12, 7, on ? P.yellow : P.metalL);
    if (on) { px(g, 3, 1, P.waterL); px(g, 4, 0, P.waterL); } else { rect(g, 9, 9, 6, 3, P.green); px(g, 10, 10, P.white); px(g, 11, 11, P.white); px(g, 12, 10, P.white); px(g, 13, 9, P.white); }
  }
  function crop(g, green) { const c = green ? P.leaf : '#b49a5c', l = green ? P.leafL : '#d2bd83';
    for (let x = 2; x < 16; x += 4) { rect(g, x, 8, 1, 8, c); px(g, x - 1, 9, l); px(g, x + 1, 11, l); px(g, x - 1, 12, c); if (green) { rect(g, x - 1, 5, 3, 3, P.wheat); } else { px(g, x + 1, 7, c); px(g, x + 2, 8, c); } } }
  function drop(g, f) { const y = [0, 1, 0, -1][f % 4]; rect(g, 6, 5 + y, 4, 6, P.water); rect(g, 7, 3 + y, 2, 2, P.water); px(g, 8, 2 + y, P.water); rect(g, 5, 7 + y, 6, 3, P.water); px(g, 6, 6 + y, P.waterL); px(g, 6, 7 + y, P.foam); rect(g, 6, 11 + y, 4, 1, P.waterD); }
  function chip(g, f) { const w = [8, 6, 2, 6][f % 4], x0 = 8 - w / 2; rect(g, x0, 3, w, 10, P.metalD); rect(g, x0, 3, w, 1, P.metalL); if (w > 2) { rect(g, x0 + 1, 5, w - 2, 6, '#2f6fd6'); px(g, 8, 7, P.yellow); } rect(g, 2, 7, 2, 2, P.metal); rect(g, 12, 7, 2, 2, P.metal); }
  function flag(g, f) { rect(g, 3, 0, 1, 16, P.ink2); const wv = f ? 1 : 0; rect(g, 4, 1 + wv, 9, 6, P.water); rect(g, 4, 1 + wv, 9, 1, P.waterL); px(g, 8, 3 + wv, P.white); px(g, 9, 4 + wv, P.white); px(g, 7, 4 + wv, P.white); rect(g, 1, 15, 5, 1, P.ink2); }
  function devil(g, f) { const r = rnd(200 + f); for (let y = 2; y < 16; y++) { const w = Math.max(2, Math.floor((16 - y) * 0.7)); const off = Math.round(Math.sin((y + f * 2) * 0.8) * 2); rect(g, 8 - w / 2 + off, y, w, 1, y % 3 ? P.dust : P.dustD); }
    for (let i = 0; i < 6; i++) px(g, Math.floor(r() * 16), Math.floor(r() * 14), P.dustD); px(g, 7, 6, P.ink); px(g, 10, 6, P.ink); }

  function outline(c, g) {
    const w = c.width, h = c.height, d = g.getImageData(0, 0, w, h), a = d.data, out = new Uint8ClampedArray(a);
    const op = (x, y) => x >= 0 && y >= 0 && x < w && y < h && a[(y * w + x) * 4 + 3] > 40;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      if (op(x, y)) continue;
      if (op(x - 1, y) || op(x + 1, y) || op(x, y - 1) || op(x, y + 1)) { const i = (y * w + x) * 4; out[i] = 27; out[i + 1] = 31; out[i + 2] = 46; out[i + 3] = 255; }
    }
    g.putImageData(new ImageData(out, w, h), 0, 0);
  }
  const SPRITES = {}; // name -> [canvas frames]
  function addSprite(name, n, w, h, fn) { SPRITES[name] = []; for (let f = 0; f < n; f++) { const [c, g] = mk(w + 2, h + 2); g.translate(1, 1); fn(g, f); g.setTransform(1, 0, 0, 1, 0, 0); outline(c, g); SPRITES[name].push(scaleUp(c)); } }
  const TILES = {};

  function build() {
    for (const name of TILE_NAMES) { const [c, g] = mk(T, T); TILE_FN[name](g); TILES[name] = scaleUp(c); }
    addSprite('nisa_idle', 2, 16, 26, (g, f) => nisa(g, 'idle', f));
    addSprite('nisa_run', 4, 16, 26, (g, f) => nisa(g, 'run', f));
    addSprite('nisa_jump', 1, 16, 26, (g, f) => nisa(g, 'jump', f));
    addSprite('nisa_action', 2, 16, 26, (g, f) => nisa(g, 'action', f));
    addSprite('farmer', 2, 16, 26, farmer);
    addSprite('pump_on', 2, 16, 16, (g, f) => pump(g, true, f));
    addSprite('pump_off', 1, 16, 16, (g, f) => pump(g, false, f));
    addSprite('crop_dry', 1, 16, 16, (g) => crop(g, false));
    addSprite('crop_green', 1, 16, 16, (g) => crop(g, true));
    addSprite('drop', 4, 16, 16, drop);
    addSprite('chip', 4, 16, 16, chip);
    addSprite('flag', 2, 16, 16, flag);
    addSprite('dust_devil', 4, 16, 16, devil);
    buildBackgrounds();
  }

  // ---------- parallax backgrounds (pre-rendered low-res strips, scaled up) ----------
  const BIOMES = {
    tulare: { sky: ['#7cc6ff', '#cdeeff'], sun: '#fff2a8', far: '#9db8c9', farHi: '#c4d6e0', mid: '#7fb35a', midHi: '#a3cf6c', near: '#5a9a45', deco: 'orchard', name: 'Tulare Basin' },
    eloy:   { sky: ['#ffb36b', '#ffe5b8'], sun: '#fff1c9', far: '#c98a6b', farHi: '#e0a785', mid: '#d9b278', midHi: '#ecc98f', near: '#c49a5c', deco: 'cactus', name: 'Eloy, Arizona' },
    konya:  { sky: ['#8fb7e6', '#e9f1f9'], sun: '#fffbe0', far: '#a9a6b8', farHi: '#d6d4e0', mid: '#d6bd6a', midHi: '#ead07e', near: '#b49a4c', deco: 'wheat', name: 'Karapınar, Konya' },
    mexico: { sky: ['#6f7fbf', '#f2b7a0'], sun: '#ffe2b0', far: '#7b7f9e', farHi: '#a3a6c2', mid: '#5e6380', midHi: '#7c82a3', near: '#4a4f68', deco: 'city', name: 'Mexico City' },
  };
  const BG = {};
  const STRIP_W = 320, STRIP_H = 180; // low-res, scaled ×3 to 960×540
  function ridge(g, w, h, base, amp, col, hiCol, seed, step) {
    const r = rnd(seed); let y = base; const pts = [];
    for (let x = 0; x <= w; x += step) { y += (r() - 0.5) * amp; y = Math.max(base - amp * 2, Math.min(base + amp, y)); pts.push([x, Math.round(y)]); }
    g.fillStyle = col; g.beginPath(); g.moveTo(0, h); for (const [x, yy] of pts) g.lineTo(x, yy); g.lineTo(w, h); g.fill();
    g.fillStyle = hiCol; for (let i = 0; i < pts.length - 1; i++) { const [x, yy] = pts[i]; if (pts[i + 1][1] > yy) rect(g, x, yy, step, 1, hiCol); }
    // make the strip tile seamlessly: copy the left edge height to the right
  }
  function buildBackgrounds() {
    for (const [id, b] of Object.entries(BIOMES)) {
      const layers = [];
      let [c, g] = mk(STRIP_W, STRIP_H);
      ridge(g, STRIP_W, STRIP_H, 86, 12, b.farHi, b.sky[1], id.length * 29, 5);
      layers.push({ c: scaleUp(c), k: 0.07 });
      // far layer
      [c, g] = mk(STRIP_W, STRIP_H);
      if (id === 'mexico') { ridge(g, STRIP_W, STRIP_H, 95, 6, b.far, b.farHi, 3, 8); g.fillStyle = b.farHi; g.beginPath(); g.moveTo(200, 95); g.lineTo(235, 52); g.lineTo(245, 50); g.lineTo(282, 95); g.fill(); rect(g, 236, 50, 8, 3, P.white); }
      else if (id === 'eloy') { ridge(g, STRIP_W, STRIP_H, 105, 5, b.far, b.farHi, 5, 10); g.fillStyle = b.far; g.beginPath(); g.moveTo(140, 110); g.lineTo(160, 62); g.lineTo(168, 58); g.lineTo(176, 70); g.lineTo(196, 110); g.fill(); }
      else ridge(g, STRIP_W, STRIP_H, 100, 9, b.far, b.farHi, id.length * 13, 6);
      layers.push({ c: scaleUp(c), k: 0.15 });
      // haze band between far range and fields
      [c, g] = mk(STRIP_W, STRIP_H); const hz = g.createLinearGradient(0, 96, 0, 126); hz.addColorStop(0, 'rgba(255,255,255,0)'); hz.addColorStop(1, 'rgba(255,255,255,.35)');
      g.fillStyle = hz; g.fillRect(0, 96, STRIP_W, 30); layers.push({ c: scaleUp(c), k: 0.15 });
      // mid layer: fields / city
      [c, g] = mk(STRIP_W, STRIP_H);
      if (id === 'mexico') {
        const r = rnd(9); for (let x = 0; x < STRIP_W; x += 9 + Math.floor(r() * 6)) { const h = 20 + Math.floor(r() * 45), w = 7 + Math.floor(r() * 7); rect(g, x, 130 - h, w, h + 50, b.mid); rect(g, x, 130 - h, 1, h + 50, b.midHi);
          for (let wy = 130 - h + 3; wy < 128; wy += 4) for (let wx = x + 2; wx < x + w - 1; wx += 3) if (r() < 0.55) px(g, wx, wy, '#ffd98a'); }
      } else {
        ridge(g, STRIP_W, STRIP_H, 114, 5, b.mid, b.midHi, id.length * 7, 10);
        const pr = rnd(id.length * 5); const shades = [b.mid, b.midHi, b.near];
        for (let y = 122; y < STRIP_H; y += 7) for (let x = 0; x < STRIP_W; x += 24 + Math.floor(pr() * 16)) rect(g, x, y, 22 + Math.floor(pr() * 14), 6, shades[Math.floor(pr() * 3)]);
        for (let y = 122; y < STRIP_H; y += 7) rect(g, 0, y + 6, STRIP_W, 1, 'rgba(0,0,0,.12)');
        const r = rnd(id.length * 31);
        for (let x = 4; x < STRIP_W; x += 14) {
          if (b.deco === 'orchard') { rect(g, x + 2, 117, 1, 4, P.trunk); rect(g, x, 112, 5, 5, P.leafD); px(g, x + 1, 113, P.leaf); }
          if (b.deco === 'cactus' && r() < 0.5) { rect(g, x + 2, 108, 2, 12, '#4f8a3c'); rect(g, x, 112, 2, 4, '#4f8a3c'); rect(g, x + 4, 111, 2, 3, '#4f8a3c'); }
          if (b.deco === 'wheat' && r() < 0.35) { rect(g, x, 113, 2, 8, '#8b7a5a'); rect(g, x - 2, 111, 6, 2, '#7a6a4a'); }
        }
        if (id === 'konya') { rect(g, 60, 104, 3, 16, '#e8e2d0'); g.fillStyle = '#e8e2d0'; g.beginPath(); g.arc(61.5, 103, 5, Math.PI, 0); g.fill(); rect(g, 52, 112, 20, 9, '#e8e2d0'); }
      }
      layers.push({ c: scaleUp(c), k: 0.4 });
      // near layer (bushes / posts)
      [c, g] = mk(STRIP_W, STRIP_H);
      const r = rnd(id.length * 47);
      for (let x = 0; x < STRIP_W; x += 22 + Math.floor(r() * 18)) {
        if (id === 'mexico') { rect(g, x, 150, 1, 30, P.ink2); rect(g, x - 2, 148, 5, 2, P.ink2); px(g, x, 147, P.yellow); }
        else { for (let yy = 0; yy < 8; yy++) { const w = 10 - Math.abs(4 - yy) * 2; rect(g, x + (10 - w) / 2, 152 + yy, w, 1, b.near); } }
      }
      layers.push({ c: scaleUp(c), k: 0.7 });
      BG[id] = layers;
    }
  }

  function drawBackground(ctx, biome, camX, w, h, t) {
    const b = BIOMES[biome] || BIOMES.tulare;
    const gr = ctx.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, b.sky[0]); gr.addColorStop(1, b.sky[1]);
    ctx.fillStyle = gr; ctx.fillRect(0, 0, w, h);
    // sun with pixel halo
    const sx = w * 0.78, sy = h * 0.2;
    ctx.fillStyle = b.sun; ctx.globalAlpha = 0.35; ctx.fillRect(sx - 42, sy - 42, 84, 84); ctx.globalAlpha = 1;
    ctx.fillRect(sx - 27, sy - 27, 54, 54); ctx.fillRect(sx - 33, sy - 15, 66, 30); ctx.fillRect(sx - 15, sy - 33, 30, 66);
    // drifting pixel clouds
    ctx.fillStyle = 'rgba(255,255,255,.85)';
    for (let i = 0; i < 4; i++) { const cx = ((i * 330 - camX * 0.05 + t * 6) % (w + 240)) - 120, cy = 50 + i * 28;
      ctx.fillRect(cx, cy, 96, 18); ctx.fillRect(cx + 18, cy - 12, 48, 12); ctx.fillRect(cx + 54, cy - 6, 30, 6); }
    for (const L of BG[biome] || BG.tulare) {
      const sw = L.c.width, off = -((camX * L.k) % sw);
      for (let x = off; x < w; x += sw) ctx.drawImage(L.c, Math.floor(x), h - L.c.height * (h / L.c.height), sw, h);
    }
  }

  // ---------- effects ----------
  function fx(ctx, type, x, y, t) {
    if (type === 'splash') { ctx.fillStyle = P.waterL; for (let i = 0; i < 8; i++) { const a = i / 8 * Math.PI * 2, d = 6 + t * 40; ctx.fillRect(x + Math.cos(a) * d, y - Math.abs(Math.sin(a)) * d, 6, 6); } }
    else if (type === 'dust') { ctx.fillStyle = 'rgba(216,184,122,.8)'; for (let i = 0; i < 6; i++) ctx.fillRect(x + (i - 3) * 8 * (1 + t), y - t * 20 - (i % 2) * 6, 6, 6); }
    else if (type === 'crack') { ctx.fillStyle = P.ink; let cx = x, cy = y; for (let i = 0; i < 8; i++) { cx += (i % 2 ? 6 : -3); cy += 4; ctx.fillRect(cx, cy, 3, 6); } }
    else if (type === 'sparkle') { ctx.fillStyle = P.yellow; const s = 3 + Math.sin(t * 10) * 2; ctx.fillRect(x - s, y, s * 2 + 3, 3); ctx.fillRect(x, y - s, 3, s * 2 + 3); }
  }
  // Interferogram-like fringe sweep (one colour cycle per band), the way real InSAR maps look.
  function radarSweep(ctx, w, h, p) {
    const band = 24, front = p * (w + 300) - 150;
    ctx.save(); ctx.globalAlpha = 0.28 * Math.sin(Math.PI * p);
    for (let x = Math.max(0, front - 300); x < Math.min(w, front); x += 6) {
      const hue = ((x / band) * 60 + p * 360) % 360; ctx.fillStyle = `hsl(${hue},85%,55%)`; ctx.fillRect(x, 0, 6, h);
    }
    ctx.globalAlpha = 0.9 * Math.sin(Math.PI * p); ctx.fillStyle = '#ffffff'; ctx.fillRect(front, 0, 3, h);
    ctx.restore();
  }

  // ---------- text, panels, HUD, title ----------
  const FONT = '"Press Start 2P", "Courier New", monospace';
  function text(ctx, s, x, y, o = {}) {
    ctx.font = `${o.size || 12}px ${FONT}`; ctx.textAlign = o.align || 'left'; ctx.textBaseline = 'top';
    if (o.shadow !== false) { ctx.fillStyle = o.shadowColor || P.ink; ctx.fillText(s, x + (o.size || 12) / 6, y + (o.size || 12) / 6); }
    ctx.fillStyle = o.color || P.white; ctx.fillText(s, x, y);
  }
  function card(ctx, x, y, w, h, o = {}) {
    ctx.fillStyle = P.ink; ctx.fillRect(x - 3, y + 3, w + 6, h); ctx.fillRect(x, y, w, h + 6);
    ctx.fillStyle = o.bg || P.cream; ctx.fillRect(x, y, w, h);
    ctx.fillStyle = 'rgba(255,255,255,.55)'; ctx.fillRect(x, y, w, 3); ctx.fillStyle = 'rgba(0,0,0,.12)'; ctx.fillRect(x, y + h - 3, w, 3);
  }
  function hud(ctx, s, w, h) {
    // left: hearts + tank
    card(ctx, 12, 10, 250, 54, { bg: 'rgba(27,31,46,.82)' });
    for (let i = 0; i < 3; i++) { ctx.fillStyle = i < (s.hearts ?? 3) ? P.red : '#4a5068'; const hx = 24 + i * 26; ctx.fillRect(hx, 20, 8, 6); ctx.fillRect(hx + 10, 20, 8, 6); ctx.fillRect(hx - 2, 24, 22, 6); ctx.fillRect(hx + 2, 30, 14, 4); ctx.fillRect(hx + 6, 34, 6, 3); }
    text(ctx, 'TANK', 24, 44, { size: 8, color: P.tank });
    const tm = s.tankMax || 10; for (let i = 0; i < tm; i++) { ctx.fillStyle = i < (s.tank || 0) ? P.tank : '#3a4058'; ctx.fillRect(64 + i * 18, 42, 14, 12); }
    // centre: aquifer meter with red line
    const mx = w / 2 - 170, mw = 340;
    card(ctx, mx, 10, mw, 54, { bg: 'rgba(27,31,46,.82)' });
    text(ctx, 'UNDERGROUND WATER', mx + 10, 16, { size: 8, color: P.foam });
    ctx.fillStyle = '#3a2a1c'; ctx.fillRect(mx + 10, 32, mw - 20, 20);
    const v = Math.max(0, Math.min(100, s.aquifer ?? 70)), red = s.redLine ?? 40;
    ctx.fillStyle = v < red ? P.red : P.water; ctx.fillRect(mx + 10, 32, (mw - 20) * v / 100, 20);
    ctx.fillStyle = P.waterL; ctx.fillRect(mx + 10, 32, (mw - 20) * v / 100, 4);
    const rx = mx + 10 + (mw - 20) * red / 100; ctx.fillStyle = P.yellow; ctx.fillRect(rx - 1, 28, 3, 28);
    if (v < red) text(ctx, 'GROUND SINKING!', mx + mw / 2, 36, { size: 8, color: P.yellow, align: 'center' });
    // right: chips + score
    card(ctx, w - 232, 10, 220, 54, { bg: 'rgba(27,31,46,.82)' });
    for (let i = 0; i < 3; i++) { ctx.globalAlpha = i < (s.chips || 0) ? 1 : 0.3; ctx.drawImage(SPRITES.chip[0], w - 224 + i * 34, 16, 32, 32); }
    ctx.globalAlpha = 1;
    text(ctx, String(s.score || 0).padStart(6, '0'), w - 22, 24, { size: 14, align: 'right', color: P.yellow });
    if (s.level) text(ctx, s.level, w - 22, 46, { size: 7, align: 'right', color: P.foam, shadow: false });
  }
  function title(ctx, w, h, t) {
    drawBackground(ctx, 'tulare', t * 40, w, h, t);
    // ground strip
    for (let x = 0; x < w; x += T * SC) { ctx.drawImage(TILES.grass, x, h - T * SC * 2); ctx.drawImage(TILES.dirt, x, h - T * SC); }
    // satellite crossing
    const sx = (t * 70) % (w + 200) - 100, sy = 70 + Math.sin(t) * 6;
    ctx.fillStyle = P.metalL; ctx.fillRect(sx, sy, 24, 12); ctx.fillStyle = '#2f6fd6'; ctx.fillRect(sx - 30, sy + 2, 28, 8); ctx.fillRect(sx + 26, sy + 2, 28, 8);
    ctx.fillStyle = P.white; ctx.fillRect(sx + 8, sy + 12, 8, 4); ctx.globalAlpha = 0.25; ctx.fillStyle = P.yellow; ctx.beginPath(); ctx.moveTo(sx + 12, sy + 16); ctx.lineTo(sx - 30, h - 96); ctx.lineTo(sx + 54, h - 96); ctx.fill(); ctx.globalAlpha = 1;
    // logo
    const ly = h * 0.24 + Math.sin(t * 2) * 4;
    text(ctx, 'AQUIFER', w / 2, ly, { size: 54, align: 'center', color: P.tank, shadowColor: P.ink });
    text(ctx, 'RUN', w / 2, ly + 66, { size: 54, align: 'center', color: P.yellow, shadowColor: P.ink });
    text(ctx, 'KEEP THE GROUND FROM SINKING', w / 2, ly + 138, { size: 12, align: 'center', color: P.white });
    // hero
    const fr = Math.floor(t * 8) % 4; ctx.drawImage(SPRITES.nisa_run[fr], w / 2 - 24, h - T * SC * 2 - 78);
    if (Math.floor(t * 2) % 2) text(ctx, 'PRESS START', w / 2, h - 60, { size: 14, align: 'center', color: P.white });
  }

  function drawTile(ctx, name, x, y) { const c = TILES[name]; if (c) ctx.drawImage(c, Math.floor(x), Math.floor(y)); }
  function drawSprite(ctx, name, frame, x, y, flip) {
    const fr = SPRITES[name]; if (!fr) return; const c = fr[((frame | 0) % fr.length + fr.length) % fr.length];
    if (flip) { ctx.save(); ctx.translate(Math.floor(x) + c.width, Math.floor(y)); ctx.scale(-1, 1); ctx.drawImage(c, 0, 0); ctx.restore(); }
    else ctx.drawImage(c, Math.floor(x), Math.floor(y));
  }

  const ready = new Promise((res) => {
    const go = () => { build(); res(); };
    if (document.fonts && document.fonts.load) document.fonts.load(`12px ${FONT}`).then(go, go); else go();
  });

  root.RunArt = { TILE: T, SCALE: SC, P, BIOMES, TILE_NAMES, ready, drawTile, drawSprite, drawBackground, fx, radarSweep, hud, title, card, text,
    sprites: () => Object.keys(SPRITES), frames: (n) => (SPRITES[n] || []).length };
})(typeof window !== 'undefined' ? window : this);
