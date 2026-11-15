// Site translation (English <-> Turkish). English is the default and the page is left untouched in English.
// When Turkish is chosen (button in the header, remembered in localStorage, or ?lang=tr), this file loads
// i18n_tr.js from its own folder and translates the page's text, then keeps translating text that the
// page's own scripts add later (atlas list, simulator events, tour cards...) through a MutationObserver.
//
// How a translation is looked up: an element whose content is text plus inline tags (<b>, <a>, <span>...)
// is keyed by its text with each inline child written as {0}, {1}...  e.g.
//   "{0} shows how much the ground moved"  ->  "{0} zeminin ne kadar hareket ettiğini gösterir"
// The original child elements are moved into the new positions, so links, ids and live numbers keep working.
// Keys are whitespace-collapsed. Text without letters (numbers, units) is never touched.
// Missing keys: open any page with ?i18n=collect and run I18N.missing() in the console.
(function () {
  if (window.I18N) return;
  const STORE = 'nv-lang';
  const store = {
    get() { try { return localStorage.getItem(STORE); } catch (e) { return null; } },
    set(v) { try { localStorage.setItem(STORE, v); } catch (e) { /* private mode: choice lasts this page only */ } }
  };
  const me = document.currentScript;
  const src = me && me.src ? me.src : '';
  const base = src.replace(/[?#].*$/, '').replace(/[^/]*$/, '');
  const ver = (src.match(/\?[^#]*/) || [''])[0]; // deploy cache-bust (?v=sha) also applies to the dictionary
  const qs = new URLSearchParams(location.search);
  const collect = qs.get('i18n') === 'collect';
  const q = qs.get('lang');
  if (q === 'en' || q === 'tr') store.set(q);
  const lang = collect ? 'tr' : (q === 'en' || q === 'tr' ? q : (store.get() === 'tr' ? 'tr' : 'en'));

  const INLINE = new Set(['A', 'ABBR', 'B', 'BR', 'BUTTON', 'CODE', 'EM', 'I', 'IMG', 'INPUT', 'KBD', 'LABEL', 'MARK',
    'Q', 'S', 'SMALL', 'SPAN', 'STRONG', 'SUB', 'SUP', 'SVG', 'TIME', 'U', 'VAR', 'WBR', 'svg']);
  const SKIP = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEXTAREA', 'PRE', 'SVG', 'svg', 'CANVAS', 'TEMPLATE']);
  const ATTRS = ['placeholder', 'title', 'aria-label', 'alt'];
  const norm = s => s.replace(/\s+/g, ' ').trim();
  // Needs a real word: numbers with units ("−11.0 cm", "512 km²", "0.32 km³/yr") are left alone.
  const hasWords = s => /[A-Za-z]{3}/.test(s.replace(/\{\d+\}/g, ''));

  let dict = {}, patterns = [];
  const missing = new Set();

  // Numbers change (months, cm, counts), so a key may also be written with # for each number:
  //   "Month # of # · Summer"  ->  "Ay # / # · Yaz"   (numbers are put back in the same order)
  // {0}, {1}... are inline-element slots, not numbers, so they are kept as they are.
  const NUM = /\{\d+\}|[−+-]?\d[\d.,]*/g;
  const own = (o, k) => Object.prototype.hasOwnProperty.call(o, k);
  const produced = new Set(); // Turkish text we wrote; seeing it again is not a missing key
  function lookup(key) {
    const r = lookup0(key);
    if (r != null) produced.add(norm(r.replace(/\{\d+\}/g, '')));
    return r;
  }
  function lookup0(key) {
    if (!hasWords(key) || produced.has(norm(key.replace(/\{\d+\}/g, '')))) return null;
    if (own(dict, key)) return dict[key];
    const nums = [];
    const sk = key.replace(NUM, m => (m[0] === '{' ? m : (nums.push(m), '#')));
    if (nums.length && own(dict, sk)) return fillNums(dict[sk], nums);
    for (const [re, rep] of patterns) {
      const m = key.match(re);
      if (m) return typeof rep === 'function' ? rep(m, t) : key.replace(re, rep);
    }
    missing.add(key);
    return null;
  }
  // Put the page's numbers into a translation. Plain # takes the numbers in order. When Turkish word order
  // moves a number, the translation names it: #3 = the 3rd number of the English text (trailing , or . that
  // the number carried is dropped, the translation writes its own punctuation). Plain # skips numbers
  // that are named, so only the moved ones need an index.
  function fillNums(tpl, nums) {
    const named = new Set([...tpl.matchAll(/#(\d+)/g)].map(m => +m[1] - 1));
    let i = 0;
    const next = () => { while (named.has(i)) i++; return i < nums.length ? nums[i++] : '#'; };
    return tpl.replace(/\{\d+\}|#(\d+)|#/g, (m, n) => {
      if (m[0] === '{') return m;
      if (n) return nums[+n - 1] != null ? nums[+n - 1].replace(/[.,]$/, '') : m;
      return next();
    });
  }

  // t(): translate a fragment from inside a pattern (falls back to the English text).
  function t(s) { const k = norm(s); return Object.prototype.hasOwnProperty.call(dict, k) ? dict[k] : s; }

  function keyOf(el) {
    let k = '', n = 0, text = false;
    const kids = [];
    for (const c of el.childNodes) {
      if (c.nodeType === 3) { k += c.nodeValue; if (/\S/.test(c.nodeValue)) text = true; }
      else if (c.nodeType === 1) {
        if (!INLINE.has(c.tagName)) return {block: true};
        k += '{' + n++ + '}'; kids.push(c);
      }
    }
    return text ? {key: norm(k), kids, lead: /^\s/.test(k), trail: /\s$/.test(k)} : null;
  }

  function fill(el, tpl, info) {
    const out = [];
    const used = new Set();
    const parts = tpl.split(/\{(\d+)\}/);
    if (info.lead) out.push(document.createTextNode(' '));
    parts.forEach((p, i) => {
      if (i % 2) { const kid = info.kids[+p]; if (kid && !used.has(kid)) { out.push(kid); used.add(kid); } }
      else if (p) out.push(document.createTextNode(p));
    });
    info.kids.forEach(kid => { if (!used.has(kid)) out.push(kid); }); // never drop a live element
    if (info.trail) out.push(document.createTextNode(' '));
    el.replaceChildren(...out);
  }

  function doElement(el) {
    if (el.closest && el.closest('[translate="no"],.notranslate')) return;
    for (const a of ATTRS) {
      const v = el.getAttribute(a);
      if (v) { const tr = lookup(norm(v)); if (tr != null && !collect) el.setAttribute(a, tr); }
    }
    if (el.tagName === 'INPUT' && /^(button|submit)$/i.test(el.type) && el.value) {
      const tr = lookup(norm(el.value)); if (tr != null && !collect) el.value = tr;
    }
    const info = keyOf(el);
    if (!info) return;
    if (info.block) { // mixed block content: translate its loose text nodes one by one
      for (const c of el.childNodes) {
        if (c.nodeType === 3 && /\S/.test(c.nodeValue)) {
          const tr = lookup(norm(c.nodeValue));
          if (tr != null && !collect) c.nodeValue = c.nodeValue.replace(/\S[\s\S]*\S|\S/, tr);
        }
      }
      return;
    }
    const tr = lookup(info.key);
    if (tr != null && tr !== info.key && !collect) fill(el, tr, info);
  }

  function walk(root) {
    if (!root || root.nodeType !== 1) return;
    if (SKIP.has(root.tagName) || (root.closest && root.closest('script,style,svg,textarea,pre'))) return;
    const list = [root, ...root.querySelectorAll('*')];
    for (const el of list) {
      if (SKIP.has(el.tagName) || (el.parentElement && el.parentElement.closest('svg,script,style,textarea,pre'))) continue;
      doElement(el);
    }
  }

  let obs = null;
  function run(fn) { if (obs) obs.disconnect(); try { fn(); } finally { if (obs) { obs.takeRecords(); observe(); } } }
  function observe() {
    obs.observe(document.body, {childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ATTRS});
  }
  function onMut(recs) {
    const roots = new Set();
    for (const r of recs) {
      if (r.type === 'characterData') { if (r.target.parentElement) roots.add(r.target.parentElement); }
      else if (r.type === 'attributes') roots.add(r.target);
      else { roots.add(r.target); r.addedNodes.forEach(n => roots.add(n.nodeType === 1 ? n : n.parentElement)); }
    }
    run(() => roots.forEach(el => { if (el && el.isConnected) walk(el); }));
  }

  function translateAll() {
    run(() => {
      walk(document.body);
      const tt = lookup(norm(document.title));
      if (tt != null && !collect) document.title = tt;
    });
  }

  // ---- language button -------------------------------------------------------------------------------
  const BTN_CSS = `
.lang-btn{font:600 .74rem/1 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;letter-spacing:.06em;
  border:1px solid #c9d2de;background:#fff;color:#0b3d91;border-radius:999px;padding:6px 10px;cursor:pointer;
  white-space:nowrap;flex:none;align-self:center}
.lang-btn:hover{border-color:#0b3d91;background:#eef3fb}
.lang-btn:focus-visible{outline:2px solid #0b3d91;outline-offset:2px}
.lang-btn.lang-float{position:fixed;left:12px;bottom:12px;z-index:9000;box-shadow:0 2px 10px rgba(0,0,0,.2)}
.site-header>.site-nav{margin-left:auto}
.site-header>.lang-btn{margin-left:14px}
@media (max-width:640px){.site-header>.lang-btn{margin-left:8px;padding:5px 8px}}
html.i18n-wait body{visibility:hidden}`;

  function addButton() {
    if (document.querySelector('.lang-btn')) return;
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'lang-btn';
    b.setAttribute('translate', 'no');
    b.textContent = lang === 'tr' ? 'EN' : 'TR';
    b.title = lang === 'tr' ? 'Switch to English' : 'Türkçe';
    b.setAttribute('aria-label', b.title);
    b.addEventListener('click', () => {
      store.set(lang === 'tr' ? 'en' : 'tr');
      const u = new URL(location.href);
      u.searchParams.delete('lang');
      location.replace(u.toString());
    });
    // Site pages: right after the menu (not inside it: on phones the menu scrolls sideways and would hide it).
    const nav = document.querySelector('.site-header > .site-nav');
    const bar = document.querySelector('.topbar-meta');
    if (nav) nav.after(b);
    else if (bar) bar.appendChild(b);
    else { b.classList.add('lang-float'); document.body.appendChild(b); }
  }

  const st = document.createElement('style');
  st.textContent = BTN_CSS;
  document.head.appendChild(st);
  if (lang === 'tr' && !collect) {
    document.documentElement.classList.add('i18n-wait');
    setTimeout(() => document.documentElement.classList.remove('i18n-wait'), 2500); // never leave the page blank
  }

  function ready(fn) { if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn); else fn(); }

  function start() {
    obs = new MutationObserver(onMut);
    translateAll();
    observe();
    document.documentElement.lang = 'tr';
    document.documentElement.classList.remove('i18n-wait');
  }

  ready(addButton);
  if (lang === 'tr') {
    if (collect) ready(start);
    else {
      const s = document.createElement('script');
      s.src = base + 'i18n_tr.js' + ver;
      s.onload = () => { dict = window.I18N_TR || {}; patterns = window.I18N_TR_PATTERNS || []; ready(start); };
      s.onerror = () => document.documentElement.classList.remove('i18n-wait');
      document.head.appendChild(s);
    }
  }

  window.I18N = {lang, missing: () => [...missing].sort(), t: s => (lang === 'tr' ? t(s) : s)};
})();
