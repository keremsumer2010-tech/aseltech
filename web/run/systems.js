(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.RunSystems = factory();
}(typeof window !== 'undefined' ? window : this, function () {
  'use strict';

  function clamp(value, min, max) { return Math.max(min, Math.min(max, value)); }
  function tileCandidates(level) {
    var out = [];
    var legend = level.legend || {};
    var tiles = level.tiles || [];
    for (var y = 0; y < tiles.length; y++) {
      for (var x = 0; x < tiles[y].length; x++) {
        if (legend[tiles[y].charAt(x)] === 'sink1') out.push({ x: x, y: y });
      }
    }
    var marked = level.nisar && level.nisar.sinkTiles || [];
    for (var i = 0; i < marked.length; i++) {
      if (!out.some(function (tile) { return tile.x === marked[i].x && tile.y === marked[i].y; })) {
        out.push({ x: marked[i].x, y: marked[i].y });
      }
    }
    return out;
  }

  function createLevelState(level) {
    var aquifer = level.aquifer || {};
    var pumps = (level.entities || []).filter(function (e) { return e.type === 'pump'; }).length;
    return {
      level: level,
      tankMax: 10,
      tank: 4,
      aquifer: Number(aquifer.start === undefined ? 70 : aquifer.start),
      redLine: Number(aquifer.redLine === undefined ? 40 : aquifer.redLine),
      drainPerPump: Number(aquifer.drainPerPump === undefined ? 0.9 : aquifer.drainPerPump),
      rainRefill: Number(aquifer.rainRefill === undefined ? 4 : aquifer.rainRefill),
      rainEverySec: Number(aquifer.rainEverySec || 0),
      rainClock: 0,
      sinkClock: 0,
      elapsed: 0,
      aquiferHistory: [],
      pumpsRunning: pumps,
      offPumps: {},
      score: 0,
      chips: 0,
      crops: 0,
      pumpsOff: 0,
      drops: 0,
      completed: false,
      wasBelowRed: false,
      permanentTiles: 0,
      sinkCandidates: tileCandidates(level),
      markedTiles: (level.nisar && level.nisar.sinkTiles || []).map(function (t) { return t.x + ',' + t.y; }),
      pendingDrops: [],
      playerX: Number(level.spawnX || 2),
      levelEnded: false
    };
  }

  function update(state, dt) {
    if (!state || !Number.isFinite(dt) || dt <= 0) return state;
    state.elapsed += dt;
    state.aquifer = clamp(state.aquifer - state.pumpsRunning * state.drainPerPump * dt, 0, 100);
    if (state.rainEverySec > 0) {
      state.rainClock += dt;
      while (state.rainClock >= state.rainEverySec) {
        state.rainClock -= state.rainEverySec;
        state.aquifer = clamp(state.aquifer + state.rainRefill, 0, 100);
      }
    }
    var below = state.aquifer < state.redLine;
    if (below) {
      state.wasBelowRed = true;
      state.sinkClock += dt;
      while (state.sinkClock >= 2) {
        state.sinkClock -= 2;
        if (state.sinkCandidates.length) {
          state.sinkCandidates.sort(function (a, b) {
            var aMarked = state.markedTiles.indexOf(a.x + ',' + a.y) >= 0 ? 0 : 1;
            var bMarked = state.markedTiles.indexOf(b.x + ',' + b.y) >= 0 ? 0 : 1;
            var aDist = Math.abs(a.x - state.playerX), bDist = Math.abs(b.x - state.playerX);
            return aMarked - bMarked || aDist - bDist || a.y - b.y;
          });
          state.pendingDrops.push(state.sinkCandidates.shift());
          state.permanentTiles += 1;
          state.score = Math.max(0, state.score - 50);
        }
      }
    } else state.sinkClock = 0;
    if (state.aquiferHistory.length === 0 || state.elapsed - state.aquiferHistory[state.aquiferHistory.length - 1].t >= 1) {
      state.aquiferHistory.push({ t: Math.round(state.elapsed * 100) / 100, value: Math.round(state.aquifer * 100) / 100 });
    }
    return state;
  }

  function aquiferInfo(state) {
    return {
      value: Math.round(state.aquifer * 100) / 100,
      redLine: state.redLine,
      belowRed: state.aquifer < state.redLine,
      permanentTiles: state.permanentTiles,
      cmSunk: state.permanentTiles * 2
    };
  }

  function sinkTilesToDrop(state) {
    var drops = state.pendingDrops.slice();
    state.pendingDrops.length = 0;
    return drops;
  }

  function score(state) {
    var nisar = state.level.nisar || {};
    var realFactCm = Number.isFinite(nisar.realFactCm) ? nisar.realFactCm : null;
    var realFactText = nisar.realFactText || 'This level is a learning model, not a forecast.';
    var report = {
      aquiferCurve: state.aquiferHistory.slice(),
      cmSunk: state.permanentTiles * 2,
      realFactCm: realFactCm,
      realFactText: realFactText,
      oneLine: state.permanentTiles ? 'The aquifer fell below its red line and the ground dropped permanently.' : 'The ground stayed above its red line in this run.',
      calibrationNote: 'NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.'
    };
    return {
      score: state.score,
      stars: [!!state.completed, !!state.completed && !state.wasBelowRed, !!state.completed && state.chips >= 3],
      report: report
    };
  }

  return { createLevelState: createLevelState, update: update, aquiferInfo: aquiferInfo, sinkTilesToDrop: sinkTilesToDrop, score: score };
}));
