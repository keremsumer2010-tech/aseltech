// 3-minute jury path (PC1): fills the home page from data/global/home_summary.json only.
(function(){
  const ROOT = location.pathname.includes('/web/') ? '../' : './';
  if (location.hash === '#play' || location.hash === '#simulator'){
    location.replace(ROOT + 'game/');
    return;
  }
  document.querySelectorAll('[data-rsrc]').forEach(el => { el.src = ROOT + el.dataset.rsrc; });
  document.querySelectorAll('[data-rhref]').forEach(el => { el.href = ROOT + el.dataset.rhref; });

  const COUNTRY = {kashmar: 'Iran', kerman: 'Iran', tianjin: 'China', gorgan: 'Iran', pekalongan: 'Indonesia', houston: 'USA', lagos: 'Nigeria', can_tho: 'Vietnam'};
  const minus = v => (v < 0 ? '−' : '') + Math.abs(v).toFixed(1);
  const fmtDate = d => new Date(d + 'T00:00:00Z').toLocaleDateString('en-GB', {day: 'numeric', month: 'short', timeZone: 'UTC'});
  const setAll = (sel, text) => document.querySelectorAll(sel).forEach(el => { el.textContent = text; });

  fetch(ROOT + 'data/global/home_summary.json', {cache: 'no-cache'}).then(r => r.ok ? r.json() : null).then(h => {
    if (!h) return;
    const k = Object.fromEntries(h.kpis.map(x => [x.key, x]));
    const show = {
      regions: String(k.regions.value),
      people: (k.people.value / 1e6).toFixed(2) + ' M',
      gnss: 'r = ' + k.gnss.value.toFixed(2),
      opera: 'r = ' + k.opera.value.toFixed(2),
      storage: k.storage.value.toFixed(2) + ' km³/yr'
    };
    Object.entries(show).forEach(([key, val]) => {
      document.querySelectorAll(`[data-kpi="${key}"]`).forEach(el => {
        if (key === 'storage' && el.classList.contains('kpi-num')) el.innerHTML = k.storage.value.toFixed(2) + ' <small>km³/yr</small>';
        else el.textContent = val;
      });
      setAll(`[data-kpi-det="${key}"]`, k[key].detail);
    });
    const areaM = /([\d.,]+)\s*km²/.exec(k.people.detail || '');
    if (areaM) setAll('[data-kpi-det-num="area"]', Math.round(parseFloat(areaM[1].replace(/,/g, ''))) + ' km²');
    const [w0, w1] = h.common_window;
    const days = Math.round((new Date(w1) - new Date(w0)) / 864e5);
    setAll('[data-hs="days"]', String(days));
    setAll('[data-hs="window"]', `${fmtDate(w0)} – ${fmtDate(w1)} 2026`);
    setAll('[data-hs="nflag"]', String(h.qc_story.flagged.length));
    const nrel = /(\d+) reliable/.exec(k.regions.detail || '');
    if (nrel) setAll('[data-hs="nrel"]', nrel[1]);
    setAll('[data-hs="flagged"]', h.qc_story.flagged.map(s => s.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())).join(', '));
    setAll('[data-hs="calib"]', h.calibration_note);

    // top 5
    const list = document.getElementById('top5');
    if (list){
      const maxAbs = Math.max(...h.top5.map(t => Math.abs(t.rate_cm_per_100d_common || 0)));
      list.innerHTML = h.top5.map(t => `
        <li><span class="rk">${t.rank}</span>
          <span class="nm"><b>${t.name}</b><span>${t.country || (COUNTRY[t.id] || '')}${t.note ? ' · caution' : ''}</span></span>
          <span class="rt">${minus(t.rate_cm_per_100d_common)} cm</span>
          <span class="bar"><i style="width:${(100 * Math.abs(t.rate_cm_per_100d_common) / maxAbs).toFixed(0)}%"></i></span></li>`).join('');
      const note = document.getElementById('top5note');
      if (note) note.innerHTML = `Fastest reliable basins, cm per 100 days toward or away from the satellite, common window ${w0} to ${w1}; ${h.qc_story.flagged.length} more basins are indicative only. ` + h.calibration_note;
    }

    // QC before/after chart
    const svg = document.getElementById('qcChart');
    const b = h.qc_story.series_before, a = h.qc_story.series_after;
    if (svg && b && a){
      const W = 520, H = 300, L = 46, R = 14, T = 16, B = 34;
      const all = [...b.dates, ...a.dates].map(d => +new Date(d));
      const t0 = Math.min(...all), t1 = Math.max(...all);
      const y0 = -13, y1 = 2;
      const X = d => L + (W - L - R) * ((+new Date(d)) - t0) / (t1 - t0);
      const Y = v => T + (H - T - B) * (y1 - v) / (y1 - y0);
      const path = s => s.dates.map((d, i) => `${i ? 'L' : 'M'}${X(d).toFixed(1)},${Y(s.disp_cm[i]).toFixed(1)}`).join(' ');
      let g = '';
      for (let v = 0; v >= -12; v -= 4) g += `<line x1="${L}" x2="${W - R}" y1="${Y(v)}" y2="${Y(v)}" stroke="#e5e8ee"/><text x="${L - 8}" y="${Y(v) + 4}" text-anchor="end" font-size="11" fill="#566273">${v}</text>`;
      g += `<text x="12" y="${T + 8}" font-size="11" fill="#566273">cm</text>`;
      const lastB = b.dates.length - 1;
      g += `<path d="${path(b)}" fill="none" stroke="#9aa3b0" stroke-width="2.5" stroke-dasharray="5 4"/>`;
      g += `<path d="${path(a)}" fill="none" stroke="#0b3d91" stroke-width="3"/>`;
      g += `<circle cx="${X(b.dates[lastB])}" cy="${Y(b.disp_cm[lastB])}" r="5" fill="#c8321f"/>`;
      g += `<text x="${X(b.dates[lastB]) - 8}" y="${Y(b.disp_cm[lastB]) + 4}" text-anchor="end" font-size="12" font-weight="700" fill="#c8321f">−12.1 cm (error: one 12.1 cm phase cycle)</text>`;
      const lastA = a.dates.length - 1;
      g += `<text x="${X(a.dates[lastA]) - 6}" y="${Y(a.disp_cm[lastA]) - 10}" text-anchor="end" font-size="12" font-weight="700" fill="#0b3d91">−6.2 cm after re-processing</text>`;
      [b.dates[0], b.dates[lastB]].forEach(d => { g += `<text x="${X(d)}" y="${H - 10}" text-anchor="middle" font-size="11" fill="#566273">${fmtDate(d)}</text>`; });
      svg.innerHTML = g;
    }
  }).catch(() => {});

  // section dots: show after the overview, mark the section in view
  const dn = document.querySelector('.dotnav');
  if (dn){
    const items = [...dn.querySelectorAll('a')].map(a => [a, document.getElementById(a.getAttribute('href').slice(1))]).filter(x => x[1]);
    const built = document.getElementById('built');
    const update = () => {
      dn.classList.toggle('on', !!built && built.getBoundingClientRect().bottom < innerHeight * 0.5);
      let cur = null;
      items.forEach(([a, el]) => { if (el.getBoundingClientRect().top < innerHeight * 0.45) cur = a; });
      items.forEach(([a]) => a.classList.toggle('cur', a === cur));
    };
    addEventListener('scroll', update, {passive: true}); addEventListener('resize', update); update();
  }

  // Fullscreen image lightbox for homepage cards (PC6)
  const lbModal = document.getElementById('imgLightbox');
  const lbImg = document.getElementById('lightboxImg');
  const lbCap = document.getElementById('lightboxCap');
  const lbClose = document.getElementById('lightboxClose');
  const lbBackdrop = lbModal ? lbModal.querySelector('.lightbox-backdrop') : null;

  function openLightbox(src, alt, captionText, linkHref, linkLabel) {
    if (!lbModal || !lbImg) return;
    lbImg.src = src;
    lbImg.alt = alt || 'Enlarged figure';
    let html = captionText ? `<span>${captionText}</span>` : '';
    if (linkHref) {
      html += ` <a href="${linkHref}" class="lb-link">${linkLabel || 'Open →'}</a>`;
    }
    if (lbCap) lbCap.innerHTML = html;
    lbModal.removeAttribute('hidden');
    document.body.classList.add('lightbox-open');
    if (lbClose) lbClose.focus();
  }

  function closeLightbox() {
    if (!lbModal) return;
    lbModal.setAttribute('hidden', '');
    document.body.classList.remove('lightbox-open');
    if (lbImg) lbImg.src = '';
  }

  if (lbModal) {
    if (lbClose) lbClose.addEventListener('click', closeLightbox);
    if (lbBackdrop) lbBackdrop.addEventListener('click', closeLightbox);
    if (lbImg) lbImg.addEventListener('click', closeLightbox);
    window.addEventListener('keydown', e => {
      if (e.key === 'Escape' && !lbModal.hasAttribute('hidden')) {
        closeLightbox();
      }
    });

    document.querySelectorAll('.work .wfig').forEach(fig => {
      const img = fig.querySelector('img');
      if (!img) return;

      img.title = 'Click to enlarge full screen';

      // Add visual hint badge
      const hint = document.createElement('span');
      hint.className = 'zoom-hint';
      hint.setAttribute('aria-hidden', 'true');
      hint.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 3 21 3 21 9"></polyline><polyline points="9 21 3 21 3 15"></polyline><line x1="21" y1="3" x2="14" y2="10"></line><line x1="3" y1="21" x2="10" y2="14"></line></svg> Click to enlarge';
      fig.appendChild(hint);

      img.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();
        const figcap = fig.querySelector('figcaption');
        const caption = figcap ? figcap.textContent.trim() : (img.alt || '');
        const isSim = (img.src && img.src.includes('simulator')) || !!fig.closest('#w8');
        const linkHref = isSim ? (ROOT + 'game/') : null;
        const linkLabel = isSim ? 'Launch Simulator →' : null;
        openLightbox(img.currentSrc || img.src, img.alt, caption, linkHref, linkLabel);
      });
    });
  }
})();
