'use strict';

const assert = require('assert');
const Engine = require('./engine.js');
const Player = require('./player.js');

const T = Engine.SCALED_TILE; // 48

function makeTestLevel() {
  // 12x8 grid: row 6 is solid grass, col 8 has a 2-tile wall at rows 4..5
  const rows = [
    '............',
    '............',
    '............',
    '............',
    '........#...',
    '........#...',
    'GGGGGGGGGGGG',
    'DDDDDDDDDDDD'
  ];
  return Engine.createTileMap({
    width: 12,
    height: 8,
    tiles: rows,
    legend: { G: 'grass', D: 'dirt', '#': 'rock' }
  });
}

function emptyInput() {
  return { left: false, right: false, jump: false, jumpPressed: false, action: false, actionPressed: false };
}

// 1. Ground collision (settling onto floor)
{
  const map = makeTestLevel();
  const p = Player.createPlayer(2 * T, 4 * T); // above floor at row 6 (y = 288)
  const inp = emptyInput();
  for (let i = 0; i < 60; i++) {
    Player.updatePlayer(p, inp, map, Engine.FIXED_DT, Engine);
  }
  assert.strictEqual(p.onGround, true, 'Player should settle onto ground');
  assert.strictEqual(p.y + p.h, 6 * T, 'Player feet should rest exactly on row 6 top');
  assert.strictEqual(p.vy, 0, 'Vertical velocity should zero out on ground');
}

// 2. Wall collision (cannot pass through solid wall at col 8)
{
  const map = makeTestLevel();
  const p = Player.createPlayer(6 * T, 6 * T - 64);
  const inp = emptyInput();
  inp.right = true;
  for (let i = 0; i < 90; i++) {
    Player.updatePlayer(p, inp, map, Engine.FIXED_DT, Engine);
  }
  assert.strictEqual(p.hitWall, true, 'Player should hit wall at col 8');
  assert.ok(p.x + p.w <= 8 * T + 0.001, 'Player must not pass through col 8 wall');
}

// 3. Jump height range (full hold vs tap)
{
  const map = makeTestLevel();
  const startY = 6 * T - 64;

  // Full hold jump
  const pHold = Player.createPlayer(2 * T, startY);
  pHold.onGround = true;
  let minYHold = startY;
  for (let i = 0; i < 40; i++) {
    const inp = emptyInput();
    inp.jump = true;
    inp.jumpPressed = (i === 0);
    Player.updatePlayer(pHold, inp, map, Engine.FIXED_DT, Engine);
    if (pHold.y < minYHold) minYHold = pHold.y;
  }
  const heightHold = startY - minYHold;
  assert.ok(heightHold >= 80 && heightHold <= 140, `Full jump height ${heightHold.toFixed(1)}px should be in 80..140px`);

  // Short tap jump
  const pTap = Player.createPlayer(2 * T, startY);
  pTap.onGround = true;
  let minYTap = startY;
  for (let i = 0; i < 40; i++) {
    const inp = emptyInput();
    inp.jump = (i < 2);
    inp.jumpPressed = (i === 0);
    Player.updatePlayer(pTap, inp, map, Engine.FIXED_DT, Engine);
    if (pTap.y < minYTap) minYTap = pTap.y;
  }
  const heightTap = startY - minYTap;
  assert.ok(heightTap < heightHold, `Tap jump (${heightTap.toFixed(1)}px) must be lower than hold jump (${heightHold.toFixed(1)}px)`);
}

// 4. Coyote time (can jump within 0.1s after walking off ledge)
{
  const map = makeTestLevel();
  const p = Player.createPlayer(2 * T, 6 * T - 64);
  p.onGround = true;
  // Step 1: prime coyote timer on ground
  Player.updatePlayer(p, emptyInput(), map, Engine.FIXED_DT, Engine);
  // Step 2: move player into air for 3 frames (~0.05s < 0.1s coyote)
  p.onGround = false;
  p.y -= 4;
  for (let i = 0; i < 3; i++) {
    // keep in air (no floor contact)
    p.y = 2 * T;
    Player.updatePlayer(p, emptyInput(), map, Engine.FIXED_DT, Engine);
  }
  assert.ok(p.coyoteTimer > 0, 'Coyote timer should still be active after 0.05s in air');
  const inp = emptyInput();
  inp.jump = true;
  inp.jumpPressed = true;
  const res = Player.updatePlayer(p, inp, map, Engine.FIXED_DT, Engine);
  assert.strictEqual(res.jumped, true, 'Player should be able to jump during coyote time');
}

console.log('test_engine.js: all 4 engine & player assertions PASSED');
