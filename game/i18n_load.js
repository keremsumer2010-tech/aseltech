// Loads the site's translation script (web/js/i18n.js) into the simulator.
// live site  /game/ -> ../js/i18n.js     local server (repo root) /game/ -> ../web/js/i18n.js
(function () {
  try {
    if (localStorage.getItem('nv-lang') === 'tr' || /[?&]lang=tr\b/.test(location.search)) {
      document.documentElement.classList.add('i18n-wait');
      setTimeout(function () { document.documentElement.classList.remove('i18n-wait'); }, 2500);
    }
  } catch (e) { /* storage blocked: English */ }
  var srcs = ['../js/i18n.js', '../web/js/i18n.js'];
  (function next() {
    var src = srcs.shift();
    if (!src) return;
    var s = document.createElement('script');
    s.src = src;
    s.onerror = next;
    document.head.appendChild(s);
  })();
})();
