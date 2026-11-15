(function () {
  'use strict';

  var LEVELS = [
    { id: 'tulare', name: '1. Tulare Basin, California', biome: 'tulare', lon: -119.3, lat: 36.2, rate: '-10.1 cm', radarUrl: '../data/central_valley/disp/2026-10-14.png' },
    { id: 'eloy', name: '2. Eloy, Arizona', biome: 'eloy', lon: -111.5, lat: 32.7, rate: '-8.4 cm', radarUrl: '../data/global/eloy/disp/2026-10-17.png' },
    { id: 'konya', name: '3. Karapinar, Konya', biome: 'konya', lon: 33.5, lat: 37.7, rate: '-3.8 cm', radarUrl: '../data/karapinar/disp/2026-10-12.png' },
    { id: 'mexico', name: '4. Mexico City, Mexico', biome: 'mexico', lon: -99.1, lat: 19.4, rate: '-4.9 cm', radarUrl: '../data/global/mexico_city/disp/2026-10-20.png' }
  ];

  var STORAGE_KEY = 'aquifer_run_progress_v1';
  var SETTINGS_KEY = 'aquifer_run_settings_v1';

  var canvas = document.getElementById('gameCanvas');
  var ctx = canvas.getContext('2d');
  ctx.imageSmoothingEnabled = false;

  var Engine = window.RunEngine;
  var Player = window.RunPlayer;
  var T = Engine.SCALED_TILE;

  // Settings
  var settings = { sound: true, reducedMotion: false };
  try {
    var savedSet = JSON.parse(localStorage.getItem(SETTINGS_KEY) || 'null');
    if (savedSet) {
      settings.sound = savedSet.sound !== false;
      settings.reducedMotion = !!savedSet.reducedMotion;
    }
  } catch (e) {}
  function saveSettings() {
    try { localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings)); } catch (e) {}
  }

  // Progress
  function loadProgress() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}') || {};
    } catch (e) { return {}; }
  }
  function saveLevelStars(levelId, stars) {
    var prog = loadProgress();
    var prev = prog[levelId] || 0;
    if (stars > prev) {
      prog[levelId] = stars;
      try { localStorage.setItem(STORAGE_KEY, JSON.stringify(prog)); } catch (e) {}
    }
  }
  function isUnlocked(idx) {
    if (idx === 0) return true;
    var prog = loadProgress();
    return (prog[LEVELS[idx - 1].id] || 0) > 0;
  }

  // Minimal Web Audio synth (no external files)
  var audioCtx = null;
  function beep(freq, dur, type, vol) {
    if (!settings.sound) return;
    try {
      if (!audioCtx) {
        var AC = window.AudioContext || window.webkitAudioContext;
        if (!AC) return;
        audioCtx = new AC();
      }
      if (audioCtx.state === 'suspended') audioCtx.resume();
      var osc = audioCtx.createOscillator();
      var gain = audioCtx.createGain();
      osc.type = type || 'square';
      osc.frequency.value = freq;
      gain.gain.setValueAtTime(vol || 0.06, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + (dur || 0.1));
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + (dur || 0.1));
    } catch (e) {}
  }

  // Touch controls
  var input = Engine.createInput();
  if (window.matchMedia && window.matchMedia('(pointer: coarse)').matches) {
    document.body.classList.add('has-touch');
  }
  window.addEventListener('touchstart', function () {
    document.body.classList.add('has-touch');
  }, { once: true, passive: true });

  var touchBtns = document.querySelectorAll('.t-btn[data-key]');
  for (var i = 0; i < touchBtns.length; i++) {
    (function (btn) {
      var key = btn.getAttribute('data-key');
      function down(e) { e.preventDefault(); btn.classList.add('active'); input.setTouch(key, true); }
      function up(e) { e.preventDefault(); btn.classList.remove('active'); input.setTouch(key, false); }
      btn.addEventListener('touchstart', down, { passive: false });
      btn.addEventListener('touchend', up, { passive: false });
      btn.addEventListener('touchcancel', up, { passive: false });
      btn.addEventListener('mousedown', down);
      btn.addEventListener('mouseup', up);
      btn.addEventListener('mouseleave', up);
    })(touchBtns[i]);
  }

  // Fallback level if JSON is not yet available
  function makeFallbackLevel(meta) {
    var w = 60, h = 12;
    var rows = [];
    for (var y = 0; y < h; y++) {
      var r = '';
      for (var x = 0; x < w; x++) {
        if (y === 9) r += (x >= 20 && x <= 23) ? 'S' : 'G';
        else if (y > 9) r += 'D';
        else r += '.';
      }
      rows.push(r);
    }
    return {
      id: meta.id, name: meta.name, biome: meta.biome,
      width: w, height: h, tiles: rows,
      legend: { G: 'grass', D: 'dirt', S: 'sink1' },
      entities: [
        { type: 'drop', x: 8, y: 8 },
        { type: 'pump', x: 14, y: 8 },
        { type: 'crop', x: 18, y: 8 },
        { type: 'chip', x: 26, y: 7, fact: meta.id + '-1' },
        { type: 'checkpoint', x: 30, y: 8 },
        { type: 'flag', x: 54, y: 8 }
      ],
      aquifer: { start: 70, redLine: 40, drainPerPump: 0.9, rainRefill: 4, rainEverySec: 0 },
      nisar: { scanEverySec: 25, realFactCm: -7.8, realFactText: 'NISAR 2026 provisional measurement.' }
    };
  }

  var scenes = Engine.createSceneManager();
  var activeLevel = null; // holds current level runtime

  // --- TITLE SCENE ---
  var titleTime = 0;
  scenes.register('title', {
    enter: function () { titleTime = 0; },
    update: function (dt, inp) {
      titleTime += dt;
      if (inp.jumpPressed || inp.actionPressed) {
        beep(520, 0.1, 'triangle');
        scenes.go('map');
      }
    },
    draw: function (c) {
      if (window.RunArt && window.RunArt.title) {
        window.RunArt.title(c, Engine.VIEW_W, Engine.VIEW_H, titleTime);
      } else {
        c.fillStyle = '#0b1320';
        c.fillRect(0, 0, Engine.VIEW_W, Engine.VIEW_H);
        c.fillStyle = '#38bdf8';
        c.font = 'bold 48px monospace';
        c.textAlign = 'center';
        c.fillText('AQUIFER RUN', Engine.VIEW_W / 2, 200);
        c.fillStyle = '#e6edf3';
        c.font = '20px sans-serif';
        c.fillText('NISAR Vision · Follow the Water', Engine.VIEW_W / 2, 250);
      }
      c.fillStyle = '#f59e0b';
      c.font = 'bold 20px monospace';
      c.textAlign = 'center';
      if (Math.floor(titleTime * 2) % 2 === 0) {
        c.fillText('PRESS SPACE / JUMP TO START', Engine.VIEW_W / 2, 430);
      }
      c.textAlign = 'left';
    }
  });

  // --- MAP SCENE ---
  var mapIdx = 0;
  var mapCooldown = 0;
  scenes.register('map', {
    enter: function () { mapCooldown = 0.15; },
    update: function (dt, inp) {
      mapCooldown = Math.max(0, mapCooldown - dt);
      if (mapCooldown <= 0) {
        if (inp.left && mapIdx > 0) { mapIdx--; mapCooldown = 0.18; beep(360, 0.05); }
        if (inp.right && mapIdx < LEVELS.length - 1) { mapIdx++; mapCooldown = 0.18; beep(400, 0.05); }
      }
      if ((inp.jumpPressed || inp.actionPressed) && isUnlocked(mapIdx)) {
        beep(600, 0.12, 'triangle');
        startLevel(mapIdx);
      }
    },
    draw: function (c) {
      var prog = loadProgress();
      if (window.RunArt && window.RunArt.worldMap) {
        var pins = LEVELS.map(function (lv, idx) {
          return {
            id: lv.id,
            name: lv.name,
            lon: lv.lon,
            lat: lv.lat,
            rate: lv.rate,
            stars: prog[lv.id] || 0,
            locked: !isUnlocked(idx)
          };
        });
        window.RunArt.worldMap(c, Engine.VIEW_W, Engine.VIEW_H, titleTime, pins, mapIdx);
        return;
      }
      c.fillStyle = '#0f172a';
      c.fillRect(0, 0, Engine.VIEW_W, Engine.VIEW_H);
      c.fillStyle = '#e6edf3';
      c.font = 'bold 30px monospace';
      c.textAlign = 'center';
      c.fillText('SELECT A SINKING VALLEY', Engine.VIEW_W / 2, 74);

      for (var k = 0; k < LEVELS.length; k++) {
        var bx = 70 + k * 212;
        var by = 150;
        var bw = 188;
        var bh = 230;
        var unlocked = isUnlocked(k);
        var selected = k === mapIdx;
        if (window.RunArt && window.RunArt.card) {
          window.RunArt.card(c, bx, by, bw, bh);
        } else {
          c.fillStyle = selected ? '#1e293b' : '#111827';
          c.fillRect(bx, by, bw, bh);
        }
        c.strokeStyle = selected ? '#38bdf8' : '#334155';
        c.lineWidth = selected ? 4 : 2;
        c.strokeRect(bx, by, bw, bh);

        c.fillStyle = unlocked ? '#f8fafc' : '#64748b';
        c.font = 'bold 16px sans-serif';
        c.textAlign = 'center';
        c.fillText(LEVELS[k].name.split(',')[0], bx + bw / 2, by + 56);
        c.font = '13px sans-serif';
        c.fillStyle = '#94a3b8';
        c.fillText(LEVELS[k].name.split(',')[1] || '', bx + bw / 2, by + 80);

        var stars = prog[LEVELS[k].id] || 0;
        c.font = '24px monospace';
        c.fillStyle = '#f59e0b';
        var starStr = '';
        for (var s = 0; s < 3; s++) starStr += s < stars ? '★' : '☆';
        c.fillText(unlocked ? starStr : 'LOCKED', bx + bw / 2, by + 150);
      }

      c.fillStyle = '#94a3b8';
      c.font = '16px monospace';
      c.fillText('← / → SELECT · SPACE / ACTION TO PLAY', Engine.VIEW_W / 2, 460);
      c.textAlign = 'left';
    }
  });

  function startLevel(idx) {
    var meta = LEVELS[idx];
    fetch('levels/' + meta.id + '.json')
      .then(function (r) { if (!r.ok) throw new Error('missing'); return r.json(); })
      .catch(function () { return makeFallbackLevel(meta); })
      .then(function (json) {
        scenes.go('level', { idx: idx, json: json });
      });
  }

  // --- LEVEL SCENE ---
  scenes.register('level', {
    enter: function (payload) {
      var json = payload.json;
      var tileMap = Engine.createTileMap(json);
      var sysState = window.RunSystems && window.RunSystems.createLevelState
        ? window.RunSystems.createLevelState(json)
        : { tank: 4, tankMax: 10, aquifer: 70, redLine: 40, score: 0, chips: 0, aquiferHistory: [70] };

      var entities = (json.entities || []).map(function (e, i) {
        return {
          id: i,
          type: e.type,
          x: e.x * T,
          y: e.y * T,
          startX: e.x * T,
          w: T,
          h: T,
          range: (e.range || 4) * T,
          dir: 1,
          fact: e.fact || null,
          line: e.line || '',
          active: true,
          off: false,
          watered: false,
          calmed: false
        };
      });

      var spawnX = 2 * T;
      var spawnY = 6 * T;
      var player = Player.createPlayer(spawnX, spawnY);
      var camera = Engine.createCamera(Engine.VIEW_W, Engine.VIEW_H);

      activeLevel = {
        idx: payload.idx,
        json: json,
        tileMap: tileMap,
        sysState: sysState,
        entities: entities,
        player: player,
        camera: camera,
        time: 0,
        scanTimer: (json.nisar && json.nisar.scanEverySec) || 25,
        scanActive: 0,
        toast: '',
        toastTimer: 0
      };
    },
    update: function (dt, inp) {
      if (!activeLevel) return;
      if (inp.pausePressed) {
        scenes.go('pause');
        return;
      }

      var L = activeLevel;
      L.time += dt;
      if (L.toastTimer > 0) L.toastTimer = Math.max(0, L.toastTimer - dt);

      // NISAR radar scan
      L.scanTimer -= dt;
      if (L.scanTimer <= 0) {
        L.scanTimer = (L.json.nisar && L.json.nisar.scanEverySec) || 25;
        L.scanActive = 3.0;
        beep(740, 0.08, 'sine');
      }
      if (L.scanActive > 0) L.scanActive = Math.max(0, L.scanActive - dt);

      var pRes = Player.updatePlayer(L.player, inp, L.tileMap, dt, Engine);
      if (pRes.jumped) beep(420, 0.08, 'square');

      var events = [];

      // Pit fall
      if (L.player.y > L.tileMap.pixelHeight + 48) {
        L.player.hearts -= 1;
        beep(160, 0.2, 'sawtooth');
        events.push({ type: 'fall' });
        if (L.player.hearts <= 0) {
          startLevel(L.idx);
          return;
        }
        L.player.x = L.player.checkpointX;
        L.player.y = L.player.checkpointY;
        L.player.vx = 0;
        L.player.vy = 0;
        L.player.invulnTimer = 1.2;
        L.camera.triggerShake(5, 0.25);
      }

      // Entity collisions & interactions
      for (var i = 0; i < L.entities.length; i++) {
        var ent = L.entities[i];
        if (!ent.active) continue;

        if (ent.type === 'dust' && !ent.calmed) {
          ent.x += ent.dir * 85 * dt;
          if (ent.x > ent.startX + ent.range) ent.dir = -1;
          if (ent.x < ent.startX - ent.range) ent.dir = 1;
        }

        var overlap = L.player.x < ent.x + ent.w && L.player.x + L.player.w > ent.x &&
                      L.player.y < ent.y + ent.h && L.player.y + L.player.h > ent.y;

        if (overlap) {
          if (ent.type === 'drop' || ent.type === 'chip') {
            ent.active = false;
            beep(ent.type === 'chip' ? 880 : 660, 0.1, 'triangle');
            events.push({ type: 'pickup', target: ent.type, fact: ent.fact });
            if (ent.type === 'chip') {
              L.toast = 'Data chip collected!';
              L.toastTimer = 2.5;
            }
          } else if (ent.type === 'checkpoint') {
            L.player.checkpointX = ent.x;
            L.player.checkpointY = ent.y - L.player.h + T;
            ent.active = false;
            beep(580, 0.1, 'sine');
            L.toast = 'Checkpoint saved';
            L.toastTimer = 1.8;
          } else if (ent.type === 'dust' && !ent.calmed) {
            if (inp.actionPressed) {
              ent.calmed = true;
              beep(500, 0.12, 'triangle');
              events.push({ type: 'action', target: 'dust' });
            } else if (L.player.invulnTimer <= 0) {
              L.player.invulnTimer = 1.0;
              L.camera.triggerShake(4, 0.2);
              beep(200, 0.15, 'sawtooth');
              events.push({ type: 'dustHit' });
            }
          } else if (ent.type === 'flag') {
            events.push({ type: 'reachFlag' });
            beep(784, 0.15, 'triangle');
            if (window.RunSystems && window.RunSystems.update) {
              window.RunSystems.update(L.sysState, dt, events);
            }
            var reportData = window.RunSystems && window.RunSystems.score
              ? window.RunSystems.score(L.sysState)
              : { score: L.sysState.score || 500, stars: [true, true, false], report: { cmSunk: 0, realFactCm: (L.json.nisar && L.json.nisar.realFactCm) || -7.8, realFactText: (L.json.nisar && L.json.nisar.realFactText) || '' } };
            var starCount = (reportData.stars || []).filter(Boolean).length;
            saveLevelStars(L.json.id, starCount);
            scenes.go('report', { levelIdx: L.idx, json: L.json, result: reportData });
            return;
          } else if (inp.actionPressed) {
            if (ent.type === 'pump' && !ent.off) {
              ent.off = true;
              beep(320, 0.12, 'square');
              events.push({ type: 'action', target: 'pump', entity: ent });
              L.toast = 'Pump switched OFF';
              L.toastTimer = 2.0;
            } else if (ent.type === 'crop' && !ent.watered) {
              ent.watered = true;
              beep(640, 0.12, 'sine');
              events.push({ type: 'action', target: 'crop', entity: ent });
              L.toast = 'Crops watered!';
              L.toastTimer = 2.0;
            } else if (ent.type === 'farmer' && ent.line) {
              L.toast = ent.line;
              L.toastTimer = 3.5;
            }
          }
        }
      }

      if (window.RunSystems && window.RunSystems.update) {
        window.RunSystems.update(L.sysState, dt, events);
      }

      if (window.RunSystems && window.RunSystems.sinkTilesToDrop) {
        var toDrop = window.RunSystems.sinkTilesToDrop(L.sysState) || [];
        for (var d = 0; d < toDrop.length; d++) {
          var st = toDrop[d];
          var curTile = L.tileMap.getTile(st.x, st.y);
          if (curTile) {
            L.tileMap.setTile(st.x, st.y, null);
            L.tileMap.setTile(st.x, st.y + 1, 'sink2');
            L.camera.triggerShake(3, 0.18);
          }
        }
      }

      L.camera.update(L.player, L.tileMap, dt, settings.reducedMotion);
    },
    draw: function (c) {
      if (!activeLevel) return;
      var L = activeLevel;
      var shakeX = L.camera.shakeTime > 0 ? (Math.random() - 0.5) * L.camera.shakeMag * 2 : 0;
      var shakeY = L.camera.shakeTime > 0 ? (Math.random() - 0.5) * L.camera.shakeMag * 2 : 0;
      var cx = Math.round(L.camera.x + shakeX);
      var cy = Math.round(L.camera.y + shakeY);

      if (window.RunArt && window.RunArt.drawBackground) {
        window.RunArt.drawBackground(c, L.json.biome || 'tulare', cx, Engine.VIEW_W, Engine.VIEW_H, L.time);
      } else {
        c.fillStyle = '#0ea5e9';
        c.fillRect(0, 0, Engine.VIEW_W, Engine.VIEW_H);
      }

      // Draw visible tiles
      var startCol = Math.max(0, Math.floor(cx / T));
      var endCol = Math.min(L.tileMap.width - 1, Math.ceil((cx + Engine.VIEW_W) / T));
      var startRow = Math.max(0, Math.floor(cy / T));
      var endRow = Math.min(L.tileMap.height - 1, Math.ceil((cy + Engine.VIEW_H) / T));

      for (var y = startRow; y <= endRow; y++) {
        for (var x = startCol; x <= endCol; x++) {
          var tName = L.tileMap.getTile(x, y);
          if (!tName) continue;
          var sx = x * T - cx;
          var sy = y * T - cy;
          if (window.RunArt && window.RunArt.drawTile) {
            window.RunArt.drawTile(c, tName, sx, sy);
          } else {
            c.fillStyle = tName.indexOf('sink') === 0 ? '#b45309' : (tName === 'grass' ? '#16a34a' : '#78350f');
            c.fillRect(sx, sy, T, T);
          }
          if (L.scanActive > 0 && tName.indexOf('sink') === 0) {
            c.strokeStyle = '#ef4444';
            c.lineWidth = 3;
            c.strokeRect(sx + 2, sy + 2, T - 4, T - 4);
          }
        }
      }

      // Draw entities
      for (var i = 0; i < L.entities.length; i++) {
        var ent = L.entities[i];
        if (!ent.active) continue;
        var ex = Math.round(ent.x - cx);
        var ey = Math.round(ent.y - cy);
        if (ex < -T || ex > Engine.VIEW_W + T) continue;
        var frame = Math.floor(L.time * 6) % 4;
        var spriteName = ent.type;
        if (ent.type === 'pump') spriteName = ent.off ? 'pump_off' : 'pump_on';
        else if (ent.type === 'crop') spriteName = ent.watered ? 'crop_green' : 'crop_dry';
        else if (ent.type === 'dust') spriteName = 'dust_devil';

        if (window.RunArt && window.RunArt.drawSprite) {
          window.RunArt.drawSprite(c, spriteName, frame % 2, ex, ey, false);
        } else {
          c.fillStyle = ent.type === 'flag' ? '#22c55e' : (ent.type === 'pump' ? (ent.off ? '#64748b' : '#ef4444') : '#facc15');
          c.fillRect(ex + 8, ey + 8, T - 16, T - 16);
        }
      }

      Player.drawPlayer(c, L.player, cx, cy);

      if (L.scanActive > 0 && !settings.reducedMotion && window.RunArt && window.RunArt.radarSweep) {
        window.RunArt.radarSweep(c, Engine.VIEW_W, Engine.VIEW_H, 1 - (L.scanActive / 3.0), L.json.biome || 'tulare');
      }

      // HUD
      var info = window.RunSystems && window.RunSystems.aquiferInfo
        ? window.RunSystems.aquiferInfo(L.sysState)
        : { value: L.sysState.aquifer || 70, redLine: 40 };
      var hudState = {
        tank: L.sysState.tank || 0,
        tankMax: L.sysState.tankMax || 10,
        aquifer: info.value,
        redLine: info.redLine,
        hearts: L.player.hearts,
        chips: L.sysState.chips || 0,
        score: L.sysState.score || 0,
        level: L.json.name
      };
      if (window.RunArt && window.RunArt.hud) {
        window.RunArt.hud(c, hudState, Engine.VIEW_W, Engine.VIEW_H);
      } else {
        c.fillStyle = 'rgba(11, 15, 20, 0.78)';
        c.fillRect(0, 0, Engine.VIEW_W, 44);
        c.fillStyle = '#e6edf3';
        c.font = 'bold 15px monospace';
        c.fillText('AQUIFER: ' + Math.round(hudState.aquifer) + '% (RED: ' + hudState.redLine + '%) | TANK: ' + hudState.tank + '/' + hudState.tankMax + ' | HEARTS: ' + hudState.hearts + ' | SCORE: ' + hudState.score, 18, 27);
      }

      if (L.toastTimer > 0 && L.toast) {
        c.fillStyle = 'rgba(15, 23, 42, 0.88)';
        c.fillRect(Engine.VIEW_W / 2 - 220, 62, 440, 38);
        c.strokeStyle = '#38bdf8';
        c.lineWidth = 2;
        c.strokeRect(Engine.VIEW_W / 2 - 220, 62, 440, 38);
        c.fillStyle = '#f8fafc';
        c.font = 'bold 16px sans-serif';
        c.textAlign = 'center';
        c.fillText(L.toast, Engine.VIEW_W / 2, 87);
        c.textAlign = 'left';
      }
    }
  });

  // --- PAUSE SCENE ---
  var pauseOpt = 0;
  var pauseTimer = 0;
  scenes.register('pause', {
    enter: function () { pauseOpt = 0; pauseTimer = 0.15; },
    update: function (dt, inp) {
      pauseTimer = Math.max(0, pauseTimer - dt);
      if (inp.pausePressed && pauseTimer <= 0) {
        scenes.go('level', null); // resume without re-entering
        return;
      }
      if (inp.jumpPressed || inp.actionPressed) {
        if (pauseOpt === 0) scenes.go('level', null);
        else if (pauseOpt === 1) { settings.sound = !settings.sound; saveSettings(); }
        else if (pauseOpt === 2) { settings.reducedMotion = !settings.reducedMotion; saveSettings(); }
        else if (pauseOpt === 3) { startLevel(activeLevel.idx); }
        else if (pauseOpt === 4) { scenes.go('map'); }
      }
      if (pauseTimer <= 0 && (inp.left || inp.right)) {
        pauseOpt = (pauseOpt + (inp.right ? 1 : 4)) % 5;
        pauseTimer = 0.18;
      }
    },
    draw: function (c) {
      c.fillStyle = 'rgba(11, 15, 20, 0.9)';
      c.fillRect(0, 0, Engine.VIEW_W, Engine.VIEW_H);
      c.fillStyle = '#38bdf8';
      c.font = 'bold 34px monospace';
      c.textAlign = 'center';
      c.fillText('PAUSED', Engine.VIEW_W / 2, 130);

      var items = [
        'Resume Game',
        'Sound: ' + (settings.sound ? 'ON' : 'OFF'),
        'Reduced Motion: ' + (settings.reducedMotion ? 'ON' : 'OFF'),
        'Restart Level',
        'Back to Valley Map'
      ];
      for (var i = 0; i < items.length; i++) {
        c.fillStyle = i === pauseOpt ? '#f59e0b' : '#e6edf3';
        c.font = (i === pauseOpt ? 'bold ' : '') + '22px monospace';
        c.fillText((i === pauseOpt ? '▶ ' : '  ') + items[i], Engine.VIEW_W / 2, 210 + i * 48);
      }
      c.fillStyle = '#94a3b8';
      c.font = '14px monospace';
      c.fillText('← / → CHOOSE · SPACE / ACTION SELECT · P / ESC RESUME', Engine.VIEW_W / 2, 480);
      c.textAlign = 'left';
    }
  });

  // Override pause resume so it doesn't wipe activeLevel
  var origGo = scenes.go;
  scenes.go = function (name, payload) {
    if (name === 'level' && payload === null && activeLevel) {
      // resume existing level without calling enter()
      var prevEnter = null;
      origGo('level', activeLevel.json ? { idx: activeLevel.idx, json: activeLevel.json } : payload);
      return;
    }
    origGo(name, payload);
  };

  // --- REPORT CARD SCENE ---
  var reportPayload = null;
  scenes.register('report', {
    enter: function (payload) { reportPayload = payload; },
    update: function (dt, inp) {
      if (inp.jumpPressed || inp.actionPressed) {
        scenes.go('map');
      }
    },
    draw: function (c) {
      c.fillStyle = '#0b1320';
      c.fillRect(0, 0, Engine.VIEW_W, Engine.VIEW_H);
      if (!reportPayload) return;
      var res = reportPayload.result;
      var stars = (res.stars || []).filter(Boolean).length;
      c.fillStyle = '#38bdf8';
      c.font = 'bold 32px monospace';
      c.textAlign = 'center';
      c.fillText('VALLEY REPORT CARD: ' + reportPayload.json.name.toUpperCase(), Engine.VIEW_W / 2, 85);

      c.fillStyle = '#f59e0b';
      c.font = '44px monospace';
      var starStr = '';
      for (var s = 0; s < 3; s++) starStr += s < stars ? '★' : '☆';
      c.fillText(starStr, Engine.VIEW_W / 2, 155);

      c.fillStyle = '#e6edf3';
      c.font = '22px monospace';
      c.fillText('SCORE: ' + (res.score || 0), Engine.VIEW_W / 2, 210);
      var rep = res.report || {};
      c.fillText('PERMANENT SINKING IN LEVEL: ' + (rep.cmSunk || 0) + ' cm', Engine.VIEW_W / 2, 255);
      c.fillStyle = '#7dd3fc';
      c.font = '18px sans-serif';
      c.fillText('REAL NISAR MEASUREMENT: ' + (rep.realFactText || (rep.realFactCm + ' cm')), Engine.VIEW_W / 2, 315);

      c.fillStyle = '#94a3b8';
      c.font = '13px sans-serif';
      c.fillText('NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.', Engine.VIEW_W / 2, 410);
      c.fillStyle = '#f59e0b';
      c.font = 'bold 18px monospace';
      c.fillText('PRESS SPACE / ACTION FOR VALLEY MAP', Engine.VIEW_W / 2, 475);
      c.textAlign = 'left';
    }
  });

  function boot() {
    if (window.RunArt && window.RunArt.loadRadar) {
      LEVELS.forEach(function (lv) {
        window.RunArt.loadRadar(lv.biome, lv.radarUrl);
      });
    }
    scenes.go('title');
    Engine.startLoop(
      function step(dt) {
        input.update();
        scenes.update(dt, input);
      },
      function render() {
        scenes.draw(ctx);
      }
    );
  }

  if (window.RunArt && window.RunArt.ready && typeof window.RunArt.ready.then === 'function') {
    window.RunArt.ready.then(boot, boot);
  } else {
    boot();
  }
})();
