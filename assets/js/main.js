/* Sebastiano Bosi — Portfolio. Nessuna dipendenza. */

/* ---------- Menu mobile ---------- */
(() => {
  const btn = document.querySelector('[data-menu-open]');
  const menu = document.getElementById('menu');
  if (!btn || !menu) return;
  const close = menu.querySelector('[data-menu-close]');
  let lastFocus = null;

  const open = () => {
    lastFocus = document.activeElement;
    menu.hidden = false;
    btn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
    close.focus();
  };
  const shut = () => {
    menu.hidden = true;
    btn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
    (lastFocus || btn).focus();
  };

  btn.addEventListener('click', open);
  close.addEventListener('click', shut);
  menu.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') shut();
    if (e.key !== 'Tab') return;
    const items = menu.querySelectorAll('a, button');
    const first = items[0], last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });
  menu.querySelectorAll('a').forEach((a) => a.addEventListener('click', shut));
})();

/* ---------- Provino: il fotogramma scelto va nel telefono ---------- */
(() => {
  const sheet = document.querySelector('.contact-sheet');
  const img = document.querySelector('[data-frame-img]');
  const caption = document.querySelector('[data-frame-caption]');
  if (!sheet || !img || !caption) return;
  sheet.addEventListener('click', (e) => {
    const b = e.target.closest('button[data-frame]');
    if (!b || b.getAttribute('aria-pressed') === 'true') return;
    sheet.querySelectorAll('button').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
    const next = new Image();
    next.src = b.dataset.frame;
    const swap = () => {
      img.src = b.dataset.frame;
      img.alt = b.dataset.alt;
      img.classList.remove('is-swapping');
    };
    img.classList.add('is-swapping');
    setTimeout(() => (next.complete ? swap() : next.addEventListener('load', swap, { once: true })), 200);
    caption.innerHTML = '';
    const a = document.createElement('a');
    a.href = b.dataset.href;
    a.textContent = b.dataset.caption;
    caption.appendChild(a);
  });
})();

/* ---------- Entrata delle sezioni: titolo, poi testo, poi immagini ---------- */
(() => {
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const sel = [
    '.work-head > *', '.work-block__visual', '.work-block__cluster > *',
    '.method-head > *', '.poster li', '.about__side > *', '.about__text > *', '.record > div',
    '.section-head > *', '.brief > div', '.stat', '.steps li', '.figure', '.callout', '.lessons > div',
    '.split > *', '.brand-tile', '.swatch', '.type-card', '.ucicon', '.id-icon', '.areas',
    '.next > *', '.timeline li', '.chips', '.contact', '.footer__invite > *', '.footer__links'
  ].join(',');
  const els = [...document.querySelectorAll(sel)].filter((el) => !el.closest('.hero, .menu, .intro'));
  const io = new IntersectionObserver((entries) => {
    entries.filter((en) => en.isIntersecting).forEach((en, i) => {
      en.target.style.transitionDelay = `${Math.min(i, 6) * 75}ms`;
      en.target.classList.add('is-in');
      io.unobserve(en.target);
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  els.forEach((el) => { el.classList.add('reveal'); io.observe(el); });
  // rete di sicurezza: in fondo alla pagina non deve restare nulla nascosto
  const atEnd = () => {
    if (scrollY + innerHeight < document.documentElement.scrollHeight - 4) return;
    document.querySelectorAll('.reveal:not(.is-in)').forEach((el) => el.classList.add('is-in'));
    removeEventListener('scroll', atEnd);
  };
  addEventListener('scroll', atEnd, { passive: true });
})();

/* ---------- Video in loop: parte solo quando si vede, mai con «riduci movimento» ---------- */
(() => {
  const vids = document.querySelectorAll('video[data-autoplay]');
  if (!vids.length || !('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      const v = en.target;
      if (en.isIntersecting) { v.preload = 'auto'; v.play().catch(() => {}); } else { v.pause(); }
    });
  }, { threshold: 0.25 });
  vids.forEach((v) => io.observe(v));
})();

/* ---------- Copia indirizzo email ---------- */
(() => {
  const status = document.querySelector('[data-copy-status]');
  document.querySelectorAll('[data-copy]').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const text = btn.dataset.copy;
      let ok = false;
      try { await navigator.clipboard.writeText(text); ok = true; } catch {
        // Ripiego: seleziona l'indirizzo, così si copia con Cmd/Ctrl+C
        const el = btn.closest('.contact').querySelector('.contact__value');
        const r = document.createRange(); r.selectNodeContents(el);
        const sel = getSelection(); sel.removeAllRanges(); sel.addRange(r);
      }
      const label = btn.textContent;
      btn.textContent = ok ? 'Copiato' : 'Selezionato';
      if (status) status.textContent = ok ? 'Indirizzo email copiato' : 'Indirizzo selezionato: premi Cmd o Ctrl + C per copiarlo';
      setTimeout(() => { btn.textContent = label; }, 2000);
    });
  });
})();
