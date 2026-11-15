/* Aquifer Run offline support (PC1). Network first, cache as fallback, so updates show at once
 * and the game still opens with no connection after the first visit. */
var CACHE = 'aquifer-run-v10';
var CORE = [
  './', 'index.html', 'manifest.webmanifest',
  'art.js?v=10', 'engine.js?v=10', 'player.js?v=10', 'systems.js?v=10', 'main.js?v=10',
  'levels/tulare.json', 'levels/eloy.json', 'levels/konya.json', 'levels/mexico.json',
  '../assets/atlas_world.jpg', '../assets/logo_mark_64.png', '../assets/logo_mark_192.png', '../assets/logo_mark_512.png',
  '../data/central_valley/disp/2026-10-14.png', '../data/global/eloy/disp/2026-10-17.png',
  '../data/karapinar/disp/2026-10-12.png', '../data/global/mexico_city/disp/2026-10-20.png'
];

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) {
    // one missing file must not block the install
    return Promise.all(CORE.map(function (u) { return c.add(u).catch(function () {}); }));
  }).then(function () { return self.skipWaiting(); }));
});

self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (k) { return k.indexOf('aquifer-run-') === 0 && k !== CACHE; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;
  e.respondWith(fetch(req).then(function (res) {
    if (res && res.ok && (new URL(req.url).origin === self.location.origin || req.url.indexOf('fonts.g') !== -1)) {
      var copy = res.clone(); caches.open(CACHE).then(function (c) { c.put(req, copy); });
    }
    return res;
  }).catch(function () {
    return caches.match(req).then(function (hit) { return hit || caches.match(req, { ignoreSearch: true }); });
  }));
});
