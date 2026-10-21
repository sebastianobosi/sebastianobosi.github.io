/* Motion del brand idealista: comparsa del logo, caricamento, selezione sulla mappa. */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = s => document.querySelector(s);
  let speed = 1, looping = false, anims = [], raf = 0, loopTimer = 0;
  const EASE = 'cubic-bezier(.2,.8,.2,1)'; // ease-out
  const px1 = $('#px1'), px2 = $('#px2'), stemRect = $('#stemRect'), rest = $('#rest');
  const cues = [...document.querySelectorAll('.m-cue')], clock = $('#clock');
  const P = 166; // one pixel module in logo units

  function finalState(){
    anims.forEach(a => a.cancel()); anims = [];
    stemRect.setAttribute('y', -600); stemRect.setAttribute('height', 620);
    px1.style.transform = ''; px1.style.opacity = 1; px2.style.opacity = 1; rest.style.transform = ''; rest.style.opacity = 1;
    cues.forEach(c => c.classList.add('on')); clock.textContent = '1.200 ms';
  }
  function a(el, kf, opt){ const an = el.animate(kf, {fill:'both', ...opt, duration: opt.duration*speed, delay:(opt.delay||0)*speed}); anims.push(an); return an; }

  function play(){
    cancelAnimationFrame(raf); clearTimeout(loopTimer);
    if (reduce){ finalState(); return; }
    anims.forEach(x => x.cancel()); anims = [];
    cues.forEach(c => c.classList.remove('on'));
    // 120 ms: pixel appears 3 modules above and drops one module per step (no easing)
    a(px1, [{transform:`translateY(${-3*P}px)`},{transform:'translateY(0)'}], {delay:120, duration:240, easing:'steps(3, end)'});
    // 240 ms: the i stem builds downward under the pixel (ease-out)
    a(stemRect, [{y:-600, height:0},{y:-600, height:620}], {delay:240, duration:320, easing:EASE});
    // 560 ms: the rest of the wordmark slides out from behind the i (ease-out)
    a(rest, [{transform:'translateX(-2600px)', opacity:1},{transform:'translateX(0)', opacity:1}], {delay:560, duration:320, easing:EASE});
    // second pixel lands in one step at the end
    a(px2, [{opacity:0},{opacity:1}], {delay:880, duration:120, easing:'steps(1, end)'});
    const t0 = performance.now(), total = 1200;
    const tick = now => {
      const t = Math.min((now - t0)/speed, total);
      clock.textContent = Math.round(t).toLocaleString('it-IT') + ' ms';
      cues.forEach(c => c.classList.toggle('on', t >= +c.dataset.t));
      if (t < total) raf = requestAnimationFrame(tick);
      else if (looping) loopTimer = setTimeout(play, 1200*speed);
    };
    raf = requestAnimationFrame(tick);
  }
  // The clip rect's height is an SVG attribute, so it is animated by hand with the same ease-out
  stemRect.animate = function(kf, opt){
    const start = performance.now() + opt.delay;
    const dur = opt.duration;
    const ease = t => 1 - Math.pow(1 - t, 3);
    let id;
    const step = now => {
      const t = Math.max(0, Math.min(1, (now - start)/dur));
      const h = 620*ease(t);
      stemRect.setAttribute('y', -600); stemRect.setAttribute('height', h);
      if (t < 1) id = requestAnimationFrame(step);
    };
    stemRect.setAttribute('height', 0);
    id = requestAnimationFrame(step);
    return { cancel(){ cancelAnimationFrame(id); } };
  };

  $('#play1').addEventListener('click', play);
  $('#slow').addEventListener('click', e => { speed = speed === 1 ? 4 : 1; e.currentTarget.setAttribute('aria-pressed', speed !== 1); play(); });
  $('#loop').addEventListener('click', e => { looping = !looping; e.currentTarget.setAttribute('aria-pressed', looping); if (looping) play(); else clearTimeout(loopTimer); });

  // Loader grid: snake order, one module per 90 ms, stepped
  const grid = $('#grid'), cells = [];
  for (let i = 0; i < 15; i++){ const c = document.createElement('i'); grid.appendChild(c); cells.push(c); }
  const order = [0,1,2,3,4,9,8,7,6,5,10,11,12,13,14];
  if (reduce){ order.slice(0,9).forEach(i => cells[i].classList.add('lit')); }
  else { let k = 0; setInterval(() => { const n = k % (order.length + 4); cells.forEach(c => c.classList.remove('lit')); order.slice(Math.max(0,n-4), Math.min(n, order.length)).forEach(i => cells[i].classList.add('lit')); k++; }, 90); }

  // Map: tap to select; demo cursor cycles when idle
  const pins = [...document.querySelectorAll('.m-pin')], cursor = $('#cursor'), stage = $('#mapStage');
  let idle = true;
  const select = p => pins.forEach(x => x.classList.toggle('sel', x === p));
  pins.forEach(p => p.addEventListener('click', () => { idle = false; select(p); }));
  if (!reduce){
    let j = 1;
    setInterval(() => {
      if (!idle) return;
      const p = pins[j % pins.length], r = p.getBoundingClientRect(), s = stage.getBoundingClientRect();
      cursor.animate([{opacity:0, transform:`translate(${r.left - s.left + 20}px, ${r.top - s.top + 30}px) scale(1.4)`},{opacity:1, transform:`translate(${r.left - s.left + 20}px, ${r.top - s.top + 14}px) scale(1)`},{opacity:0, transform:`translate(${r.left - s.left + 20}px, ${r.top - s.top + 14}px) scale(.8)`}], {duration:600, easing:EASE});
      setTimeout(() => select(p), 320);
      j++;
    }, 1800);
  } else { select(pins[1]); }

  // initial: show the reveal once on load, but the page is complete at rest after 1.2 s
  finalState();
  if (!reduce && 'IntersectionObserver' in window){
    const io = new IntersectionObserver(es => { if (es.some(e => e.isIntersecting)){ io.disconnect(); setTimeout(play, 200); } }, {threshold: .5});
    io.observe($('#stage1'));
  }
})();
