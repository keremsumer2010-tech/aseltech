// Atlas <-> NISAR 3D orbit view bridge (PC1). Uses the globals atlasData, activeId and
// selectRegion from atlas.js (loaded before this file). The 3D module loads on first use.
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
  const current = () => {
    const regs = (typeof atlasData !== 'undefined' && atlasData?.regions) || [];
    const id = (typeof activeId !== 'undefined' && activeId) || regs[0]?.id;
    return regs.find(r => r.id === id) || null;
  };

  btn.addEventListener('click', async () => {
    btn.disabled = true;
    try{
      mod = mod || await import('./nisar3d.js?v=13');
      await mod.open(wrap, current());
    }catch(e){ console.error('NISAR 3D failed to load', e); }
    btn.disabled = false;
  });

  if (typeof selectRegion === 'function'){
    const orig = selectRegion;
    selectRegion = async function(id){
      const res = orig.apply(this, arguments);
      if (mod && mod.isOpen()){
        const r = (atlasData?.regions || []).find(x => x.id === id);
        if (r) mod.selectRegion(r);
      }
      return res;
    };
  }
})();
