(function (global) {
  'use strict';

  var TILE_SIZE = 16;
  var SCALE = 3;
  var SCALED_TILE = TILE_SIZE * SCALE; // 48 px
  var VIEW_W = 960;
  var VIEW_H = 540;
  var FIXED_DT = 1 / 60;

  var SOLID_TILES = {
    grass: true, dirt: true, clay: true, rock: true, sand: true, road: true,
    brick: true, canal: true, pipe_v: true, pipe_h: true, crate: true,
    sink1: true, sink2: true, sink3: true, sinkhole_edge: true,
    bridge: true, house_wall: true, house_roof: true
  };

  function createInput() {
    var keys = {};
    var prev = { jump: false, action: false, pause: false, left: false, right: false };
    var touch = { left: false, right: false, jump: false, action: false };

    function isDown(codes) {
      for (var i = 0; i < codes.length; i++) {
        if (keys[codes[i]]) return true;
      }
      return false;
    }

    var state = {
      left: false,
      right: false,
      jump: false,
      jumpPressed: false,
      action: false,
      actionPressed: false,
      pausePressed: false,
      setKey: function (code, down) { keys[code] = !!down; },
      setTouch: function (name, down) { touch[name] = !!down; },
      update: function () {
        var gpLeft = false, gpRight = false, gpJump = false, gpAction = false, gpPause = false;
        if (typeof navigator !== 'undefined' && navigator.getGamepads) {
          var pads = navigator.getGamepads();
          for (var i = 0; i < pads.length; i++) {
            var p = pads[i];
            if (!p) continue;
            if (p.axes && p.axes[0] < -0.35) gpLeft = true;
            if (p.axes && p.axes[0] > 0.35) gpRight = true;
            if (p.buttons) {
              if (p.buttons[14] && p.buttons[14].pressed) gpLeft = true;
              if (p.buttons[15] && p.buttons[15].pressed) gpRight = true;
              if (p.buttons[0] && p.buttons[0].pressed) gpJump = true;
              if ((p.buttons[1] && p.buttons[1].pressed) || (p.buttons[2] && p.buttons[2].pressed)) gpAction = true;
              if (p.buttons[9] && p.buttons[9].pressed) gpPause = true;
            }
          }
        }
        var l = isDown(['ArrowLeft', 'KeyA']) || touch.left || gpLeft;
        var r = isDown(['ArrowRight', 'KeyD']) || touch.right || gpRight;
        var j = isDown(['Space', 'ArrowUp', 'KeyW']) || touch.jump || gpJump;
        var a = isDown(['KeyE', 'Enter', 'KeyX']) || touch.action || gpAction;
        var ps = isDown(['KeyP', 'Escape']) || touch.pause || gpPause;

        state.left = l;
        state.right = r;
        state.jump = j;
        state.jumpPressed = j && !prev.jump;
        state.action = a;
        state.actionPressed = a && !prev.action;
        state.pausePressed = ps && !prev.pause;

        prev.left = l;
        prev.right = r;
        prev.jump = j;
        prev.action = a;
        prev.pause = ps;
      }
    };

    if (typeof window !== 'undefined') {
      window.addEventListener('keydown', function (e) {
        if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Space'].indexOf(e.code) !== -1) {
          e.preventDefault();
        }
        keys[e.code] = true;
      }, { passive: false });
      window.addEventListener('keyup', function (e) {
        keys[e.code] = false;
      });
    }
    return state;
  }

  function createTileMap(levelJson) {
    var width = levelJson.width || (levelJson.tiles && levelJson.tiles[0] ? levelJson.tiles[0].length : 0);
    var height = levelJson.height || (levelJson.tiles ? levelJson.tiles.length : 0);
    var legend = levelJson.legend || {};
    var grid = [];
    for (var y = 0; y < height; y++) {
      var row = [];
      var line = (levelJson.tiles && levelJson.tiles[y]) || '';
      for (var x = 0; x < width; x++) {
        var ch = line.charAt(x) || '.';
        row.push(legend[ch] || null);
      }
      grid.push(row);
    }

    return {
      width: width,
      height: height,
      pixelWidth: width * SCALED_TILE,
      pixelHeight: height * SCALED_TILE,
      getTile: function (tx, ty) {
        if (tx < 0 || tx >= width || ty < 0 || ty >= height) return null;
        return grid[ty][tx];
      },
      setTile: function (tx, ty, name) {
        if (tx < 0 || tx >= width || ty < 0 || ty >= height) return false;
        grid[ty][tx] = name || null;
        return true;
      },
      isSolid: function (tx, ty) {
        if (tx < 0 || tx >= width) return true; // level side walls
        if (ty < 0) return false;
        if (ty >= height) return false; // pit below map
        var t = grid[ty][tx];
        return !!(t && SOLID_TILES[t]);
      }
    };
  }

  function moveAndCollide(entity, tileMap, dt) {
    entity.onGround = false;
    entity.hitWall = false;

    // Horizontal pass
    entity.x += entity.vx * dt;
    var topTile = Math.floor(entity.y / SCALED_TILE);
    var botTile = Math.floor((entity.y + entity.h - 0.01) / SCALED_TILE);

    if (entity.vx > 0) {
      var rightTile = Math.floor((entity.x + entity.w) / SCALED_TILE);
      for (var ty = topTile; ty <= botTile; ty++) {
        if (tileMap.isSolid(rightTile, ty)) {
          entity.x = rightTile * SCALED_TILE - entity.w;
          entity.vx = 0;
          entity.hitWall = true;
          break;
        }
      }
    } else if (entity.vx < 0) {
      var leftTile = Math.floor(entity.x / SCALED_TILE);
      for (var ty2 = topTile; ty2 <= botTile; ty2++) {
        if (tileMap.isSolid(leftTile, ty2)) {
          entity.x = (leftTile + 1) * SCALED_TILE;
          entity.vx = 0;
          entity.hitWall = true;
          break;
        }
      }
    }

    // Vertical pass
    entity.y += entity.vy * dt;
    var leftCol = Math.floor((entity.x + 0.01) / SCALED_TILE);
    var rightCol = Math.floor((entity.x + entity.w - 0.01) / SCALED_TILE);

    if (entity.vy > 0) {
      var footTile = Math.floor((entity.y + entity.h) / SCALED_TILE);
      for (var tx = leftCol; tx <= rightCol; tx++) {
        if (tileMap.isSolid(tx, footTile)) {
          entity.y = footTile * SCALED_TILE - entity.h;
          entity.vy = 0;
          entity.onGround = true;
          break;
        }
      }
    } else if (entity.vy < 0) {
      var headTile = Math.floor(entity.y / SCALED_TILE);
      for (var tx2 = leftCol; tx2 <= rightCol; tx2++) {
        if (tileMap.isSolid(tx2, headTile)) {
          entity.y = (headTile + 1) * SCALED_TILE;
          entity.vy = 0;
          break;
        }
      }
    }
  }

  function createCamera(viewW, viewH) {
    return {
      x: 0,
      y: 0,
      lookAhead: 0,
      shakeTime: 0,
      shakeMag: 0,
      update: function (target, tileMap, dt, reducedMotion) {
        var desiredLook = target.facing >= 0 ? 90 : -90;
        this.lookAhead += (desiredLook - this.lookAhead) * Math.min(1, dt * 5);
        var targetX = target.x + target.w * 0.5 + this.lookAhead - viewW * 0.45;
        var targetY = target.y + target.h * 0.5 - viewH * 0.55;
        var maxX = Math.max(0, tileMap.pixelWidth - viewW);
        var maxY = Math.max(0, tileMap.pixelHeight - viewH);
        this.x += (Math.max(0, Math.min(maxX, targetX)) - this.x) * Math.min(1, dt * 8);
        this.y += (Math.max(0, Math.min(maxY, targetY)) - this.y) * Math.min(1, dt * 6);
        if (this.shakeTime > 0) {
          this.shakeTime = Math.max(0, this.shakeTime - dt);
        }
        if (reducedMotion) {
          this.shakeTime = 0;
        }
      },
      triggerShake: function (mag, dur) {
        this.shakeMag = mag || 4;
        this.shakeTime = dur || 0.25;
      }
    };
  }

  function createSceneManager() {
    var scenes = {};
    var current = null;
    var currentName = '';
    return {
      register: function (name, sceneObj) { scenes[name] = sceneObj; },
      go: function (name, payload) {
        if (current && current.exit) current.exit();
        currentName = name;
        current = scenes[name] || null;
        if (current && current.enter) current.enter(payload);
      },
      name: function () { return currentName; },
      update: function (dt, input) {
        if (current && current.update) current.update(dt, input);
      },
      draw: function (ctx) {
        if (current && current.draw) current.draw(ctx);
      }
    };
  }

  function startLoop(stepFn, renderFn) {
    var last = 0;
    var acc = 0;
    var rafId = 0;
    function frame(ts) {
      if (!last) last = ts;
      var elapsed = Math.min(0.1, (ts - last) / 1000);
      last = ts;
      acc += elapsed;
      while (acc >= FIXED_DT) {
        stepFn(FIXED_DT);
        acc -= FIXED_DT;
      }
      renderFn();
      rafId = requestAnimationFrame(frame);
    }
    rafId = requestAnimationFrame(frame);
    return function stop() { cancelAnimationFrame(rafId); };
  }

  var RunEngine = {
    TILE_SIZE: TILE_SIZE,
    SCALE: SCALE,
    SCALED_TILE: SCALED_TILE,
    VIEW_W: VIEW_W,
    VIEW_H: VIEW_H,
    FIXED_DT: FIXED_DT,
    SOLID_TILES: SOLID_TILES,
    createInput: createInput,
    createTileMap: createTileMap,
    moveAndCollide: moveAndCollide,
    createCamera: createCamera,
    createSceneManager: createSceneManager,
    startLoop: startLoop
  };

  global.RunEngine = RunEngine;
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = RunEngine;
  }
})(typeof window !== 'undefined' ? window : globalThis);
