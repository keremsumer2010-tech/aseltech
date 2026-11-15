/* AQUIFER RUN — game rules (PC1). UMD: window.RunSystems in the browser, module.exports in Node.
 * Contract: web/run/DESIGN.md §10. Events come from main.js:
 *   {type:'pickup', target:'drop'|'chip', fact} · {type:'action', target:'pump'|'crop'|'dust', entity}
 *   {type:'dustHit'} · {type:'fall'} · {type:'reachFlag'}
 * Before each update main.js sets state.playerTx (player tile column) so sinking happens where the
 * player can see it.
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.RunSystems = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';
  var CM_PER_TILE = 2;          // one collapsed tile = 2 cm of permanent sinking (shown on the report)
  var SINK_EVERY = 2.0;         // seconds between collapses while below the safe line
  var SINK_NEAR = 14;           // only tiles within this many columns of the player collapse

  function count(level, type) { return (level.entities || []).filter(function (e) { return e.type === type; }).length; }

  function createLevelState(level) {
    var a = level.aquifer || {}, legend = level.legend || {}, sinkTiles = [];
    (level.tiles || []).forEach(function (row, y) {
      for (var x = 0; x < row.length; x++) { var n = legend[row.charAt(x)]; if (n && n.indexOf('sink') === 0) sinkTiles.push({ x: x, y: y, depth: 0 }); }
    });
    var chips = (level.entities || []).filter(function (e) { return e.type === 'chip'; });
    var start = a.start == null ? 70 : a.start;
    return {
      levelId: level.id, levelName: level.name, nisar: level.nisar || {},
      tank: 2, tankMax: 10, aquifer: start, redLine: a.redLine == null ? 40 : a.redLine,
      drainPerPump: a.drainPerPump == null ? 0.35 : a.drainPerPump,
      recharge: a.recharge == null ? 0.05 : a.recharge,
      cropRefill: a.cropRefill == null ? 3 : a.cropRefill,
      pumpBoost: a.pumpBoost == null ? 4 : a.pumpBoost,   // switching a pump off lets pressure recover at once
      pumpsTotal: count(level, 'pump'), pumpsOff: 0,
      cropsTotal: count(level, 'crop'), cropsWatered: 0,
      chipsTotal: chips.filter(function (c) { return c.fact !== 'qc'; }).length, chips: 0, qcFound: false,
      drops: 0, falls: 0, dustHits: 0, score: 0, time: 0,
      sinkTiles: sinkTiles, pending: [], permanentTiles: 0, sinkTimer: 0,
      belowRedEver: false, minAquifer: start, history: [start], histTimer: 0,
      facts: [], messages: [], finished: false, playerTx: 0,
    };
  }

  function say(state, text, kind) { state.messages.push({ text: text, kind: kind || 'info' }); }

  function handle(state, ev) {
    if (ev.type === 'pickup' && ev.target === 'drop') {
      state.drops++; state.score += 10;
      if (state.tank < state.tankMax) state.tank++; else say(state, 'Tank full! Water a thirsty crop.', 'info');
    } else if (ev.type === 'pickup' && ev.target === 'chip') {
      if (ev.fact === 'qc') {
        state.qcFound = true; state.score += 150;
        say(state, 'Bad reading! It jumped 12.1 cm in one step. Our check flags data like this.', 'science');
      } else {
        state.chips++; state.score += 300; if (ev.fact) state.facts.push(ev.fact);
        say(state, 'NISAR data chip ' + state.chips + '/' + state.chipsTotal + ' collected!', 'good');
      }
    } else if (ev.type === 'action' && ev.target === 'pump') {
      state.pumpsOff++; state.score += 150; state.aquifer = Math.min(100, state.aquifer + state.pumpBoost);
      var left = state.pumpsTotal - state.pumpsOff;
      say(state, left > 0 ? 'Pump off! ' + left + ' still draining the ground.' : 'All pumps off! The water underground can recover.', 'good');
    } else if (ev.type === 'action' && ev.target === 'crop') {
      if (state.tank >= 1) {
        state.tank -= 1; state.cropsWatered++; state.score += 100;
        state.aquifer = Math.min(100, state.aquifer + state.cropRefill);
        say(state, 'Crop saved with rainwater, so this farm pumps less!', 'good');
      } else {
        if (ev.entity) ev.entity.watered = false;   // veto: not enough water
        say(state, 'Your tank is empty! Catch a raindrop first, then water the crop.', 'warn');
      }
    } else if (ev.type === 'action' && ev.target === 'dust') {
      if (state.tank >= 1) { state.tank -= 1; state.score += 50; say(state, 'A splash of water calmed the dust devil.', 'good'); }
      else { if (ev.entity) ev.entity.calmed = false; say(state, 'No water left to spray!', 'warn'); }
    } else if (ev.type === 'dustHit') {
      state.dustHits++; var lost = Math.min(3, state.tank); state.tank -= lost;
      say(state, 'The dust devil stole ' + lost + ' water!', 'warn');
    } else if (ev.type === 'fall') {
      state.falls++; state.score = Math.max(0, state.score - 50);
    } else if (ev.type === 'reachFlag') {
      state.finished = true;
    }
  }

  function update(state, dt, events) {
    if (!state || state.finished) { (events || []).forEach(function (e) { if (state) handle(state, e); }); return state; }
    state.time += dt;
    (events || []).forEach(function (e) { handle(state, e); });
    var running = Math.max(0, state.pumpsTotal - state.pumpsOff);
    state.aquifer += (state.recharge - running * state.drainPerPump) * dt;
    state.aquifer = Math.max(0, Math.min(100, state.aquifer));
    state.minAquifer = Math.min(state.minAquifer, state.aquifer);
    state.histTimer += dt;
    if (state.histTimer >= 1) { state.histTimer = 0; state.history.push(Math.round(state.aquifer * 10) / 10); }

    if (state.aquifer < state.redLine) {
      if (!state.belowRedEver) say(state, 'Below the safe line! The clay squeezes and the ground starts to sink.', 'danger');
      state.belowRedEver = true;
      state.sinkTimer += dt;
      var every = SINK_EVERY * (0.5 + state.aquifer / state.redLine * 0.5);  // deeper = faster
      if (state.sinkTimer >= every) { state.sinkTimer = 0; collapseOne(state); }
    } else state.sinkTimer = 0;
    return state;
  }

  function collapseOne(state) {
    var best = null, bestD = 1e9;
    state.sinkTiles.forEach(function (t) {
      if (t.depth >= 2) return;
      var d = Math.abs(t.x - state.playerTx);
      if (d <= SINK_NEAR && d < bestD) { best = t; bestD = d; }
    });
    if (!best) return;
    state.pending.push({ x: best.x, y: best.y });
    best.y += 1; best.depth += 1;            // the ground under it can sink once more
    state.permanentTiles++; state.score = Math.max(0, state.score - 50);
  }

  function sinkTilesToDrop(state) { var p = state.pending; state.pending = []; return p; }

  function aquiferInfo(state) {
    return { value: state.aquifer, redLine: state.redLine, belowRed: state.aquifer < state.redLine,
      permanentTiles: state.permanentTiles, cmSunk: state.permanentTiles * CM_PER_TILE };
  }

  function score(state) {
    var stars = [!!state.finished, !state.belowRedEver, state.chips >= state.chipsTotal && state.chipsTotal > 0];
    var cm = state.permanentTiles * CM_PER_TILE, n = state.nisar || {};
    var oneLine = !state.belowRedEver
      ? 'You never let the water drop below the safe line, so the clay was not crushed. That is what good groundwater management looks like.'
      : cm === 0 ? 'The water dipped below the safe line, but you acted before the ground collapsed.'
        : 'The ground sank ' + cm + ' cm for good while the water was too low. Real valleys cannot undo this: the squeezed clay never holds water again.';
    return {
      score: state.score + state.tank * 10, stars: stars,
      report: {
        aquiferCurve: state.history.slice(), redLine: state.redLine, cmSunk: cm, minAquifer: Math.round(state.minAquifer),
        pumpsOff: state.pumpsOff, pumpsTotal: state.pumpsTotal, cropsWatered: state.cropsWatered, cropsTotal: state.cropsTotal,
        chips: state.chips, chipsTotal: state.chipsTotal, qcFound: state.qcFound, time: Math.round(state.time),
        realFactCm: n.realFactCm, realFactText: n.realFactText || '', oneLine: oneLine,
        calibration: 'NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.',
      },
    };
  }

  function popMessages(state) { var m = state.messages; state.messages = []; return m; }

  return { CM_PER_TILE: CM_PER_TILE, createLevelState: createLevelState, update: update, sinkTilesToDrop: sinkTilesToDrop,
    aquiferInfo: aquiferInfo, score: score, popMessages: popMessages };
});
