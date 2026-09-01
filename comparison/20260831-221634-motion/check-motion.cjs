const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../../script.js'), 'utf8');
const results = [];
function check(name, run) { run(); results.push({ name, result: 'PASS' }); }
function element() {
  const attrs = {}, classes = new Set(), handlers = {}, styles = {};
  return { attrs, classes, handlers, styles, inert: false,
    classList: { add: (...names) => names.forEach(n => classes.add(n)) },
    style: { setProperty: (k,v) => { styles[k] = v; } },
    setAttribute: (k,v) => { attrs[k] = v; },
    getAttribute: k => attrs[k], removeAttribute: k => { delete attrs[k]; },
    addEventListener: (k,f) => { handlers[k] = f; },
    getClientRects: () => [{}], querySelector: () => ({ alt: '既存先輩のコピー' }),
    focus() {}, setPointerCapture() {}, hasPointerCapture: () => false
  };
}
function setup({ reduced = false, io = true, mobile = true } = {}) {
  const panel = element(), track = element(), section = element(), status = element(), pagination = element();
  const slides = [element(), element()], dots = [element(), element()], target = element(), hero = [element(), element()];
  const media = { matches: mobile, addEventListener(k,fn) { this.change = fn; } };
  const motion = { matches: reduced, addEventListener(k,fn) { this.change = fn; } };
  track.querySelectorAll = () => slides;
  panel.querySelectorAll = () => slides;
  section.querySelector = s => ({ '.people-panel': panel, '.people-track': track, '.people-status': status, '.people-pagination': pagination })[s];
  section.querySelectorAll = () => dots;
  const observers = [];
  class Observer {
    constructor(fn, options) { this.fn = fn; this.options = options; this.observed = new Set(); this.removed = new Set(); observers.push(this); }
    observe(e) { this.observed.add(e); }
    unobserve(e) { this.observed.delete(e); this.removed.add(e); }
    disconnect() { this.observed.clear(); this.disconnected = true; }
  }
  const document = {
    readyState: 'complete', addEventListener() {},
    querySelector: s => ({ '.people': section, '.people-panel': panel })[s] || null,
    querySelectorAll: s => s.startsWith('.brand,') ? hero : s === '.benefit-card' ? [target] : []
  };
  const window = { matchMedia: q => q.includes('reduced-motion') ? motion : media };
  if (io) window.IntersectionObserver = Observer;
  vm.runInNewContext(source, { window, document, IntersectionObserver: Observer, requestAnimationFrame: fn => fn() });
  const pointer = (x,y,extra={}) => ({ clientX:x, clientY:y, pointerId:1, isPrimary:true, button:0, ...extra });
  const swipe = (dx,dy=0) => { panel.handlers.pointerdown(pointer(200,200)); panel.handlers.pointerup(pointer(200+dx,200+dy)); };
  return { panel, track, slides, dots, status, target, hero, media, motion, observers, swipe, pointer, pagination };
}
check('Reduced motion skips IntersectionObserver and hidden reveal state', () => {
  const t = setup({reduced:true}); assert.equal(t.observers.length,0); assert.equal(t.target.classes.has('reveal'),false);
  t.swipe(-100); assert.equal(t.dots[1].attrs['aria-current'],'true');
});
check('Missing IntersectionObserver leaves readable content and working carousel', () => {
  const t=setup({io:false}); assert.equal(t.observers.length,0); assert.equal(t.target.classes.has('reveal'),false); t.swipe(-100); assert.equal(t.dots[1].attrs['aria-current'],'true');
});
check('Reveal runs once and unobserves intersecting target', () => {
  const t=setup(), o=t.observers[0]; assert.equal(o.options.threshold,.15); assert.equal(t.target.classes.has('is-visible'),false);
  o.fn([{target:t.target,isIntersecting:true}]); assert.equal(t.target.classes.has('is-visible'),true); assert.equal(o.removed.has(t.target),true);
  o.fn([{target:t.target,isIntersecting:false}]); assert.equal(t.target.classes.has('is-visible'),true);
  t.hero.forEach(e=>assert.equal(e.classes.has('is-visible'),true));
});
check('Changing to reduced motion disconnects observation and reveals all', () => {
  const t=setup(); t.motion.change({matches:true}); assert.equal(t.observers[0].disconnected,true); assert.equal(t.target.classes.has('is-visible'),true);
});
check('Pointer swipe, short gesture, vertical gesture, cancellation and looping', () => {
  const t=setup(); t.swipe(-49); assert.equal(t.dots[0].attrs['aria-current'],'true');
  t.swipe(-70,100); assert.equal(t.dots[0].attrs['aria-current'],'true');
  t.panel.handlers.pointerdown(t.pointer(200,200)); t.panel.handlers.pointercancel(); t.panel.handlers.pointerup(t.pointer(50,200)); assert.equal(t.dots[0].attrs['aria-current'],'true');
  t.swipe(-60); assert.equal(t.dots[1].attrs['aria-current'],'true'); assert.equal(t.slides[0].inert,true); assert.equal(t.slides[1].inert,false);
  t.swipe(-60); assert.equal(t.dots[0].attrs['aria-current'],'true'); t.swipe(60); assert.equal(t.dots[1].attrs['aria-current'],'true');
});
check('Dot click, keyboard and desktop breakpoint keep correct state', () => {
  const t=setup(); t.dots[1].handlers.click(); assert.equal(t.dots[1].attrs['aria-current'],'true');
  t.pagination.handlers.keydown({key:'Home',preventDefault(){}}); assert.equal(t.dots[0].attrs['aria-current'],'true');
  t.pagination.handlers.keydown({key:'ArrowRight',preventDefault(){}}); assert.equal(t.dots[1].attrs['aria-current'],'true');
  t.media.matches=false; t.media.change(); t.slides.forEach(s=>{assert.equal(s.inert,false); assert.equal(s.attrs['aria-hidden'],undefined);});
  assert.equal(t.track.styles['--people-index'],0); t.swipe(-100); assert.equal(t.track.styles['--people-index'],0);
});
check('No autoplay timer, no external animation dependencies', () => {
  assert.equal(/setInterval|setTimeout|gsap|swiper/i.test(source),false);
});
console.log(JSON.stringify(results,null,2));
