'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const Systems = require('./systems.js');
const levelsDir = path.join(__dirname, 'levels');
const facts = require('./facts.json');
const atlas = require('../../data/global/atlas.json');
const home = require('../../data/global/home_summary.json');

function loadLevels() {
  return fs.readdirSync(levelsDir).filter((name) => name.endsWith('.json'))
    .map((name) => JSON.parse(fs.readFileSync(path.join(levelsDir, name), 'utf8')));
}

function testAquiferAndEvents() {
  const level = {
    id: 'test',
    aquifer: { start: 70, redLine: 40, drainPerPump: 1, rainRefill: 4 },
    entities: [
      { type: 'pump', x: 3 }, { type: 'pump', x: 20 },
      { type: 'crop', x: 4 }, { type: 'drop' }
    ],
    legend: { S: 'sink1' },
    tiles: ['.....', '...S.'],
    nisar: { realFactCm: -1, realFactText: 'test', sinkTiles: [{ x: 3, y: 1 }] }
  };
  const state = Systems.createLevelState(level);
  Systems.update(state, 1, []);
  assert.strictEqual(state.aquifer, 68, 'each running pump drains its configured amount each second');
  Systems.update(state, 1, [{ type: 'action', target: 'pump', entity: { id: 0 } }]);
  assert.strictEqual(state.pumpsRunning, 1, 'switching a pump off stops its drain');
  assert.strictEqual(state.score, 150, 'switching off a pump awards points');
  const beforeDrop = state.aquifer;
  Systems.update(state, 0.01, [{ type: 'pickup', target: 'drop' }]);
  assert.strictEqual(state.tank, 5, 'a rain drop refills the tank');
  assert(state.aquifer >= beforeDrop + 3.9, 'a rain drop refills the aquifer');
  assert.strictEqual(state.score, 160, 'a rain drop awards points');
  Systems.update(state, 0.01, [{ type: 'action', target: 'crop', entity: { id: 2 } }]);
  assert.strictEqual(state.tank, 3, 'watering a crop uses two tank units');
  assert.strictEqual(state.crops, 1, 'watering a crop is recorded');
  assert.strictEqual(state.score, 410, 'watering and the farmer pump action award points');
  assert.strictEqual(state.pumpsRunning, 0, 'watering lets the farmer switch off the nearest pump');
  Systems.update(state, 0.01, [{ type: 'pickup', target: 'chip' }]);
  assert.strictEqual(state.chips, 1);
  assert.strictEqual(state.score, 710, 'a data chip awards points');
  Systems.update(state, 0.01, [{ type: 'dustHit' }]);
  assert.strictEqual(state.tank, 0, 'a dust devil hit removes three tank units');

  state.aquifer = state.redLine - 1;
  Systems.update(state, 2.1, []);
  assert.strictEqual(state.permanentTiles, 1, 'one tile sinks after two seconds below the red line');
  const dropped = Systems.sinkTilesToDrop(state);
  assert.deepStrictEqual(dropped, [{ x: 3, y: 1 }], 'NISAR-marked tile is selected first');
  assert.deepStrictEqual(Systems.sinkTilesToDrop(state), [], 'the engine receives each tile only once');
  const report = Systems.score(state);
  assert.strictEqual(report.score, 660, 'report score uses crops, pumps, drops, chips, and sinking');
  assert.strictEqual(report.report.cmSunk, 2, 'one tile represents two centimetres in the game model');
  assert.strictEqual(report.stars[0], false, 'no completion star before reaching the flag');
  Systems.update(state, 0.01, [{ type: 'reachFlag' }]);
  assert.deepStrictEqual(Systems.score(state).stars, [true, false, false]);
  assert.strictEqual(Systems.score(state).report.aquiferCurve.length > 0, true, 'the report keeps the aquifer curve');
  assert(Systems.score(state).report.calibrationNote.includes('NASA-JPL and ISRO'));
}

