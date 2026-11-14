const model = require('../../game/model.js');

const scenarios = [
  ['D0', 0, 'Dry', 0],
  ['D50', 50, 'Dry', 0],
  ['D100', 100, 'Dry', 0],
  ['D150', 150, 'Dry', 0],
  ['W100', 100, 'Wet', 0],
  ['BN100', 100, 'Below Normal', 0],
  ['D100-F30', 100, 'Dry', 30],
  ['W0-F30', 0, 'Wet', 30],
  ['W150-F30', 150, 'Wet', 30],
  ['BN50-F30', 50, 'Below Normal', 30],
];

const results = scenarios.map(([name, pumpingPct, waterYear, fallowPct]) => {
  const state = model.createSimulationState({
    year1WaterYear: waterYear,
    year2WaterYear: waterYear,
    rngSeed: 7,
  });
  const surfaceAllocPct = model.getWaterYearSpec(waterYear).maxSurfacePct;
  model.setDistrictControls(state, 'ALL', { pumpingPct, surfaceAllocPct, fallowPct });
  for (let month = 0; month < 24; month += 1) model.stepMonth(state);

  const final = state.valleyHistory[state.valleyHistory.length - 1];
  return {
    strategy: name,
    pumpingPct,
    year: waterYear,
    fallowPct,
    months: state.monthStep,
    totalSubsidenceCm: Math.abs(final.worstTotalCm),
    permanentSubsidenceCm: Math.abs(final.worstInelasticCm),
    revenueMUsd: final.totalRevenueMUsd,
  };
});

const dryPumpSeries = results.slice(0, 4).map((r) => r.totalSubsidenceCm);
const pumpingMonotonic = dryPumpSeries.every((value, index) => index === 0 || value >= dryPumpSeries[index - 1]);
const permanentWithinTotal = results.every((r) => r.permanentSubsidenceCm <= r.totalSubsidenceCm + 1e-9);
const finiteAndNonnegative = results.every((r) =>
  [r.totalSubsidenceCm, r.permanentSubsidenceCm, r.revenueMUsd].every((value) => Number.isFinite(value) && value >= 0),
);

console.log(JSON.stringify({ results, checks: { pumpingMonotonic, permanentWithinTotal, finiteAndNonnegative } }, null, 2));
if (results.some((r) => r.months !== 24)) process.exitCode = 1;
