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
  const en = document.documentElement.lang === 'en';
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
      btn.textContent = ok ? (en ? 'Copied' : 'Copiato') : (en ? 'Selected' : 'Selezionato');
      if (status) status.textContent = ok ? (en ? 'Email address copied' : 'Indirizzo email copiato') : (en ? 'Address selected: press Cmd or Ctrl + C to copy it' : 'Indirizzo selezionato: premi Cmd o Ctrl + C per copiarlo');
      setTimeout(() => { btn.textContent = label; }, 2000);
    });
  });
})();
