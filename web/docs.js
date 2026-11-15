// Shared helpers for science / data / faq pages: render team Markdown files and data tables.
const LOCAL = location.pathname.includes('/web/');
const ROOT = LOCAL ? '../' : './';
async function md(el, path, strip){
  const box = document.getElementById(el); if (!box) return;
  try{
    const r = await fetch(ROOT + path); if (!r.ok) throw 0;
    let t = await r.text();
    if (strip) t = t.replace(/^>.*\n(>.*\n)*/m, '');           // drop internal usage notes at top
    // Inline LaTeX ($\sigma_{pair}\sqrt{N}$) used to reach the page raw. Protect it from Markdown,
    // then typeset it with KaTeX (or show a readable plain-text fallback if KaTeX did not load). PC1.
    const maths = [];
    t = t.split(/(`[^`\n]*`)/).map((seg, i) => i % 2 ? seg : seg.replace(/\$(?=\S)([^$\n]+?)(?<=\S)\$/g, (m, tex) => {
      if (!/[\\^_{}=]/.test(tex) && !/^[A-Za-z]$/.test(tex)) return m;  // currency etc.
      maths.push(tex); return `@@MATH${maths.length - 1}@@`;
    })).join('');
    let html = marked.parse(t);
    html = html.replace(/@@MATH(\d+)@@/g, (m, i) => texToHtml(maths[+i]));
    const dir = path.slice(0, path.lastIndexOf('/') + 1);
    html = html.replace(/<img\s+([^>]*?)src=["']([^"']+)["']/gi, (m, pre, src) => {
      const fixedSrc = !/^(https?:|\/|data:)/.test(src) ? ROOT + dir + src : src;
      return `<img loading="lazy" decoding="async" style="max-width:100%" ${pre}src="${fixedSrc}"`;
    });
    box.innerHTML = html;
    box.querySelectorAll('a[href]').forEach(a => { const h = a.getAttribute('href'); if (h && !/^(https?:|#|mailto:|\/)/.test(h)) a.href = ROOT + dir + h; });
    box.querySelectorAll('a[href^="http"]').forEach(a => { a.target = '_blank'; a.rel = 'noopener'; });
  }catch(e){ box.innerHTML = '<p class="small">This section is being prepared.</p>'; }
}
const TEX_SYM = {sigma: 'σ', theta: 'θ', Delta: 'Δ', sum: 'Σ', cdot: '·', times: '×', le: '≤', ge: '≥', div: '÷', circ: '°', sqrt: '√', pm: '±', approx: '≈'};
function texToHtml(tex){
  if (window.katex){
    try{ return katex.renderToString(tex, {throwOnError: false, output: 'html'}); }catch(e){}
  }
  return '<i>' + tex.replace(/\\text\{([^}]*)\}/g, '$1')
    .replace(/\\([A-Za-z]+)/g, (m, w) => TEX_SYM[w] || w)
    .replace(/[{}\\]/g, '').replace(/</g, '&lt;') + '</i>';
}
async function J(p){ try{ const r = await fetch(ROOT + p); return r.ok ? await r.json() : null; }catch(e){ return null; } }
