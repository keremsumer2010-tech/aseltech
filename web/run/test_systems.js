// Aquifer Run rule + level checks (PC1). Usage: node web/run/test_systems.js
const fs = require('fs'), path = require('path');
const Sys = require('./systems.js');
const Engine = require('./engine.js');
let fail = 0;
const ok = (cond, msg) => { if (!cond) { fail++; console.log('  FAIL:', msg); } };

// ---------- rules ----------
const lvl = { id: 't', aquifer: { start: 50, redLine: 40, drainPerPump: 1, recharge: 0, pumpBoost: 0 }, tiles: ['....', 'SSGG'], legend: { S: 'sink1', G: 'grass' },
  entities: [{ type: 'pump' }, { type: 'pump' }, { type: 'crop' }, { type: 'chip', fact: 'a' }, { type: 'chip', fact: 'qc' }], nisar: { realFactCm: -7.3 } };
let s = Sys.createLevelState(lvl);
Sys.update(s, 1, []); ok(Math.abs(s.aquifer - 48) < 1e-6, 'two running pumps drain 2 per second');
Sys.update(s, 1, [{ type: 'action', target: 'pump' }]); ok(s.pumpsOff === 1 && Math.abs(s.aquifer - 47) < 1e-6, 'pump off reduces drain');
const crop = { watered: true }; s.tank = 0; Sys.update(s, 0, [{ type: 'action', target: 'crop', entity: crop }]);
ok(crop.watered === false && s.cropsWatered === 0, 'crop needs water in the tank (veto)');
s.tank = 4; Sys.update(s, 0, [{ type: 'action', target: 'crop', entity: { watered: true } }]); ok(s.tank === 3 && s.cropsWatered === 1, 'crop watering costs 1');
Sys.update(s, 0, [{ type: 'pickup', target: 'chip', fact: 'qc' }]); ok(s.qcFound && s.chips === 0, 'qc chip is the bad-data trap, not a real chip');
Sys.update(s, 0, [{ type: 'pickup', target: 'chip', fact: 'a' }]); ok(s.chips === 1 && s.chipsTotal === 1, 'real chips counted');
s.aquifer = 30; s.playerTx = 0; for (let i = 0; i < 30; i++) Sys.update(s, 0.2, []);
const drops = Sys.sinkTilesToDrop(s); ok(drops.length >= 1 && s.belowRedEver, 'below the safe line, nearby cracked ground collapses');
ok(Sys.aquiferInfo(s).cmSunk === s.permanentTiles * 2, '1 collapsed tile = 2 cm');
Sys.update(s, 0, [{ type: 'reachFlag' }]); const sc = Sys.score(s);
ok(sc.stars[0] === true && sc.stars[1] === false && sc.stars[2] === true, 'stars: end yes, safe line no, chips yes');
ok(sc.report.realFactCm === -7.3 && /provisional/.test(sc.report.calibration), 'report carries the real NISAR number and calibration sentence');

// ---------- levels ----------
const dir = path.join(__dirname, 'levels');
const files = fs.readdirSync(dir).filter((f) => f.endsWith('.json'));
ok(files.length === 4, 'four levels');
for (const f of files) {
  const L = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
  ok(L.tiles.length === L.height && L.tiles.every((r) => r.length === L.width), `${f}: tile grid ${L.width}x${L.height}`);
  ok(L.tiles.every((r) => [...r].every((c) => c === '.' || L.legend[c])), `${f}: every tile char has a legend entry`);
  const flag = L.entities.find((e) => e.type === 'flag'); ok(!!flag, `${f}: has a flag`);
  ok(L.entities.filter((e) => e.type === 'chip' && e.fact !== 'qc').length === 3, `${f}: 3 data chips`);
  ok(typeof L.nisar.realFactCm === 'number' && L.radar, `${f}: real NISAR number + radar map`);
  // reachability: standable cells; jumps reach 4 columns on the level or down, 3 columns when going up 1-2 rows
  const tm = Engine.createTileMap(L), solid = (x, y) => tm.isSolid(x, y) && x >= 0 && x < L.width;
  const stand = (x, y) => solid(x, y + 1) && !solid(x, y) && !solid(x, y - 1);
  const start = [L.spawn.x, L.spawn.y + 1]; while (!stand(start[0], start[1]) && start[1] < L.height) start[1]++;
  ok(stand(start[0], start[1]), `${f}: spawn stands on ground`);
  const seen = new Set([start.join(',')]), q = [start];
  while (q.length) { const [x, y] = q.shift();
    for (let dx = -4; dx <= 4; dx++) for (let dy = -2; dy <= 8; dy++) { const nx = x + dx, ny = y + dy, k = nx + ',' + ny;
      if (Math.abs(dx) === 4 && dy < 0) continue;   // engine: ~3.8 tiles across on the level, ~2.2 up
      if (!seen.has(k) && nx >= 0 && nx < L.width && ny >= 0 && ny < L.height && stand(nx, ny)) { seen.add(k); q.push([nx, ny]); } } }
  ok([...seen].some((k) => { const [x, y] = k.split(',').map(Number); return Math.abs(x - flag.x) <= 1 && Math.abs(y - flag.y) <= 1; }), `${f}: flag reachable from spawn`);
  const items = L.entities.filter((e) => ['pump', 'crop', 'chip'].includes(e.type));
  const unreachable = items.filter((e) => ![...seen].some((k) => { const [x, y] = k.split(',').map(Number); return Math.abs(x - e.x) <= 1 && y - e.y >= -1 && y - e.y <= 3; /* jump apex reaches ~3 rows above the feet */ }));
  ok(unreachable.length === 0, `${f}: every pump/crop/chip reachable (${unreachable.map((e) => e.type + '@' + e.x).join(' ')})`);
  console.log(`${f}: ${L.width} cols, pumps ${L.entities.filter((e) => e.type === 'pump').length}, crops ${L.entities.filter((e) => e.type === 'crop').length}, reachable cells ${seen.size}`);
}
console.log(fail ? `test_systems.js: ${fail} FAILED` : 'test_systems.js: all checks passed');
process.exit(fail ? 1 : 0);
