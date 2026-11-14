// Atlas <-> NISAR 3D orbit view bridge (PC1). Uses the globals atlasData, activeId and
// selectRegion from atlas.js (loaded before this file). The 3D view opens by default;
// "2D map" in its toolbar returns to the flat atlas map, this button brings it back.
(function(){
  const bar = document.querySelector('.atlas-toolbar');
  const wrap = document.querySelector('.atlas-mapwrap');
  if (!bar || !wrap) return;

  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'n3d-open-btn';
  btn.innerHTML = '<span class="dot"></span>NISAR 3D orbit';
  btn.title = 'Fly the real NISAR orbit and watch the radar swath image the selected region';
  bar.appendChild(btn);

  let mod = null;
  const regions = () => (typeof atlasData !== 'undefined' && atlasData?.regions) || [];
  const current = () => {
    const id = (typeof activeId !== 'undefined' && activeId) || regions()[0]?.id;
    return regions().find(r => r.id === id) || null;
  };
  const load = async () => (mod = mod || await import('./nisar3d.js?v=14'));

  async function openView(opts){
    btn.disabled = true;
    try{ await load(); await mod.open(wrap, current(), opts); }
    catch(e){ console.error('NISAR 3D failed to load', e); }
    btn.disabled = false;
  }
  btn.addEventListener('click', () => openView({}));

  // Open by default once the atlas data is in (WebGL required; otherwise the 2D map stays).
  const hasGL = (() => { try{ const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); }catch(e){ return false; } })();
  if (hasGL){
    let tries = 0;
    const wait = setInterval(() => {
      if (regions().length || ++tries > 60){ clearInterval(wait); if (regions().length) openView({}); }
    }, 250);
  }

  // Picking a region while the 3D view is open plays NISAR's next real pass over it.
  if (typeof selectRegion === 'function'){
    const orig = selectRegion;
    selectRegion = async function(id){
      const res = orig.apply(this, arguments);
      if (mod && mod.isOpen()){
        const r = regions().find(x => x.id === id);
        if (r) mod.selectRegion(r, {autoplay: true});
      }
      return res;
    };
  }
})();
