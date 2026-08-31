() => {
  const rect = e => {
    const r = e.getBoundingClientRect();
    return {left:r.left+scrollX, top:r.top+scrollY, right:r.right+scrollX, bottom:r.bottom+scrollY, width:r.width, height:r.height};
  };
  const name = e => e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+(e.className&&typeof e.className==='string'?'.'+e.className.trim().replace(/\s+/g,'.'):'');
  const styles = e => {
    const c=getComputedStyle(e);
    return {display:c.display,overflowX:c.overflowX,overflowY:c.overflowY,clip:c.clip,clipPath:c.clipPath,maskImage:c.maskImage,contain:c.contain,objectFit:c.objectFit,aspectRatio:c.aspectRatio,transform:c.transform,background:c.backgroundColor,border:c.border,borderRadius:c.borderRadius,boxShadow:c.boxShadow,padding:[c.paddingTop,c.paddingRight,c.paddingBottom,c.paddingLeft],margin:[c.marginTop,c.marginRight,c.marginBottom,c.marginLeft],gap:c.gap,gridTemplateColumns:c.gridTemplateColumns};
  };
  const images=Array.from(document.images).map((e,i)=>{
    const r=rect(e); const ancestors=[];
    for(let p=e.parentElement;p;p=p.parentElement) {
      const s=getComputedStyle(p);
      ancestors.push({element:name(p),...rect(p),display:s.display,overflowX:s.overflowX,overflowY:s.overflowY,clip:s.clip,clipPath:s.clipPath,maskImage:s.maskImage,contain:s.contain});
    }
    const visible=r.width>0&&r.height>0&&ancestors.every(a=>a.display!=='none');
    const clipping=visible?ancestors.filter(a=>((['hidden','clip','scroll','auto'].includes(a.overflowX))&&(r.left<a.left-.5||r.right>a.right+.5))||((['hidden','clip','scroll','auto'].includes(a.overflowY))&&(r.top<a.top-.5||r.bottom>a.bottom+.5))||a.clipPath!=='none'||a.maskImage!=='none'||a.clip!=='auto'):[];
    return {index:i,element:name(e),src:e.getAttribute('src'),currentSrc:e.currentSrc,alt:e.alt,naturalWidth:e.naturalWidth,naturalHeight:e.naturalHeight,complete:e.complete,visible,...r,...styles(e),ratioError:visible&&e.naturalHeight?Math.abs(r.width/r.height-e.naturalWidth/e.naturalHeight):0,parent:{...ancestors[0]},ancestors,clipping:clipping.map(a=>({...a}))};
  });
  const sections={};
  document.querySelectorAll('main>section,body>footer').forEach(e=>{
    const r=rect(e);if(!r.height)return;
    const containers=Array.from(e.querySelectorAll('.hero-content,.hero-actions,.benefit-list,.benefit-desktop-list,.frontline-diagram,.field-grid,.career-grid,.career-note,.career-details,.people-panel,.flow-grid,.final-copy,.final-line')).filter(x=>rect(x).height).map(x=>({element:name(x),...rect(x),...styles(x),children:Array.from(x.children).map(c=>({element:name(c),...rect(c)}))}));
    sections[e.classList[0]]={...r,...styles(e),containers};
  });
  return {viewport:{width:innerWidth,height:innerHeight,dpr:devicePixelRatio,scrollWidth:document.documentElement.scrollWidth,clientWidth:document.documentElement.clientWidth,pageHeight:document.documentElement.scrollHeight,scrollY},fonts:document.fonts.status,sections,images,links:Array.from(document.querySelectorAll('a')).map(e=>({text:e.getAttribute('aria-label')||e.innerText||e.querySelector('img')?.alt,href:e.getAttribute('href')})),overflowElements:Array.from(document.querySelectorAll('body *')).filter(e=>{const r=rect(e);return r.width>0&&(r.left<-.5||r.right>innerWidth+.5)&&!e.classList.contains('visually-hidden');}).map(e=>({element:name(e),...rect(e)}))};
}
