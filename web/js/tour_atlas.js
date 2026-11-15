// Atlas page guided tour (steps only; the engine is js/tour.js).
// Opens by itself on the first visit once the atlas data has loaded; the "How to use" button replays it.
(function () {
  const steps = [
    {el: null, title: 'Welcome to the Subsidence Atlas',
      text: 'Every place on this page is sinking because groundwater is pumped out faster than it refills, measured by the NASA-ISRO NISAR radar satellite. This one-minute tour shows you how to read it.'},
    {el: '#vitalBar', title: 'The headline numbers',
      text: 'How many cities we measured, the fastest-sinking place, how much land is sinking (more than 5 cm, 2 inches, in one summer), and roughly how many people live on it.'},
    {el: '#atlasMap', title: 'The globe',
      text: 'Each dot is a measured basin; the colour shows how fast it sinks. Drag to turn the globe, scroll or pinch to zoom, and <b>click a dot</b> to open that place.'},
    {el: '#atlasTop5Card', title: 'Top 5 at a glance',
      text: 'The five fastest-sinking basins we trust most. Click a row to fly there.'},
    {el: '#atlasLayers', title: 'Change what the map shows',
      text: '<b>Subsidence</b> shows how much the ground moved, <b>Uncertainty</b> how sure the measurement is, and <b>Confidence</b> which places are reliable and which are only indicative.'},
    {el: '#tourBtn', title: 'Let the map present',
      text: '<b>Tour top 5</b> flies through the five fastest basins automatically. Handy when you show this to someone.'},
    {el: '.atlas-controls', title: 'Find and compare',
      text: 'Below the globe: search a city, filter by confidence or country, rank by speed or by area, switch between line-of-sight and vertical values, or put two cities side by side.'},
    {el: '#atlasTables', title: 'Rankings and downloads',
      text: 'Further down: ranking tables for reliable and indicative places, the change log, and open downloads (JSON, GeoJSON, CSV) with a citation.'},
    {el: '#guideBtn', title: 'See this again',
      text: 'That is it. Press <b>How to use</b> any time to replay this tour.'}
  ];

  const opts = {key: 'atlas-v1'};
  const btn = document.getElementById('guideBtn');
  if (btn) btn.addEventListener('click', () => window.GuidedTour && GuidedTour.start(steps, opts));

  // First visit: wait for the list and the map to exist so the lit areas are the real ones.
  let tries = 0;
  (function wait() {
    const ready = document.querySelectorAll('#top5CardRows tr').length && document.querySelector('#atlasMap canvas');
    if (ready || tries > 40) { if (window.GuidedTour) setTimeout(() => GuidedTour.auto(steps, opts), 600); return; }
    tries++; setTimeout(wait, 250);
  })();
})();
