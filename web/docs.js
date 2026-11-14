// Shared helpers for science / data / faq pages: render team Markdown files and data tables.
const LOCAL = location.pathname.includes('/web/');
const ROOT = LOCAL ? '../' : './';
async function md(el, path, strip){
  const box = document.getElementById(el); if (!box) return;
  try{
    const r = await fetch(ROOT + path, {cache: 'no-cache'}); if (!r.ok) throw 0;
    let t = await r.text();
    if (strip) t = t.replace(/^>.*\n(>.*\n)*/m, '');           // drop internal usage notes at top
    box.innerHTML = marked.parse(t);
    const dir = path.slice(0, path.lastIndexOf('/') + 1);
    box.querySelectorAll('img').forEach(im => { const a = im.getAttribute('src'); if (a && !/^(https?:|\/|data:)/.test(a)) im.src = ROOT + dir + a; im.style.maxWidth = '100%'; });
    box.querySelectorAll('a[href]').forEach(a => { const h = a.getAttribute('href'); if (h && !/^(https?:|#|mailto:|\/)/.test(h)) a.href = ROOT + dir + h; });
    box.querySelectorAll('a[href^="http"]').forEach(a => { a.target = '_blank'; a.rel = 'noopener'; });
  }catch(e){ box.innerHTML = '<p class="small">This section is being prepared.</p>'; }
}
async function J(p){ try{ const r = await fetch(ROOT + p, {cache: 'no-cache'}); return r.ok ? await r.json() : null; }catch(e){ return null; } }
