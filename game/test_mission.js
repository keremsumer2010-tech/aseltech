// Balance check for the mission scoring (PC1): good play should reach A/B, over-pumping must fail.
// Usage: node game/test_mission.js
const Model = require('./model.js');
const Mission = require('./mission.js');

const baseline = (st) => ({ pumpingPct: 100, surfaceAllocPct: Math.min(60, Model.getWaterYearSpec(st.currentWaterYear).maxSurfacePct), fallowPct: 0 });
const strategies = {
  doNothing: baseline,
  overpump: (st) => ({ pumpingPct: 145, surfaceAllocPct: Math.min(20, Model.getWaterYearSpec(st.currentWaterYear).maxSurfacePct), fallowPct: 0 }),
  balance: (st) => ({ pumpingPct: 55, surfaceAllocPct: Model.getWaterYearSpec(st.currentWaterYear).maxSurfacePct, fallowPct: 25 }),
  smart: (st) => ({ pumpingPct: 75, surfaceAllocPct: Model.getWaterYearSpec(st.currentWaterYear).maxSurfacePct, fallowPct: 10 }),
  stopAll: (st) => ({ pumpingPct: 0, surfaceAllocPct: Model.getWaterYearSpec(st.currentWaterYear).maxSurfacePct, fallowPct: 50 }),
};

let fail = 0;
for (const basinId of ['tulare', 'konya']) {
  for (const y2 of ['Wet', 'Below Normal', 'Critical']) {
    const opts = { basinId, year1WaterYear: 'Below Normal', year2WaterYear: y2 };
    const ref = Mission.buildReference(Model, opts, baseline);
    const row = [];
    const res = {};
    for (const [name, pol] of Object.entries(strategies)) {
      const st = Model.createSimulationState(opts);
      Model.setDistrictControls(st, 'ALL', pol(st));
      let wy = st.currentWaterYear;
      while (!st.finished) { Model.stepMonth(st); if (st.currentWaterYear !== wy) { Model.setDistrictControls(st, 'ALL', pol(st)); wy = st.currentWaterYear; } }
      const ev = Mission.evaluate(st, ref);
      res[name] = ev;
      row.push(`${name}=${ev.grade}${ev.score}`);
    }
    console.log(basinId.padEnd(7), y2.padEnd(13), row.join('  '));
    if (!['D', 'F'].includes(res.overpump.grade)) { fail++; console.log('  FAIL: over-pumping should not pass'); }
    if (!['A', 'B'].includes(res.smart.grade) && !['A', 'B'].includes(res.balance.grade)) { fail++; console.log('  FAIL: no good strategy reaches A/B'); }
    if (['A', 'B'].includes(res.stopAll.grade)) { fail++; console.log('  FAIL: stopping all pumping should cost the farms'); }
  }
}
process.exit(fail ? 1 : 0);
