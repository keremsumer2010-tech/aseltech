/* Mission & scoring for "Valley Under Pressure" (PC1).
 *
 * The player is judged against what would have happened if nobody changed anything: a hidden
 * "status quo" run of the same valley, with the same two water years, under the 2026 baseline
 * settings (the settings the model is calibrated to with NISAR). Three objectives:
 *   1. Keep the farms alive    — revenue at least 85% of the status quo
 *   2. Protect the aquifer      — permanent (inelastic) sinking at most half of the status quo
 *   3. Protect people & canals  — fewer dry wells than the status quo and canal loss below 12%
 * Score 0-100 -> grade A-F. Works in the browser (window.ValleyMission) and in Node (tests).
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.ValleyMission = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const TARGETS = { revenueShare: 0.85, permanentShare: 0.5, canalLossPct: 12 };

  function totals(state) {
    const ds = state.districts;
    return {
      revenue: ds.reduce((s, d) => s + d.cumulativeRevenueMUsd, 0),
      permanent: ds.reduce((m, d) => Math.max(m, Math.abs(d.inelasticCm)), 0),
      dryWells: ds.reduce((s, d) => s + d.dryWells, 0),
      canalLoss: ds.reduce((m, d) => Math.max(m, d.canalCapacityLossPct), 0),
    };
  }

  /** Run the status-quo valley for 24 months and keep monthly totals (index = month). */
  function buildReference(Model, createOpts, baselinePatch) {
    const st = Model.createSimulationState(createOpts);
    const patch = typeof baselinePatch === 'function' ? baselinePatch : () => baselinePatch;
    Model.setDistrictControls(st, 'ALL', patch(st));
    const months = [totals(st)];
    let lastWy = st.currentWaterYear;
    while (!st.finished) {
      Model.stepMonth(st);
      if (st.currentWaterYear !== lastWy) { Model.setDistrictControls(st, 'ALL', patch(st)); lastWy = st.currentWaterYear; }
      months.push(totals(st));
    }
    return { months };
  }

  const clamp01 = (v) => Math.max(0, Math.min(1, v));

  function evaluate(state, ref) {
    const t = totals(state);
    const r = ref.months[Math.min(state.monthStep, ref.months.length - 1)];
    const started = state.monthStep >= 12;  // permanent sinking builds up in the first summer, so judge after one full water year
    const revShare = r.revenue > 0 ? t.revenue / r.revenue : 1;
    const permShare = r.permanent > 0.05 ? t.permanent / r.permanent : (t.permanent > 0.05 ? 2 : 0);

    const farms = clamp01((revShare - 0.5) / (TARGETS.revenueShare - 0.5));  // below half the income the farms fail
    const ground = clamp01((1 - permShare) / (1 - TARGETS.permanentShare));
    const wellsOk = t.dryWells <= Math.max(0, r.dryWells - 1) || t.dryWells === 0;
    const people = clamp01((t.dryWells === 0 ? 1 : 1 - t.dryWells / Math.max(1, r.dryWells)) * 0.6 + (t.canalLoss < TARGETS.canalLossPct ? 0.4 : 0.4 * clamp01(1 - (t.canalLoss - TARGETS.canalLossPct) / 30)));

    const score = started ? Math.round(100 * (0.40 * farms + 0.40 * ground + 0.20 * people)) : null;
    const grade = score === null ? '–' : score >= 85 ? 'A' : score >= 70 ? 'B' : score >= 55 ? 'C' : score >= 40 ? 'D' : 'F';
    return {
      score, grade, totals: t, reference: r,
      objectives: [
        { key: 'farms', label: 'Keep the farms alive', ok: revShare >= TARGETS.revenueShare,
          now: `$${t.revenue.toFixed(1)}M`, goal: started ? `≥ $${(r.revenue * TARGETS.revenueShare).toFixed(1)}M (85% of doing nothing)` : 'at least 85% of the income of doing nothing', progress: farms },
        { key: 'ground', label: 'Protect the aquifer', ok: permShare <= TARGETS.permanentShare,
          now: `${t.permanent.toFixed(1)} cm permanent`, goal: started ? `≤ ${(r.permanent * TARGETS.permanentShare).toFixed(1)} cm (half of doing nothing)` : 'at most half the permanent sinking of doing nothing', progress: ground },
        { key: 'people', label: 'Protect wells & canals', ok: wellsOk && t.canalLoss < TARGETS.canalLossPct,
          now: `${t.dryWells} dry wells · canal −${t.canalLoss.toFixed(0)}%`, goal: started ? `< ${Math.max(1, r.dryWells)} dry wells · canal loss < 12%` : 'fewer dry wells than doing nothing, canal loss under 12%', progress: people },
      ],
    };
  }

  return { TARGETS, totals, buildReference, evaluate };
});
