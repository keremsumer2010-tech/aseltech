// Simulator guided tour (steps only). The engine lives in the site's js/tour.js:
// live site  /game/ -> ../js/tour.js     local server (repo root) /game/ -> ../web/js/tour.js
// Opens by itself the first time someone presses "Start simulation"; the "? Guide" button replays it.
(function () {
  const steps = [
    {el: null, title: 'How the simulator works',
      text: 'You run the water for a farming valley, month by month. Pump too much groundwater and the ground sinks for good, the same thing NISAR measures from space. Here is a quick look around.'},
    {el: '#mapStage', title: 'The valley',
      text: 'The colours show how far each district has sunk in the simulation. Canals change colour as the ground under them tilts and they lose capacity.'},
    {el: '.layer-switch', title: 'Compare with the satellite',
      text: '<b>Live Simulation</b> is your valley. <b>2026 NISAR Raster</b> is what the radar really measured. <b>Blend</b> lays one over the other.'},
    {el: '#basinSeg', title: 'Pick a basin',
      text: 'Switch between the Tulare Basin in California and the Konya Basin in Türkiye.'},
    {el: '.panel-card.levers', title: 'Your three controls',
      text: 'Drag the bars: how much <b>groundwater</b> to pump, how much <b>surface water</b> arrives by canal, and how much farmland to <b>fallow</b> (leave unplanted). Less pumping means less sinking, but also less farm income.'},
    {el: '#nextMonthBtn', title: 'Move time forward',
      text: 'Each press runs one month with your settings. <b>+6 months</b> jumps ahead, <b>Reset</b> starts over. Keyboard: <b>Space</b> or <b>N</b>.'},
    {el: '.timeline-dock', title: 'Sinking over time',
      text: 'Your sinking month by month, next to the 2026 NISAR measurement for the same place.'},
    {el: '.dock-card.readout', title: 'The trade-off',
      text: 'Total and permanent sinking against farm revenue. The goal is to keep the farms running without sinking the ground for good.'},
    {el: '.panel-card.events', title: 'What happened',
      text: 'Wells running dry, canals losing capacity, drought years: every month’s events are written here.'},
    {el: '#presetSeg', title: 'Ready-made scenarios',
      text: 'Try <b>Over-Pump</b> or <b>SGMA Balance</b> (California’s groundwater law) to see the two extremes, or press <b>Quick demo</b> for a 30-second automatic run.'},
    {el: '#guideBtn', title: 'See this again',
      text: 'That is all. Press <b>Guide</b> any time to replay this tour.'}
  ];
  const opts = {key: 'sim-v1'};

  function load(cb) {
    if (window.GuidedTour) return cb();
    const srcs = ['../js/tour.js', '../web/js/tour.js'];
    (function next() {
      const src = srcs.shift();
      if (!src) return;
      const s = document.createElement('script');
      s.src = src;
      s.onload = () => (window.GuidedTour ? cb() : next());
      s.onerror = next;
      document.head.appendChild(s);
    })();
  }

  function run(first) {
    load(() => (first ? GuidedTour.auto(steps, opts) : GuidedTour.start(steps, opts)));
  }

  const guide = document.getElementById('guideBtn');
  if (guide) guide.addEventListener('click', () => run(false));
  const startBtn = document.getElementById('startBtn');
  if (startBtn) startBtn.addEventListener('click', () => setTimeout(() => run(true), 500));
  load(() => {}); // fetch the engine early so the first tour opens without a delay
})();
