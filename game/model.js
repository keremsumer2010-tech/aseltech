/**
 * Valley Under Pressure — Aquifer & Terzaghi Compaction Simulation Model (v2)
 *
 * Hydrological bucket model + Terzaghi / USGS skeletal storage subsidence physics
 * calibrated against NASA-ISRO NISAR provisional GUNW measurements (2026-06-28 -> 2026-10-14).
 *
 * Sources:
 *  - NISAR Provisional GUNW Time Series: ../data/central_valley/summary.json & points.json
 *  - USGS PP 1766 (Faunt et al., 2009): Central Valley Hydrologic Model (S_y, S_ske, S_skv, clay thickness)
 *  - USGS SIR 2013-5142 (Sneed et al., 2013): Subsidence along the Delta-Mendota & Friant-Kern corridors
 *  - California DWR: San Joaquin Valley Water Year Hydrologic Classification Index
 *  - USGS / USBR: Friant-Kern Canal ~60% historic conveyance capacity reduction due to differential subsidence
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.ValleyModel = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /**
   * Model configuration and sourced/illustrative parameters.
   * Parameters lacking a direct site-specific peer-reviewed curve are marked `illustrative: true`.
   */
  const CONFIG = {
    totalMonths: 24,
    startYear: 2026,
    startMonthIndex: 9, // October (0-indexed: 9 = Oct, start of California Water Year)
    incidenceDegDefault: 39.1, // data/central_valley/summary.json incidence_deg_at_max
    nisarWindowDays: 108, // 2026-06-28 to 2026-10-14
    calibration: {
      targetDistrictId: 'p01',
      targetMeasuredLosCm: -7.8,
      targetMeasuredVertCm: -10.1,
      scenario: {
        waterYearType: 'Below Normal', // Representative of dry-summer stress; calibrated at 100% pump
        pumpingPct: 100,
        surfaceAllocPct: 60,
        fallowPct: 0,
      },
      // Explicit extraction-stress multiplier aligning baseline summer drawdown to NISAR 108-day observation.
      // Derived so 108-day Jul-Oct baseline run at Terra Bella / Pixley matches summary.json (-10.1 cm vertical).
      extractionScaleFactor: 1.0,
      source: 'Calibrated to ../data/central_valley/summary.json (provisional NISAR path 34, 2026-06-28 -> 2026-10-14)',
      illustrative: false,
    },
    physics: {
      specificYield: {
        value: 0.10,
        unit: 'dimensionless',
        source: 'Williamson, Prudic & Swain (1989) USGS PP 1401-D — Tulare/SJV cited average 0.10 (range 0.08–0.12)',
        illustrative: false,
      },
      elasticSpecificStorage: {
        value: 1.0e-5,
        unit: '1/m',
        source: 'Order of magnitude, Sneed (2001) USGS OFR 01-35; exact m^-1 value not verified in full PDF',
        illustrative: true,
      },
      inelasticSpecificStorage: {
        value: 3.1e-4,
        unit: '1/m',
        source: 'Order of magnitude (~31x S_ske), Sneed (2001) USGS OFR 01-35 (>=20x ratio); exact value not verified',
        illustrative: true,
      },
      baselineAnnualDemandM: {
        value: 1.48,
        unit: 'm/yr equivalent column',
        source: 'Simplified Tulare bucket irrigation demand curve',
        illustrative: true,
      },
      baselineAnnualRechargeM: {
        value: 0.72,
        unit: 'm/yr natural + canal percolation',
        source: 'Scaled regional recharge + conveyance seepage benchmark',
        illustrative: true,
      },
    },
    // Monthly California Central Valley irrigation & recharge normalized weights (Oct..Sep, sum = 1.0, illustrative)
    seasonalWeights: {
      // Index: 0=Oct, 1=Nov, 2=Dec, 3=Jan, 4=Feb, 5=Mar, 6=Apr, 7=May, 8=Jun, 9=Jul, 10=Aug, 11=Sep
      pumping: [0.05, 0.02, 0.01, 0.01, 0.02, 0.05, 0.09, 0.12, 0.15, 0.19, 0.17, 0.12],
      recharge: [0.04, 0.08, 0.14, 0.18, 0.17, 0.15, 0.10, 0.06, 0.03, 0.02, 0.015, 0.015],
    },
    // California DWR San Joaquin Valley Water Year Index structure (weights/probs marked illustrative until CDEC WSIHIST verified)
    waterYearTypes: [
      { id: 'Wet', label: 'Wet', prob: 0.30, rechargeMult: 1.38, maxSurfacePct: 100, badgeColor: '#3ddc97', illustrative: true },
      { id: 'Above Normal', label: 'Above Normal', prob: 0.15, rechargeMult: 1.15, maxSurfacePct: 90, badgeColor: '#4da3ff', illustrative: true },
      { id: 'Below Normal', label: 'Below Normal', prob: 0.17, rechargeMult: 0.90, maxSurfacePct: 70, badgeColor: '#8cbef8', illustrative: true },
      { id: 'Dry', label: 'Dry', prob: 0.18, rechargeMult: 0.60, maxSurfacePct: 40, badgeColor: '#f5b942', illustrative: true },
      { id: 'Critical', label: 'Critical', prob: 0.20, rechargeMult: 0.35, maxSurfacePct: 15, badgeColor: '#ff6b57', illustrative: true },
    ],
    thresholds: {
      canalMediumGradientMmKm: 5.0,
      canalHighGradientMmKm: 10.0,
      sinkholeAlertCm: 4.0, // Karapinar 0-1 km NISAR ring mean (-4.152 cm LOS, data/karapinar/assets.json)
      source: 'Aligned with risk/compute_risk.py, data/central_valley/assets.json, and data/karapinar/assets.json',
      illustrative: true,
    },
  };

  /**
   * 7 Real Tulare Basin / Southern San Joaquin Valley Districts anchored on data/central_valley/points.json.
   * Baseline clay thickness b0, initial depth-to-water, preconsolidation head, and well distributions
   * combine measured NISAR spatial contrast with USGS Tulare Basin hydrogeology.
   */
  const DEFAULT_DISTRICTS = [
    {
      id: 'p01',
      name: 'Terra Bella / Pixley Corridor',
      shortName: 'Terra Bella',
      pointName: '6 km N of Terra Bella',
      lon: -119.02173,
      lat: 36.01119,
      areaKm2: 340,
      clayThicknessM: 76, // Thick eastern alluvial/clay interbeds along Friant-Kern
      initialHeadM: -48.0, // Depth relative to ground surface (m)
      preconsolidationHeadM: -48.3,
      pumpingIntensity: 1.05,
      wellDepthsM: [50, 54, 58, 63, 70, 78, 88, 100], // Representative domestic + ag well thresholds (illustrative)
      revenuePerIrrigatedHa: 5400, // USD/ha citrus/orchard mix (illustrative)
      irrigatedAreaKHa: 28,
      canalCorridor: 'Friant-Kern Canal',
      baseGradientMmKm: 46.06, // From data/central_valley/assets.json
      nisarLosCm: -7.8,
      nisarDates: ['2026-06-28', '2026-07-10', '2026-07-22', '2026-08-15', '2026-08-27', '2026-09-08', '2026-09-20', '2026-10-14'],
      nisarSeriesCm: [0.0, -0.84, -2.07, -3.0, -4.6, -3.35, -6.24, -7.8],
    },
    {
      id: 'p04',
      name: 'Corcoran Bowl (Tulare Lakebed)',
      shortName: 'Corcoran',
      pointName: '15 km W of Corcoran',
      lon: -119.7283,
      lat: 36.0909,
      areaKm2: 460,
      clayThicknessM: 82, // Total compressible fine-grained interbeds (Corcoran Clay member <= 61 m)
      initialHeadM: -52.0,
      preconsolidationHeadM: -52.4,
      pumpingIntensity: 0.90,
      wellDepthsM: [55, 60, 65, 72, 82, 95],
      revenuePerIrrigatedHa: 4300,
      irrigatedAreaKHa: 38,
      canalCorridor: 'Tulare Irrigation District Canal',
      baseGradientMmKm: 57.01,
      nisarLosCm: -7.0,
      nisarDates: ['2026-06-28', '2026-07-10', '2026-07-22', '2026-08-15', '2026-08-27', '2026-09-08', '2026-09-20', '2026-10-14'],
      nisarSeriesCm: [0.0, -0.75, -1.85, -2.69, -4.12, -3.01, -5.6, -7.0],
    },
    {
      id: 'p02',
      name: 'South Lemoore / Kettleman',
      shortName: 'S. Lemoore',
      pointName: '21 km S of Lemoore',
      lon: -119.8447,
      lat: 36.1163,
      areaKm2: 390,
      clayThicknessM: 75,
      initialHeadM: -50.0,
      preconsolidationHeadM: -50.3,
      pumpingIntensity: 1.04,
      wellDepthsM: [53, 57, 62, 69, 80, 92],
      revenuePerIrrigatedHa: 4600,
      irrigatedAreaKHa: 31,
      canalCorridor: 'California Aqueduct',
      baseGradientMmKm: 49.12,
      nisarLosCm: -7.78,
      nisarDates: ['2026-06-28', '2026-07-10', '2026-07-22', '2026-08-15', '2026-08-27', '2026-09-08', '2026-09-20', '2026-10-14'],
      nisarSeriesCm: [0.0, -0.84, -2.06, -2.99, -4.58, -3.34, -6.22, -7.78],
    },
    {
      id: 'p03',
      name: 'Huron / Westlands Subbasin',
      shortName: 'Huron',
      pointName: '10 km SW of Huron',
      lon: -120.157,
      lat: 36.1272,
      areaKm2: 410,
      clayThicknessM: 72,
      initialHeadM: -58.0,
      preconsolidationHeadM: -58.3,
      pumpingIntensity: 1.01,
      wellDepthsM: [61, 66, 72, 80, 90, 105],
      revenuePerIrrigatedHa: 4800,
      irrigatedAreaKHa: 34,
      canalCorridor: 'California Aqueduct (West)',
      baseGradientMmKm: 36.4,
      nisarLosCm: -7.22,
      nisarDates: ['2026-06-28', '2026-07-10', '2026-07-22', '2026-08-15', '2026-08-27', '2026-09-08', '2026-09-20', '2026-10-14'],
      nisarSeriesCm: [0.0, -0.78, -1.91, -2.78, -4.25, -3.1, -5.77, -7.22],
    },
    {
      id: 'p05',
      name: 'Ivanhoe / Kaweah Fan',
      shortName: 'Ivanhoe',
      pointName: '5 km NE of Ivanhoe',
      lon: -119.1712,
      lat: 36.4117,
      areaKm2: 310,
      clayThicknessM: 60,
      initialHeadM: -36.0,
      preconsolidationHeadM: -36.4,
      pumpingIntensity: 1.03,
      wellDepthsM: [39, 43, 47, 52, 60, 70],
      revenuePerIrrigatedHa: 5200,
      irrigatedAreaKHa: 24,
      canalCorridor: 'Alta East Branch Canal',
      baseGradientMmKm: 48.1,
      nisarLosCm: -6.25,
      nisarDates: ['2026-06-28', '2026-07-10', '2026-07-22', '2026-08-15', '2026-08-27', '2026-09-08', '2026-09-20', '2026-10-14'],
      nisarSeriesCm: [0.0, -0.67, -1.66, -2.4, -3.68, -2.68, -5.0, -6.25],
    },
    {
      id: 'p08',
      name: 'Richgrove / Foothill Transition',
      shortName: 'Richgrove',
      pointName: 'Richgrove',
      lon: -119.108,
      lat: 35.7847,
      areaKm2: 260,
      clayThicknessM: 12, // Thin sand-gravel terrace, low compressible clay fraction
      initialHeadM: -31.0,
      preconsolidationHeadM: -32.2,
      pumpingIntensity: 0.60,
      wellDepthsM: [36, 42, 48, 56, 65],
      revenuePerIrrigatedHa: 3900,
      irrigatedAreaKHa: 18,
      canalCorridor: 'Friant-Kern South Branch',
      baseGradientMmKm: 18.2,
      nisarLosCm: -0.29,
      nisarDates: ['2026-06-28', '2026-07-10', '2026-07-22', '2026-08-15', '2026-08-27', '2026-09-08', '2026-09-20', '2026-10-14'],
      nisarSeriesCm: [0.0, -0.03, -0.08, -0.11, -0.17, -0.12, -0.23, -0.29],
    },
    {
      id: 'p06',
      name: 'Avenal / Coast Range Fringe',
      shortName: 'Avenal Fringe',
      pointName: '6 km S of Avenal',
      lon: -120.1154,
      lat: 35.9503,
      areaKm2: 290,
      clayThicknessM: 14,
      initialHeadM: -42.0,
      preconsolidationHeadM: -43.0,
      pumpingIntensity: 0.62,
      wellDepthsM: [47, 53, 60, 68],
      revenuePerIrrigatedHa: 3100,
      irrigatedAreaKHa: 14,
      canalCorridor: 'California Aqueduct (Reach 7)',
      baseGradientMmKm: 7.5,
      nisarLosCm: -0.46,
      nisarDates: ['2026-06-28', '2026-07-10', '2026-07-22', '2026-08-15', '2026-08-27', '2026-09-08', '2026-09-20', '2026-10-14'],
      nisarSeriesCm: [0.0, -0.05, -0.12, -0.18, -0.27, -0.20, -0.37, -0.46],
    },
  ];

  /**
   * 6 Konya Closed Basin (Karapinar, Turkiye) zones anchored directly on data/karapinar/points.json & assets.json.
   * Baseline NISAR span: 2026-06-26 -> 2026-10-12 (-5.9 cm LOS peak, -8.0 cm implied vertical at 41.9 deg incidence).
   */
  const KONYA_DISTRICTS = [
    {
      id: 'p01',
      name: 'West Karapinar Core',
      shortName: 'W. Karapinar',
      pointName: '2 km W of Karapınar',
      lon: 33.53056,
      lat: 37.71818,
      areaKm2: 180,
      clayThicknessM: 64, // Thick lacustrine carbonates & neogene clay interbeds
      initialHeadM: -46.0,
      preconsolidationHeadM: -46.3,
      pumpingIntensity: 1.0,
      wellDepthsM: [49, 53, 58, 65, 74, 86],
      revenuePerIrrigatedHa: 3400,
      irrigatedAreaKHa: 28,
      canalCorridor: 'Karapinar D330 Corridor',
      baseGradientMmKm: 32.8,
      sinkholesWithin5km: 10,
      nisarLosCm: -5.93,
      nisarDates: ['2026-06-26', '2026-07-08', '2026-07-20', '2026-08-13', '2026-08-25', '2026-09-06', '2026-09-18', '2026-09-30', '2026-10-12'],
      nisarSeriesCm: [0.0, -1.06, -0.78, -2.1, -2.27, -2.78, -2.51, -3.69, -5.93],
    },
    {
      id: 'p02',
      name: 'Oymali Irrigated Plain',
      shortName: 'Oymali',
      pointName: '3 km W of Oymalı',
      lon: 33.79045,
      lat: 37.74485,
      areaKm2: 145,
      clayThicknessM: 42,
      initialHeadM: -42.0,
      preconsolidationHeadM: -42.5,
      pumpingIntensity: 0.72,
      wellDepthsM: [46, 51, 57, 65],
      revenuePerIrrigatedHa: 2900,
      irrigatedAreaKHa: 22,
      canalCorridor: 'Oymali Agricultural Drain',
      baseGradientMmKm: 18.5,
      sinkholesWithin5km: 4,
      nisarLosCm: -2.57,
      nisarDates: ['2026-06-26', '2026-07-08', '2026-07-20', '2026-08-13', '2026-08-25', '2026-09-06', '2026-09-18', '2026-09-30', '2026-10-12'],
      nisarSeriesCm: [0.0, -0.73, -0.36, -0.95, -0.22, -0.7, -0.69, -1.13, -2.57],
    },
    {
      id: 'p03',
      name: 'Akoren Wellfield Zone',
      shortName: 'Akoren',
      pointName: '5 km NW of Akören',
      lon: 33.77806,
      lat: 37.68869,
      areaKm2: 130,
      clayThicknessM: 36,
      initialHeadM: -39.0,
      preconsolidationHeadM: -39.6,
      pumpingIntensity: 0.65,
      wellDepthsM: [43, 49, 56, 64],
      revenuePerIrrigatedHa: 2800,
      irrigatedAreaKHa: 19,
      canalCorridor: 'Akoren Local Collector',
      baseGradientMmKm: 14.2,
      sinkholesWithin5km: 2,
      nisarLosCm: -1.82,
      nisarDates: ['2026-06-26', '2026-07-08', '2026-07-20', '2026-08-13', '2026-08-25', '2026-09-06', '2026-09-18', '2026-09-30', '2026-10-12'],
      nisarSeriesCm: [0.0, -0.54, -0.42, -0.41, 0.03, 1.3, 0.1, -0.82, -1.82],
    },
    {
      id: 'p04',
      name: 'Gazi Osman Pasa Karst Belt',
      shortName: 'Gazi O. Pasa',
      pointName: '6 km SE of Gazi Osman Paşa',
      lon: 33.51831,
      lat: 37.65262,
      areaKm2: 140,
      clayThicknessM: 34,
      initialHeadM: -40.0,
      preconsolidationHeadM: -40.7,
      pumpingIntensity: 0.62,
      wellDepthsM: [44, 50, 58, 67],
      revenuePerIrrigatedHa: 3000,
      irrigatedAreaKHa: 21,
      canalCorridor: 'D330 Highway & Obruk Belt',
      baseGradientMmKm: 13.4,
      sinkholesWithin5km: 6,
      nisarLosCm: -1.74,
      nisarDates: ['2026-06-26', '2026-07-08', '2026-07-20', '2026-08-13', '2026-08-25', '2026-09-06', '2026-09-18', '2026-09-30', '2026-10-12'],
      nisarSeriesCm: [0.0, -0.09, -0.22, -0.56, -0.11, -0.57, 0.36, -0.66, -1.74],
    },
    {
      id: 'p06',
      name: 'Kesmez Limestone Margin',
      shortName: 'Kesmez',
      pointName: '7 km N of Kesmez',
      lon: 33.70747,
      lat: 37.70788,
      areaKm2: 115,
      clayThicknessM: 14,
      initialHeadM: -34.0,
      preconsolidationHeadM: -35.0,
      pumpingIntensity: 0.48,
      wellDepthsM: [39, 46, 54],
      revenuePerIrrigatedHa: 2500,
      irrigatedAreaKHa: 15,
      canalCorridor: 'Kesmez Feeder Drain',
      baseGradientMmKm: 6.2,
      sinkholesWithin5km: 3,
      nisarLosCm: -0.35,
      nisarDates: ['2026-06-26', '2026-07-08', '2026-07-20', '2026-08-13', '2026-08-25', '2026-09-06', '2026-09-18', '2026-09-30', '2026-10-12'],
      nisarSeriesCm: [0.0, 0.04, -0.11, 1.3, -0.05, 0.86, 1.66, 0.57, -0.35],
    },
    {
      id: 'p11',
      name: 'Yesilyurt Reference Bench',
      shortName: 'Yesilyurt',
      pointName: '2 km SE of Yeşilyurt',
      lon: 33.74333,
      lat: 37.75453,
      areaKm2: 105,
      clayThicknessM: 10,
      initialHeadM: -29.0,
      preconsolidationHeadM: -30.5,
      pumpingIntensity: 0.35,
      wellDepthsM: [35, 42, 50],
      revenuePerIrrigatedHa: 2400,
      irrigatedAreaKHa: 12,
      canalCorridor: 'Yesilyurt Reference Corridor',
      baseGradientMmKm: 3.1,
      sinkholesWithin5km: 0,
      nisarLosCm: 0.47,
      nisarDates: ['2026-06-26', '2026-07-08', '2026-07-20', '2026-08-13', '2026-08-25', '2026-09-06', '2026-09-18', '2026-09-30', '2026-10-12'],
      nisarSeriesCm: [0.0, 0.28, 0.08, 0.33, 0.25, 0.18, 0.31, 0.32, 0.47],
    },
  ];

  const BASINS = {
    tulare: {
      id: 'tulare',
      name: 'Tulare Basin, California (USA)',
      shortLabel: 'Tulare Basin, USA',
      incidenceDegDefault: 39.1,
      targetDistrictId: 'p01',
      targetMeasuredLosCm: -7.8,
      targetMeasuredVertCm: -10.1,
      nisarWindowText: '2026-06-28 → 2026-10-14',
      summaryPath: '../data/central_valley/summary.json',
      wyLabel: 'California DWR SJV Water Year Index',
      districts: DEFAULT_DISTRICTS,
    },
    konya: {
      id: 'konya',
      name: 'Konya Closed Basin / Karapinar, Turkiye',
      shortLabel: 'Konya Basin, Türkiye',
      incidenceDegDefault: 41.9,
      targetDistrictId: 'p01',
      targetMeasuredLosCm: -5.9,
      targetMeasuredVertCm: -8.0,
      nisarWindowText: '2026-06-26 → 2026-10-12',
      summaryPath: '../data/karapinar/summary.json',
      wyLabel: 'Anatolian Interior Precipitation Index (illustrative)',
      districts: KONYA_DISTRICTS,
    },
  };

  function getBasinConfig(basinId) {
    return BASINS[basinId] || BASINS.tulare;
  }

  const MONTH_NAMES = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'];

  function degToRad(deg) {
    return (deg * Math.PI) / 180;
  }

  /**
   * Convert vertical displacement (cm) to NISAR Line-of-Sight (LOS) assuming purely vertical motion.
   */
  function verticalToLos(verticalCm, incidenceDeg) {
    const deg = typeof incidenceDeg === 'number' ? incidenceDeg : CONFIG.incidenceDegDefault;
    return verticalCm * Math.cos(degToRad(deg));
  }

  /**
   * Convert NISAR LOS (cm) to implied vertical displacement (cm) assuming purely vertical motion.
   */
  function losToVertical(losCm, incidenceDeg) {
    const deg = typeof incidenceDeg === 'number' ? incidenceDeg : CONFIG.incidenceDegDefault;
    return losCm / Math.cos(degToRad(deg));
  }

  /**
   * Determine California DWR Water Year class deterministically or stochastically from a uniform [0,1) draw.
   */
  function sampleWaterYearType(rngVal) {
    const u = typeof rngVal === 'number' ? Math.max(0, Math.min(0.999999, rngVal)) : Math.random();
    let acc = 0;
    for (let i = 0; i < CONFIG.waterYearTypes.length; i++) {
      acc += CONFIG.waterYearTypes[i].prob;
      if (u < acc) return CONFIG.waterYearTypes[i];
    }
    return CONFIG.waterYearTypes[2]; // Below Normal fallback
  }

  function getWaterYearSpec(id) {
    return CONFIG.waterYearTypes.find((w) => w.id === id) || CONFIG.waterYearTypes[2];
  }

  /**
   * Compute exact calibration scale factor so that Terra Bella (p01) over 108 summer irrigation days
   * (fractional Jul+Aug+Sep+half-Oct window under baseline normal/below-normal pumping) reproduces
   * `targetMeasuredVertCm` (-10.1 cm vertical / -7.8 cm LOS).
   */
  function computeCalibratedDemandMultiplier(targetVertCm, basinId) {
    const basin = getBasinConfig(basinId);
    const targetVert = typeof targetVertCm === 'number' ? targetVertCm : basin.targetMeasuredVertCm;
    const p01 = basin.districts[0];
    const sy = CONFIG.physics.specificYield.value;
    const ske = CONFIG.physics.elasticSpecificStorage.value;
    const skv = CONFIG.physics.inelasticSpecificStorage.value;
    const b0 = p01.clayThicknessM;
    // 108-day NISAR window spans Jun 28 -> Oct 14: sum seasonal weights for Jul (9), Aug (10), Sep (11), ~half Oct (0) + 2 days Jun
    const pumpSum =
      CONFIG.seasonalWeights.pumping[9] +
      CONFIG.seasonalWeights.pumping[10] +
      CONFIG.seasonalWeights.pumping[11] +
      0.45 * CONFIG.seasonalWeights.pumping[0] +
      0.07 * CONFIG.seasonalWeights.pumping[8];
    const rechSum =
      CONFIG.seasonalWeights.recharge[9] +
      CONFIG.seasonalWeights.recharge[10] +
      CONFIG.seasonalWeights.recharge[11] +
      0.45 * CONFIG.seasonalWeights.recharge[0] +
      0.07 * CONFIG.seasonalWeights.recharge[8];

    // Pre-drop allowance above preconsolidation head is initialBufferM; remaining drawdown drives inelastic compaction
    // Exact piecewise inverse of stepMonth(): total = ske*b0*initialBufferM + skv*b0*(dhAbs - initialBufferM)
    const initialBufferM = Math.max(0, p01.initialHeadM - p01.preconsolidationHeadM);
    const neededCompactionM = Math.abs(targetVert) / 100.0;
    const requiredDhAbs =
      neededCompactionM / b0 <= ske * initialBufferM
        ? neededCompactionM / (b0 * ske)
        : initialBufferM + (neededCompactionM / b0 - ske * initialBufferM) / skv;
    // Required net column withdrawal over 108-day window: sy * requiredDhAbs = pumpCol - rechCol
    const rechCol =
      CONFIG.physics.baselineAnnualRechargeM.value *
      getWaterYearSpec(CONFIG.calibration.scenario.waterYearType).rechargeMult *
      (0.65 + 0.35 * (CONFIG.calibration.scenario.surfaceAllocPct / 100.0)) *
      rechSum;
    const neededPumpCol = sy * requiredDhAbs + rechCol;
    const rawPumpCol = CONFIG.physics.baselineAnnualDemandM.value * p01.pumpingIntensity * pumpSum;
    return neededPumpCol / rawPumpCol;
  }

  /**
   * Create a fresh 24-month game/simulation state.
   */
  function createSimulationState(options) {
    const opts = options || {};
    const basinId = opts.basinId || 'tulare';
    const basin = getBasinConfig(basinId);
    const customDistricts = opts.districts || basin.districts;
    const summaryData = opts.summaryData || null;
    const targetVert =
      summaryData && typeof summaryData.max_subsidence_vertical_cm_estimate === 'number'
        ? summaryData.max_subsidence_vertical_cm_estimate
        : basin.targetMeasuredVertCm;
    const targetLos =
      summaryData && typeof summaryData.max_subsidence_cm === 'number'
        ? summaryData.max_subsidence_cm
        : basin.targetMeasuredLosCm;
    const incidenceDeg =
      summaryData && typeof summaryData.incidence_deg_at_max === 'number'
        ? summaryData.incidence_deg_at_max
        : basin.incidenceDegDefault;

    const calFactor = computeCalibratedDemandMultiplier(targetVert, basinId);
    const wyYear1 = opts.year1WaterYear || 'Below Normal';
    const wyYear2 = opts.year2WaterYear || sampleWaterYearType(opts.rngSeed).id;

    const districts = customDistricts.map((d) => ({
      ...d,
      headM: d.initialHeadM,
      preconsolidationHeadM: d.preconsolidationHeadM,
      elasticCm: 0.0,
      inelasticCm: 0.0,
      totalCm: 0.0,
      dryWells: 0,
      canalCapacityLossPct: 0.0,
      sinkholeRiskIndicator: false,
      currentGradientMmKm: d.baseGradientMmKm * 0.15, // Start of water year (Oct) baseline
      cumulativeRevenueMUsd: 0.0,
      controls: {
        pumpingPct: 100,
        surfaceAllocPct: getWaterYearSpec(wyYear1).maxSurfacePct,
        fallowPct: 0,
      },
      history: [],
    }));

    return {
      basinId: basin.id,
      basinName: basin.name,
      monthStep: 0, // 0..24
      totalMonths: CONFIG.totalMonths,
      finished: false,
      calibrationFactor: calFactor,
      incidenceDeg: incidenceDeg,
      measuredTargetLosCm: targetLos,
      measuredTargetVertCm: targetVert,
      year1WaterYear: wyYear1,
      year2WaterYear: wyYear2,
      currentWaterYear: wyYear1,
      sinkholeRiskActive: false,
      events: [],
      districts: districts,
      valleyHistory: [],
    };
  }

  /**
   * Set player policy controls for one district or all districts.
   */
  function setDistrictControls(state, districtId, patch) {
    const wySpec = getWaterYearSpec(state.currentWaterYear);
    const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
    const applyOne = (d) => {
      if (typeof patch.pumpingPct === 'number') {
        d.controls.pumpingPct = clamp(patch.pumpingPct, 0, 150);
      }
      if (typeof patch.surfaceAllocPct === 'number') {
        d.controls.surfaceAllocPct = clamp(patch.surfaceAllocPct, 0, wySpec.maxSurfacePct);
      }
      if (typeof patch.fallowPct === 'number') {
        d.controls.fallowPct = clamp(patch.fallowPct, 0, 50);
      }
    };

    if (districtId === 'ALL') {
      state.districts.forEach(applyOne);
    } else {
      const target = state.districts.find((d) => d.id === districtId);
      if (target) applyOne(target);
    }
    return state;
  }

  /**
   * Advance one month (or a fractional month weight `monthFraction` for exact 108-day calibration checks).
   */
  function stepMonth(state, monthFraction) {
    if (state.finished || state.monthStep >= state.totalMonths) {
      state.finished = true;
      return { state, newEvents: [] };
    }

    const frac = typeof monthFraction === 'number' ? monthFraction : 1.0;
    const mIdx = state.monthStep;
    const wyMonthIdx = mIdx % 12; // 0=Oct .. 11=Sep
    const wyNumber = mIdx < 12 ? 1 : 2;
    const prevWy = state.currentWaterYear;
    state.currentWaterYear = wyNumber === 1 ? state.year1WaterYear : state.year2WaterYear;
    const wySpec = getWaterYearSpec(state.currentWaterYear);

    const calendarYear = CONFIG.startYear + Math.floor((CONFIG.startMonthIndex + mIdx) / 12);
    const monthLabel = MONTH_NAMES[wyMonthIdx] + ' ' + calendarYear;

    const sy = CONFIG.physics.specificYield.value;
    const ske = CONFIG.physics.elasticSpecificStorage.value;
    const skv = CONFIG.physics.inelasticSpecificStorage.value;
    const baseDemand = CONFIG.physics.baselineAnnualDemandM.value;
    const baseRecharge = CONFIG.physics.baselineAnnualRechargeM.value;

    const pumpWeight = CONFIG.seasonalWeights.pumping[wyMonthIdx] * frac;
    const rechWeight = CONFIG.seasonalWeights.recharge[wyMonthIdx] * frac;

    const newEvents = [];
    if (mIdx === 12 || (mIdx > 0 && state.currentWaterYear !== prevWy)) {
      const basinCfg = getBasinConfig(state.basinId);
      const capMsg = wySpec.maxSurfacePct < 70 ? `Surface allocations capped at ${wySpec.maxSurfacePct}% under seasonal quota rules.` : `Full or near-full surface deliveries (${wySpec.maxSurfacePct}% cap) available.`;
      newEvents.push({
        id: `wy-${wyNumber}-${state.currentWaterYear}`,
        severity: wySpec.id === 'Critical' || wySpec.id === 'Dry' ? 'danger' : 'info',
        title: `Water Year 2 Declaration: ${wySpec.label} Year`,
        detail: `${basinCfg.wyLabel} sets WY${wyNumber} to ${wySpec.label}. ${capMsg}`,
        source: basinCfg.wyLabel,
      });
    }

    state.districts.forEach((d) => {
      // Respect surface cap if water year transitioned into a drier class
      if (d.controls.surfaceAllocPct > wySpec.maxSurfacePct) {
        d.controls.surfaceAllocPct = wySpec.maxSurfacePct;
      }

      const activeCroppedFraction = 1.0 - d.controls.fallowPct / 100.0;
      const pumpFactor = (d.controls.pumpingPct / 100.0) * activeCroppedFraction;
      const surfaceFactor = Math.min(wySpec.maxSurfacePct, d.controls.surfaceAllocPct) / 100.0;

      // Water balance bucket: Δh = (Recharge - Pumping_Withdrawal) / S_y
      const rechargeM =
        baseRecharge *
        wySpec.rechargeMult *
        (0.65 + 0.35 * surfaceFactor) *
        rechWeight;
      const withdrawalM =
        baseDemand *
        d.pumpingIntensity *
        state.calibrationFactor *
        pumpFactor *
        pumpWeight;

      const deltaH = (rechargeM - withdrawalM) / sy;
      const prevHead = d.headM;
      const nextHead = prevHead + deltaH;
      const prevPc = d.preconsolidationHeadM;

      // Terzaghi / USGS elastic vs inelastic skeletal compaction:
      //  - Any head movement above preconsolidation head is purely elastic (recoverable on recharge).
      //  - Any drop below historical minimum (preconsolidation head) induces permanent clay compaction
      //    and lowers h_pc irreversibly.
      let dElasticCm = 0;
      let dInelasticCm = 0;

      if (nextHead >= prevPc) {
        // Entire step stays in elastic regime (either falling toward h_pc or recovering upward)
        dElasticCm = ske * d.clayThicknessM * deltaH * 100.0;
      } else {
        // Crosses or drops further below prevPc
        if (prevHead > prevPc) {
          const elasticPartDh = prevPc - prevHead; // negative
          const virginPartDh = nextHead - prevPc; // negative
          dElasticCm = ske * d.clayThicknessM * elasticPartDh * 100.0;
          dInelasticCm = skv * d.clayThicknessM * virginPartDh * 100.0;
        } else {
          // Already at preconsolidation stress: all further drop is virgin inelastic compaction
          dInelasticCm = skv * d.clayThicknessM * deltaH * 100.0;
        }
        d.preconsolidationHeadM = nextHead;
      }

      d.headM = nextHead;
      // Elastic deflection rebounds toward zero on winter recharge; tiny net positive elastic heave capped cleanly
      d.elasticCm = Math.min(2.0, d.elasticCm + dElasticCm);
      // Permanent compaction is strictly non-positive (never recovers when water returns)
      d.inelasticCm = Math.min(0.0, d.inelasticCm + dInelasticCm);
      d.totalCm = d.elasticCm + d.inelasticCm;

      // Dry wells: count wells whose intake depth becomes shallower than depth-to-water (-headM)
      const prevDry = d.dryWells;
      const depthToWaterM = -d.headM;
      d.dryWells = d.wellDepthsM.filter((depth) => depthToWaterM >= depth).length;
      if (d.dryWells > prevDry && d.dryWells >= 2 && newEvents.length < 3) {
        newEvents.push({
          id: `wells-${d.id}-${mIdx}`,
          severity: 'warn',
          title: `Domestic & Shallow Wells Failing in ${d.shortName}`,
          detail: `Water table dropped to ${depthToWaterM.toFixed(1)} m depth, dewatering ${d.dryWells}/${d.wellDepthsM.length} tracked representative wells (illustrative threshold).`,
          source: 'Illustrative well-depth curve calibrated to SJV shallow domestic wells',
        });
      }

      // Differential subsidence gradient & canal capacity loss (Friant-Kern / Aqueduct illustrative physics)
      const prevCapLoss = d.canalCapacityLossPct;
      // Scale district total subsidence magnitude against historical 108-day gradient from assets.json
      const amp = Math.max(0, Math.abs(d.totalCm) / Math.max(1.5, Math.abs(losToVertical(d.nisarLosCm, state.incidenceDeg))));
      d.currentGradientMmKm = Number((d.baseGradientMmKm * Math.min(2.5, amp)).toFixed(2));
      if (d.currentGradientMmKm > CONFIG.thresholds.canalHighGradientMmKm && Math.abs(d.totalCm) > 2.0) {
        const excessFrac = Math.min(1.0, (Math.abs(d.totalCm) - 2.0) / 28.0);
        // USBR/FWA documented up to ~60% capacity bottleneck in worst Friant-Kern Middle Reach sag zones
        d.canalCapacityLossPct = Number((Math.min(60.0, excessFrac * 60.0)).toFixed(1));
      } else {
        d.canalCapacityLossPct = Math.max(d.canalCapacityLossPct, 0);
      }

      if (prevCapLoss < 12 && d.canalCapacityLossPct >= 12 && newEvents.length < 3) {
        newEvents.push({
          id: `canal-${d.id}-${mIdx}`,
          severity: 'danger',
          title: `${d.canalCorridor} Freeboard & Conveyance Loss`,
          detail: `Differential subsidence reached ${d.currentGradientMmKm.toFixed(1)} mm/km near ${d.shortName}, cutting canal conveyance by ${d.canalCapacityLossPct.toFixed(0)}%. (Reference bottleneck threshold vs. NISAR gradients).`,
          source: 'data/central_valley/assets.json / USGS SIR 2013-5142',
        });
      }

      // Konya Closed Basin factual sinkhole risk indicator (indicator only, never predictive)
      if (state.basinId === 'konya' && (d.sinkholesWithin5km || 0) > 0) {
        const wasActive = d.sinkholeRiskIndicator;
        const breached = d.headM <= d.preconsolidationHeadM + 0.05 && Math.abs(d.totalCm) >= CONFIG.thresholds.sinkholeAlertCm;
        if (breached) {
          d.sinkholeRiskIndicator = true;
          state.sinkholeRiskActive = true;
          if (!wasActive && newEvents.length < 3) {
            newEvents.push({
              id: `sinkhole-${d.id}-${mIdx}`,
              severity: 'danger',
              title: `Sinkhole risk indicator elevated in ${d.shortName}`,
              detail: `Subsidence reached ${d.totalCm.toFixed(1)} cm below historical groundwater lows near ${d.sinkholesWithin5km} documented obruks (0-1 km ring NISAR mean -4.15 cm). Indicator only; does not predict collapse of individual sinkholes.`,
              source: 'data/karapinar/assets.json & sinkholes.geojson (indicator only)',
            });
          }
        }
      }

      // Monthly crop revenue (M USD): scales with cropped area & total water sufficiency; penalized if groundwater overly restricted
      const waterSupplyIndex = Math.min(1.15, 0.58 * (d.controls.pumpingPct / 100.0) + 0.42 * surfaceFactor + 0.15 * rechWeight * 8);
      const cropYieldMult = Math.max(0.25, waterSupplyIndex) * activeCroppedFraction;
      const grossYearRevM = (d.revenuePerIrrigatedHa * (d.irrigatedAreaKHa * 1000)) / 1e6;
      const pumpEnergyPenaltyM = 0.04 * (d.controls.pumpingPct / 100.0) * (depthToWaterM / 50.0) * grossYearRevM * pumpWeight;
      const monthRevM = grossYearRevM * pumpWeight * cropYieldMult - pumpEnergyPenaltyM;
      d.cumulativeRevenueMUsd += monthRevM;

      d.history.push({
        monthStep: mIdx + 1,
        label: monthLabel,
        headM: Number(d.headM.toFixed(2)),
        preconsolidationHeadM: Number(d.preconsolidationHeadM.toFixed(2)),
        elasticCm: Number(d.elasticCm.toFixed(2)),
        inelasticCm: Number(d.inelasticCm.toFixed(2)),
        totalCm: Number(d.totalCm.toFixed(2)),
        totalLosCm: Number(verticalToLos(d.totalCm, state.incidenceDeg).toFixed(2)),
        dryWells: d.dryWells,
        canalCapacityLossPct: d.canalCapacityLossPct,
        gradientMmKm: d.currentGradientMmKm,
        revenueMUsd: Number(d.cumulativeRevenueMUsd.toFixed(2)),
      });
    });

    // Summarize worst-hit / basin aggregates for the bottom timeline chart
    const sortedByTotal = [...state.districts].sort((a, b) => a.totalCm - b.totalCm);
    const worstDistrict = sortedByTotal[0];
    const totalDryWells = state.districts.reduce((s, d) => s + d.dryWells, 0);
    const totalRevenueM = state.districts.reduce((s, d) => s + d.cumulativeRevenueMUsd, 0);
    const maxCapLoss = state.districts.reduce((m, d) => Math.max(m, d.canalCapacityLossPct), 0);

    state.valleyHistory.push({
      monthStep: mIdx + 1,
      wyMonthIdx: wyMonthIdx,
      label: monthLabel,
      waterYear: state.currentWaterYear,
      worstDistrictId: worstDistrict.id,
      worstTotalCm: Number(worstDistrict.totalCm.toFixed(2)),
      worstInelasticCm: Number(worstDistrict.inelasticCm.toFixed(2)),
      worstElasticCm: Number(worstDistrict.elasticCm.toFixed(2)),
      worstLosCm: Number(verticalToLos(worstDistrict.totalCm, state.incidenceDeg).toFixed(2)),
      meanTotalCm: Number((state.districts.reduce((s, d) => s + d.totalCm, 0) / state.districts.length).toFixed(2)),
      totalDryWells: totalDryWells,
      maxCanalLossPct: Number(maxCapLoss.toFixed(1)),
      totalRevenueMUsd: Number(totalRevenueM.toFixed(1)),
    });

    if (newEvents.length) {
      state.events = [...newEvents, ...state.events].slice(0, 12);
    }

    state.monthStep += 1;
    if (state.monthStep >= state.totalMonths) {
      state.finished = true;
    }

    return { state, newEvents };
  }

  /**
   * Run deterministic 108-day calibration test (Jul + Aug + Sep + 0.45*Oct + 0.07*Jun) under
   * baseline pumping (100%), normal/below-normal allocation, and 0% fallowing to verify alignment
   * with data/central_valley/summary.json within +-10%.
   */
  function runCalibrationCheck(summaryData, basinId) {
    const basin = getBasinConfig(basinId);
    const s = summaryData || {};
    const measuredLos = typeof s.max_subsidence_cm === 'number' ? s.max_subsidence_cm : basin.targetMeasuredLosCm;
    const measuredVert =
      typeof s.max_subsidence_vertical_cm_estimate === 'number'
        ? s.max_subsidence_vertical_cm_estimate
        : basin.targetMeasuredVertCm;
    const incDeg = typeof s.incidence_deg_at_max === 'number' ? s.incidence_deg_at_max : basin.incidenceDegDefault;

    const sim = createSimulationState({
      basinId: basin.id,
      year1WaterYear: CONFIG.calibration.scenario.waterYearType,
      year2WaterYear: CONFIG.calibration.scenario.waterYearType,
      summaryData: s,
    });
    setDistrictControls(sim, 'ALL', {
      pumpingPct: CONFIG.calibration.scenario.pumpingPct,
      surfaceAllocPct: CONFIG.calibration.scenario.surfaceAllocPct,
      fallowPct: CONFIG.calibration.scenario.fallowPct,
    });

    // Execute the exact 108-day Jun -> Oct summer window slice across seasonal weights
    const windowSlices = [
      { monthStepIdx: 8, frac: 0.07 }, // late Jun
      { monthStepIdx: 9, frac: 1.0 },  // Jul
      { monthStepIdx: 10, frac: 1.0 }, // Aug
      { monthStepIdx: 11, frac: 1.0 }, // Sep
      { monthStepIdx: 0, frac: 0.45 }, // early-mid Oct
    ];

    windowSlices.forEach((sl) => {
      sim.monthStep = sl.monthStepIdx;
      sim.finished = false;
      stepMonth(sim, sl.frac);
    });

    const p01 = sim.districts.find((d) => d.id === 'p01');
    const simVertCm = Number(p01.totalCm.toFixed(2));
    const simLosCm = Number(verticalToLos(p01.totalCm, incDeg).toFixed(2));
    const errorPct = Number((Math.abs((simVertCm - measuredVert) / measuredVert) * 100.0).toFixed(2));

    return {
      basinId: basin.id,
      district: p01.name,
      windowDays: CONFIG.nisarWindowDays,
      calibrationFactor: Number(sim.calibrationFactor.toFixed(3)),
      measuredLosCm: measuredLos,
      measuredVertCm: measuredVert,
      simulatedVertCm: simVertCm,
      simulatedLosCm: simLosCm,
      errorPct: errorPct,
      within10Pct: errorPct <= 10.0,
    };
  }

  /**
   * Synchronize district NISAR reference data directly from fetched basin points.json.
   */
  function hydrateFromRepoData(pointsJson, summaryJson, basinId) {
    const basin = getBasinConfig(basinId);
    const districts = basin.districts.map((d) => ({ ...d }));
    if (Array.isArray(pointsJson)) {
      districts.forEach((d) => {
        const match = pointsJson.find((p) => p.id === d.id);
        if (match) {
          d.pointName = match.name || d.pointName;
          d.lon = typeof match.lon === 'number' ? match.lon : d.lon;
          d.lat = typeof match.lat === 'number' ? match.lat : d.lat;
          if (Array.isArray(match.dates) && match.dates.length) {
            d.nisarDates = match.dates;
          }
          if (Array.isArray(match.disp_cm) && match.disp_cm.length) {
            d.nisarSeriesCm = match.disp_cm;
            d.nisarLosCm = match.disp_cm[match.disp_cm.length - 1];
          }
        }
      });
    }
    return { districts, summaryData: summaryJson || null };
  }

  return {
    CONFIG,
    BASINS,
    DEFAULT_DISTRICTS,
    KONYA_DISTRICTS,
    MONTH_NAMES,
    getBasinConfig,
    verticalToLos,
    losToVertical,
    sampleWaterYearType,
    getWaterYearSpec,
    computeCalibratedDemandMultiplier,
    createSimulationState,
    setDistrictControls,
    stepMonth,
    runCalibrationCheck,
    hydrateFromRepoData,
  };
});
