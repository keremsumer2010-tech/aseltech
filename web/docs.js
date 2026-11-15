// Shared helpers for science / data / faq pages: render team Markdown files and data tables.
const LOCAL = location.pathname.includes('/web/');
const ROOT = LOCAL ? '../' : './';
async function md(el, path, strip){
  const box = document.getElementById(el); if (!box) return;
  try{
    const r = await fetch(ROOT + path); if (!r.ok) throw 0;
    let t = await r.text();
    if (strip) t = t.replace(/^>.*\n(>.*\n)*/m, '');           // drop internal usage notes at top
    let html = marked.parse(t);
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
async function J(p){ try{ const r = await fetch(ROOT + p); return r.ok ? await r.json() : null; }catch(e){ return null; } }
