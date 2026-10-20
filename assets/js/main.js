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

/* ---------- Filtri della pagina Lavori ---------- */
(() => {
  const bar = document.querySelector('[data-filters]');
  if (!bar) return;
  const cards = document.querySelectorAll('[data-tags]');
  const status = document.querySelector('[data-filter-status]');
  bar.addEventListener('click', (e) => {
    const b = e.target.closest('button[data-filter]');
    if (!b) return;
    bar.querySelectorAll('button').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
    const f = b.dataset.filter;
    let n = 0;
    cards.forEach((c) => {
      const show = f === 'tutti' || c.dataset.tags.split(' ').includes(f);
      c.hidden = !show;
      if (show) n++;
    });
    if (status) status.textContent = n === 1 ? '1 progetto' : `${n} progetti`;
  });
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
