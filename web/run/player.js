(function (global) {
  'use strict';

  var MOVE_SPEED = 240;      // px/sec (~5 tiles/sec)
  var GROUND_ACCEL = 1800;
  var GROUND_FRICTION = 1600;
  var AIR_ACCEL = 1100;
  var AIR_FRICTION = 350;
  var GRAVITY = 1480;
  var JUMP_VEL = -560;       // reaches ~106 px (~2.2 tiles) on full hold
  var MAX_FALL = 680;
  var COYOTE_MAX = 0.1;      // 0.1 s
  var BUFFER_MAX = 0.1;      // 0.1 s

  function createPlayer(spawnX, spawnY) {
    return {
      x: spawnX,
      y: spawnY,
      w: 32,   // crisp hitbox inside 16x24*3 sprite
      h: 64,
      vx: 0,
      vy: 0,
      facing: 1,
      onGround: false,
      hitWall: false,
      coyoteTimer: 0,
      jumpBufferTimer: 0,
      actionTimer: 0,
      animTimer: 0,
      animState: 'idle',
      checkpointX: spawnX,
      checkpointY: spawnY,
      hearts: 3,
      invulnTimer: 0
    };
  }

  function updatePlayer(player, input, tileMap, dt, engine) {
    var Engine = engine || global.RunEngine;

    // Horizontal movement
    var dir = (input.right ? 1 : 0) - (input.left ? 1 : 0);
    if (dir !== 0) {
      player.facing = dir;
      var accel = player.onGround ? GROUND_ACCEL : AIR_ACCEL;
      player.vx += dir * accel * dt;
      if (player.vx > MOVE_SPEED) player.vx = MOVE_SPEED;
      if (player.vx < -MOVE_SPEED) player.vx = -MOVE_SPEED;
    } else {
      var fric = player.onGround ? GROUND_FRICTION : AIR_FRICTION;
      if (player.vx > 0) {
        player.vx = Math.max(0, player.vx - fric * dt);
      } else if (player.vx < 0) {
        player.vx = Math.min(0, player.vx + fric * dt);
      }
    }

    // Coyote time & jump buffer
    if (player.onGround) {
      player.coyoteTimer = COYOTE_MAX;
    } else {
      player.coyoteTimer = Math.max(0, player.coyoteTimer - dt);
    }

    if (input.jumpPressed) {
      player.jumpBufferTimer = BUFFER_MAX;
    } else {
      player.jumpBufferTimer = Math.max(0, player.jumpBufferTimer - dt);
    }

    var jumped = false;
    if (player.jumpBufferTimer > 0 && player.coyoteTimer > 0) {
      player.vy = JUMP_VEL;
      player.onGround = false;
      player.coyoteTimer = 0;
      player.jumpBufferTimer = 0;
      jumped = true;
    }

    // Variable jump height: release early to cut ascent
    if (!input.jump && player.vy < -180) {
      player.vy *= 0.55;
    }

    // Gravity
    player.vy = Math.min(MAX_FALL, player.vy + GRAVITY * dt);

    // Move and collide (x then y)
    Engine.moveAndCollide(player, tileMap, dt);

    // Action animation timer
    if (input.actionPressed) {
      player.actionTimer = 0.22;
    } else if (player.actionTimer > 0) {
      player.actionTimer = Math.max(0, player.actionTimer - dt);
    }

    if (player.invulnTimer > 0) {
      player.invulnTimer = Math.max(0, player.invulnTimer - dt);
    }

    // Animation state
    player.animTimer += dt;
    if (player.actionTimer > 0) {
      player.animState = 'action';
    } else if (!player.onGround) {
      player.animState = 'jump';
    } else if (Math.abs(player.vx) > 20) {
      player.animState = 'run';
    } else {
      player.animState = 'idle';
    }

    return { jumped: jumped };
  }

  function drawPlayer(ctx, player, camX, camY) {
    var sx = Math.round(player.x - camX);
    var sy = Math.round(player.y - camY);
    if (player.invulnTimer > 0 && Math.floor(player.invulnTimer * 16) % 2 === 0) {
      return;
    }
    var Art = global.RunArt;
    if (Art && Art.drawSprite) {
      var frameCount = player.animState === 'run' ? 4 : (player.animState === 'jump' ? 1 : 2);
      var frame = Math.floor(player.animTimer * 8) % frameCount;
      Art.drawSprite(ctx, 'nisa_' + player.animState, frame, sx - 8, sy - 8, player.facing < 0);
      return;
    }
    // Fallback crisp placeholder when RunArt is not loaded yet
    ctx.fillStyle = '#38bdf8';
    ctx.fillRect(sx, sy, player.w, player.h);
    ctx.fillStyle = '#f59e0b';
    ctx.fillRect(sx - 2, sy - 4, player.w + 4, 10); // ranger hat
    ctx.fillStyle = '#1d4ed8';
    var packX = player.facing >= 0 ? sx - 6 : sx + player.w - 2;
    ctx.fillRect(packX, sy + 16, 8, 22); // water tank
  }

  var RunPlayer = {
    MOVE_SPEED: MOVE_SPEED,
    GRAVITY: GRAVITY,
    JUMP_VEL: JUMP_VEL,
    COYOTE_MAX: COYOTE_MAX,
    BUFFER_MAX: BUFFER_MAX,
    createPlayer: createPlayer,
    updatePlayer: updatePlayer,
    drawPlayer: drawPlayer
  };

  global.RunPlayer = RunPlayer;
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = RunPlayer;
  }
})(typeof window !== 'undefined' ? window : globalThis);
