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

// 5. Jump buffer (pressing jump 0.05s before landing triggers jump on landing)
{
  const map = makeTestLevel();
  const p = Player.createPlayer(2 * T, 6 * T - 64 - 8); // 8px above ground
  p.vy = 200; // falling fast enough to land in ~2-3 frames
  let jumpedOnLand = false;
  for (let i = 0; i < 10; i++) {
    const inp = emptyInput();
    if (i === 0) {
      inp.jump = true;
      inp.jumpPressed = true;
    }
    const res = Player.updatePlayer(p, inp, map, Engine.FIXED_DT, Engine);
    if (res.jumped) {
      jumpedOnLand = true;
      break;
    }
  }
  assert.strictEqual(jumpedOnLand, true, 'Jump buffer should trigger jump upon landing within 0.1s');
}

// 6. Coyote time expiry (cannot jump after > 0.1s in air)
{
  const map = makeTestLevel();
  const p = Player.createPlayer(2 * T, 6 * T - 64);
  p.onGround = true;
  Player.updatePlayer(p, emptyInput(), map, Engine.FIXED_DT, Engine);
  p.onGround = false;
  for (let i = 0; i < 8; i++) { // 8 * 1/60 = 0.133s > 0.1s
    p.y = 2 * T;
    Player.updatePlayer(p, emptyInput(), map, Engine.FIXED_DT, Engine);
  }
  assert.strictEqual(p.coyoteTimer, 0, 'Coyote timer should expire after > 0.1s in air');
  const inp = emptyInput();
  inp.jump = true;
  inp.jumpPressed = true;
  const res = Player.updatePlayer(p, inp, map, Engine.FIXED_DT, Engine);
  assert.strictEqual(res.jumped, false, 'Player should NOT be able to jump after coyote time expires');
}

// 7. Gamepad mapping and edge-triggered actions
{
  const prior = Object.getOwnPropertyDescriptor(globalThis, 'navigator');
  const pressedPad = {
    axes: [-0.8],
    buttons: Array.from({ length: 16 }, (_, i) => ({ pressed: [0, 1, 9, 14].includes(i) }))
  };
  let pads = [pressedPad];
  try {
    Object.defineProperty(globalThis, 'navigator', {
      configurable: true,
      value: { getGamepads: () => pads }
    });
    const input = Engine.createInput();
    input.update();
    assert.strictEqual(input.left, true, 'left axis and D-pad map to left movement');
    assert.strictEqual(input.jump, true, 'gamepad button 0 maps to jump');
    assert.strictEqual(input.action, true, 'gamepad button 1 maps to ACTION');
    assert.strictEqual(input.pausePressed, true, 'gamepad button 9 maps to pause');
    assert.strictEqual(input.jumpPressed, true, 'first gamepad jump frame is edge-triggered');
    input.update();
    assert.strictEqual(input.jumpPressed, false, 'held gamepad jump does not retrigger');
    pads = [];
    input.update();
    pads = [pressedPad];
    input.update();
    assert.strictEqual(input.actionPressed, true, 'released then pressed ACTION creates a new edge');
  } finally {
    if (prior) Object.defineProperty(globalThis, 'navigator', prior);
    else delete globalThis.navigator;
  }
}

console.log('test_engine.js: all 7 engine & player assertions PASSED');