function testLevelsAndReachability() {
  const levels = loadLevels();
  assert.strictEqual(levels.length, 4, 'all four planned levels exist');
  const ids = new Set();
  for (const level of levels) {
    ids.add(level.id);
    assert(level.width >= 180 && level.width <= 260, `${level.id}: width is in the required range`);
    assert.strictEqual(level.height, 15, `${level.id}: height is 15 tiles`);
    assert.strictEqual(level.tiles.length, level.height, `${level.id}: row count matches height`);
    for (const [y, row] of level.tiles.entries()) {
      assert.strictEqual(row.length, level.width, `${level.id}: row ${y} matches width`);
      for (const ch of row) assert(ch === '.' || level.legend[ch], `${level.id}: tile ${ch} has a legend entry`);
    }
    const chips = level.entities.filter((entity) => entity.type === 'chip');
    assert.strictEqual(chips.length, 3, `${level.id}: has three hidden data chips`);
    assert.strictEqual(level.entities.filter((entity) => entity.type === 'checkpoint').length, 2,
      `${level.id}: has two checkpoints`);
    assert.strictEqual(level.entities.filter((entity) => entity.type === 'flag').length, 1,
      `${level.id}: has one finish flag`);
    for (const chip of chips) assert(facts[chip.fact], `${level.id}: chip references a fact card`);

    // BFS over standing surfaces; jumps span up to four tiles horizontally and three vertically.
    const walkable = new Set(['grass', 'dirt', 'clay', 'rock', 'sand', 'road', 'brick', 'sink1']);
    const surfaces = [];
    for (let y = 0; y < level.height; y++) {
      for (let x = 0; x < level.width; x++) {
        const tile = level.legend[level.tiles[y][x]];
        if (tile && walkable.has(tile)) surfaces.push({ x, y: y - 1 });
      }
    }
    const start = { x: level.spawnX || 2, y: level.height - 3 };
    const finishEntity = level.entities.find((entity) => entity.type === 'flag');
    const finish = { x: finishEntity.x, y: finishEntity.y };
    const key = (node) => `${node.x},${node.y}`;
    const visited = new Set([key(start)]);
    const queue = [start];
    while (queue.length) {
      const current = queue.shift();
      for (const next of surfaces) {
        const nodeKey = key(next);
        if (Math.abs(next.x - current.x) <= 4 && Math.abs(next.y - current.y) <= 3 && !visited.has(nodeKey)) {
          visited.add(nodeKey);
          queue.push(next);
        }
      }
    }
    assert(visited.has(key(finish)), `${level.id}: the finish is reachable with the jump limits`);
  }
  assert.deepStrictEqual([...ids].sort(), ['eloy', 'konya', 'mexico', 'tulare']);
  const tutorial = levels.find((level) => level.id === 'tulare');
  assert.deepStrictEqual(tutorial.tutorial.steps.map((step) => step.text), [
    'Collect raindrops to fill your tank.',
    'Press ACTION beside a pump to turn it off.',
    'Press ACTION to water the crop.'
  ]);
  assert.strictEqual(Object.keys(facts).length, 12, 'three sourced fact cards exist per level');
  for (const [id, fact] of Object.entries(facts)) {
    assert(fact.source === 'data/global/home_summary.json' || fact.source === 'data/global/atlas.json',
      `${id}: facts use an approved source`);
    assert.strictEqual(fact.quality, 'provisional', `${id}: source quality is labeled`);
  }
  const central = atlas.regions.find((region) => region.id === 'central_valley');
  const eloy = home.top5.find((region) => region.id === 'eloy');
  const mexico = home.top5.find((region) => region.id === 'mexico_city');
  const konya = atlas.regions.find((region) => region.id === 'karapinar');
  assert.strictEqual(levels.find((level) => level.id === 'tulare').nisar.realFactCm, central.max_cm_los);
  assert.strictEqual(levels.find((level) => level.id === 'eloy').nisar.realFactCm, eloy.rate_cm_per_100d_common);
  assert.strictEqual(levels.find((level) => level.id === 'mexico').nisar.realFactCm, mexico.rate_cm_per_100d_common);
  assert.strictEqual(levels.find((level) => level.id === 'konya').nisar.realFactCm, konya.max_cm_los);
}

testAquiferAndEvents();
testLevelsAndReachability();
console.log('Aquifer Run systems, facts, and four level reachability checks passed.');
