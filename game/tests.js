/* Valley Under Pressure — model verification suite.
 * Shared by the simulator's "Model tests" panel and test_model.html.
 * Every case runs game/model.js live in the browser; nothing here is a stored result. */
(function (root) {
  'use strict';

  async function getJson(url) {
    try { const r = await fetch(url); return r.ok ? await r.json() : null; } catch (_e) { return null; }
  }

  function run24(opts, controls, months) {
    const M = root.ValleyModel;
    const s = M.createSimulationState(opts);
    M.setDistrictControls(s, 'ALL', controls);
    for (let i = 0; i < (months || 24); i++) M.stepMonth(s);
    return s;
  }

  async function run(base) {
    const M = root.ValleyModel;
    const b = base || '..';
    const [cvSum, cvPts, kSum, kPts] = await Promise.all([
      getJson(`${b}/data/central_valley/summary.json`),
      getJson(`${b}/data/central_valley/points.json`),
      getJson(`${b}/data/karapinar/summary.json`),
      getJson(`${b}/data/karapinar/points.json`),
    ]);
    const cases = [];
    const add = (group, name, criterion, pass, result) => cases.push({ id: `T-${String(cases.length + 1).padStart(2, '0')}`, group, name, criterion, pass: Boolean(pass), result });
    const f = (v, n = 2) => Number(v).toFixed(n);

    /* A · Calibration against NISAR */
    const cal = M.runCalibrationCheck(cvSum);
    add('Calibration', 'Tulare Basin, 108-day NISAR window',
      'Simulated vertical sinking within ±10 % of NISAR (summary.json)',
      cal.within10Pct && cal.simulatedVertCm < 0,
      `${f(cal.simulatedVertCm)} cm simulated vs ${f(cal.measuredVertCm)} cm measured · error ${cal.errorPct} %`);

    const kcal = M.runCalibrationCheck(kSum, 'konya');
    add('Calibration', 'Konya Closed Basin, 108-day NISAR window',
      'Simulated vertical sinking within ±10 % of NISAR (summary.json)',
      kcal.within10Pct && kcal.simulatedVertCm < 0,
      `${f(kcal.simulatedVertCm)} cm simulated vs ${f(kcal.measuredVertCm)} cm measured · error ${kcal.errorPct} %`);

    const hyd = M.hydrateFromRepoData(cvPts, cvSum);
    const p01 = hyd.districts.find((d) => d.id === 'p01');
    add('Calibration', 'Measured points loaded from repository data',
      'Terra Bella (p01) carries the NISAR value from points.json (−7.8 cm LOS)',
      p01 && Math.abs(p01.nisarLosCm - (-7.8)) < 0.05,
      p01 ? `${hyd.districts.length} districts · p01 = ${f(p01.nisarLosCm)} cm LOS` : 'p01 missing');

    const r = M.losToVertical(M.verticalToLos(-10, 39.1), 39.1);
    add('Calibration', 'Line-of-sight ↔ vertical conversion',
      'Round trip at 39.1° incidence returns the input (|error| < 10⁻⁹ cm)',
      Math.abs(r - (-10)) < 1e-9, `−10 cm → ${f(M.verticalToLos(-10, 39.1), 3)} cm LOS → ${f(r, 6)} cm`);

    /* B · Physics */
    const M2 = M;
    const hyst = M2.createSimulationState({ year1WaterYear: 'Dry', year2WaterYear: 'Wet' });
    M2.setDistrictControls(hyst, 'ALL', { pumpingPct: 145, surfaceAllocPct: 20, fallowPct: 0 });
    for (let i = 0; i < 12; i++) M2.stepMonth(hyst);
    const y1 = { ...hyst.districts[0] };
    M2.setDistrictControls(hyst, 'ALL', { pumpingPct: 10, surfaceAllocPct: 100, fallowPct: 50 });
    for (let i = 0; i < 6; i++) M2.stepMonth(hyst);
    const w = hyst.districts[0];
    add('Physics', 'Permanent clay compaction does not recover',
      'After a wet winter the water rises, but permanent sinking stays locked in',
      w.headM > y1.headM && w.inelasticCm <= y1.inelasticCm + 1e-9 && w.inelasticCm < -5,
      `water ${f(y1.headM, 1)} → ${f(w.headM, 1)} m · permanent ${f(y1.inelasticCm)} → ${f(w.inelasticCm)} cm`);

    const zero = run24({ year1WaterYear: 'Wet', year2WaterYear: 'Wet' }, { pumpingPct: 0, surfaceAllocPct: 100, fallowPct: 0 });
    const worstZero = Math.min(...zero.districts.map((d) => d.inelasticCm));
    add('Physics', 'No pumping, wet years: no permanent sinking',
      'Permanent compaction stays at 0 cm in every district (|value| < 0.01 cm)',
      worstZero > -0.01, `largest permanent value ${f(worstZero, 3)} cm across ${zero.districts.length} districts`);

    let monotone = true;
    const mix = M.createSimulationState({ year1WaterYear: 'Dry', year2WaterYear: 'Wet' });
    let prev = 0;
    for (let i = 0; i < 24; i++) {
      M.setDistrictControls(mix, 'ALL', { pumpingPct: i % 6 < 3 ? 150 : 0, surfaceAllocPct: 40, fallowPct: 0 });
      M.stepMonth(mix);
      const v = mix.districts[0].inelasticCm;
      if (v > prev + 1e-9) monotone = false;
      prev = v;
    }
    add('Physics', 'Permanent sinking only accumulates',
      'With pumping switched on and off every 3 months, permanent sinking never decreases',
      monotone, `24 months checked · final permanent ${f(prev)} cm`);

    /* C · Policy response */
    const hi = run24({ year1WaterYear: 'Below Normal', year2WaterYear: 'Below Normal' }, { pumpingPct: 150, surfaceAllocPct: 60, fallowPct: 0 });
    const mid = run24({ year1WaterYear: 'Below Normal', year2WaterYear: 'Below Normal' }, { pumpingPct: 100, surfaceAllocPct: 60, fallowPct: 0 });
    const cons = run24({ year1WaterYear: 'Below Normal', year2WaterYear: 'Below Normal' }, { pumpingPct: 40, surfaceAllocPct: 60, fallowPct: 25 });
    const [a, bb, c] = [hi, mid, cons].map((s) => s.districts[0].totalCm);
    add('Policy response', 'More pumping, more sinking',
      '150 % pumping sinks more than 100 %, which sinks more than conservation (40 %, 25 % fallow)',
      a < bb && bb < c, `150 %: ${f(a)} cm · 100 %: ${f(bb)} cm · conservation: ${f(c)} cm`);

    const fal0 = run24({ year1WaterYear: 'Below Normal', year2WaterYear: 'Below Normal' }, { pumpingPct: 100, surfaceAllocPct: 60, fallowPct: 0 });
    const fal40 = run24({ year1WaterYear: 'Below Normal', year2WaterYear: 'Below Normal' }, { pumpingPct: 100, surfaceAllocPct: 60, fallowPct: 40 });
    const rev = (s) => s.districts.reduce((t, d) => t + d.cumulativeRevenueMUsd, 0);
    add('Policy response', 'Fallowing trades income for ground',
      'Resting 40 % of land lowers farm income and does not increase sinking',
      rev(fal40) < rev(fal0) && fal40.districts[0].totalCm >= fal0.districts[0].totalCm - 1e-9,
      `income $${f(rev(fal0), 1)}M → $${f(rev(fal40), 1)}M · sinking ${f(fal0.districts[0].totalCm)} → ${f(fal40.districts[0].totalCm)} cm`);

    /* D · Numerical integrity */
    const crit = run24({ year1WaterYear: 'Critical', year2WaterYear: 'Critical' }, { pumpingPct: 120, surfaceAllocPct: 100, fallowPct: 0 });
    const capOk = crit.districts.every((d) => d.controls.surfaceAllocPct <= 15);
    const finite = crit.districts.every((d) => [d.headM, d.totalCm, d.inelasticCm, d.cumulativeRevenueMUsd, d.canalCapacityLossPct].every(Number.isFinite));
    add('Integrity', 'Critical-year surface water cap',
      'Surface water held at ≤ 15 % and no NaN or infinite value over 24 months',
      crit.finished && capOk && finite && crit.valleyHistory.length === 24,
      `max surface ${Math.max(...crit.districts.map((d) => d.controls.surfaceAllocPct))} % · ${crit.valleyHistory.length} months · finite: ${finite}`);

    const over = run24({ year1WaterYear: 'Critical', year2WaterYear: 'Critical' }, { pumpingPct: 150, surfaceAllocPct: 0, fallowPct: 0 });
    const bounded = over.districts.every((d) => d.canalCapacityLossPct >= 0 && d.canalCapacityLossPct <= 60.0001 && d.dryWells >= 0 && d.dryWells <= d.wellDepthsM.length);
    add('Integrity', 'Physical limits respected under extreme pumping',
      'Canal capacity loss stays within 0–60 % and dry wells never exceed the wells modelled',
      bounded, `max canal loss ${f(Math.max(...over.districts.map((d) => d.canalCapacityLossPct)), 1)} % · max dry wells ${Math.max(...over.districts.map((d) => d.dryWells))}`);

    const d1 = run24({ year1WaterYear: 'Dry', year2WaterYear: 'Wet' }, { pumpingPct: 110, surfaceAllocPct: 40, fallowPct: 10 });
    const d2 = run24({ year1WaterYear: 'Dry', year2WaterYear: 'Wet' }, { pumpingPct: 110, surfaceAllocPct: 40, fallowPct: 10 });
    const same = d1.districts.every((d, i) => d.totalCm === d2.districts[i].totalCm && d.cumulativeRevenueMUsd === d2.districts[i].cumulativeRevenueMUsd);
    add('Integrity', 'Reproducible results',
      'Two runs with identical inputs give identical outputs in every district',
      same, `${d1.districts.length} districts compared · Terra Bella ${f(d1.districts[0].totalCm)} cm both runs`);

    /* E · Konya */
    const kh = M.hydrateFromRepoData(kPts, kSum, 'konya');
    const kp01 = kh.districts.find((d) => d.id === 'p01');
    const ks = M.createSimulationState({ basinId: 'konya', districts: kh.districts, summaryData: kh.summaryData, year1WaterYear: 'Dry', year2WaterYear: 'Dry' });
    M.setDistrictControls(ks, 'ALL', { pumpingPct: 140, surfaceAllocPct: 30, fallowPct: 0 });
    for (let i = 0; i < 24; i++) M.stepMonth(ks);
    add('Konya', 'Sinkhole risk indicator responds to heavy pumping',
      '6 Konya districts load from NISAR data; two dry years at 140 % raise the indicator',
      kh.districts.length === 6 && kp01 && Math.abs(kp01.nisarLosCm - (-5.93)) < 0.05 && ks.sinkholeRiskActive,
      `${kh.districts.length} districts · p01 ${kp01 ? f(kp01.nisarLosCm) : '—'} cm LOS · indicator ${ks.sinkholeRiskActive ? 'raised' : 'not raised'}`);

    const passed = cases.filter((x) => x.pass).length;
    return { cases, passed, total: cases.length, ranAt: new Date() };
  }

  root.ValleyTests = { run };
})(typeof self !== 'undefined' ? self : this);
