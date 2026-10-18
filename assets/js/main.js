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

/* ---------- Modulo contatti ---------- */
(() => {
  const form = document.querySelector('[data-contact-form]');
  if (!form) return;
  const summary = form.querySelector('.error-summary');
  const summaryList = summary.querySelector('ul');
  const success = document.querySelector('[data-contact-success]');

  const rules = {
    nome: (v) => (v.trim() ? '' : 'Scrivi il tuo nome, così so come chiamarti'),
    email: (v) => {
      if (!v.trim()) return 'Scrivi la tua email, così posso risponderti';
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim())) return 'Manca il dominio completo: ad esempio nome@dominio.it';
      return '';
    },
    messaggio: (v) => (v.trim().length >= 10 ? '' : 'Scrivi almeno una riga, così so come aiutarti'),
  };

  const check = (input) => {
    const rule = rules[input.name];
    if (!rule) return '';
    const field = input.closest('.field');
    const help = field.querySelector('.field__help span');
    const msg = rule(input.value);
    if (!help.dataset.default) help.dataset.default = help.textContent;
    if (msg) {
      field.setAttribute('data-invalid', '');
      input.setAttribute('aria-invalid', 'true');
      help.textContent = msg;
    } else {
      field.removeAttribute('data-invalid');
      input.removeAttribute('aria-invalid');
      help.textContent = help.dataset.default;
    }
    return msg;
  };

  // Validazione all'uscita dal campo, non mentre si scrive
  form.querySelectorAll('input[name], textarea[name]').forEach((el) => {
    el.addEventListener('blur', () => { if (el.value) check(el); });
    el.addEventListener('input', () => { if (el.hasAttribute('aria-invalid')) check(el); });
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const errors = [];
    form.querySelectorAll('input[name], textarea[name]').forEach((el) => {
      const msg = check(el);
      if (msg) errors.push({ id: el.id, label: el.closest('.field').querySelector('label').textContent });
    });

    if (errors.length) {
      summaryList.innerHTML = errors.map((x) => `<li><a href="#${x.id}">${x.label}</a></li>`).join('');
      summary.querySelector('strong').textContent =
        errors.length === 1 ? 'Il messaggio non è partito: controlla 1 campo' : `Il messaggio non è partito: controlla ${errors.length} campi`;
      summary.hidden = false;
      summary.focus();
      return;
    }
    summary.hidden = true;

    const data = new FormData(form);
    const endpoint = form.getAttribute('action') || '';
    const submit = form.querySelector('[type="submit"]');

    // Se il servizio del modulo non è ancora configurato, apre il programma di posta
    if (!endpoint || endpoint.includes('TUO_ID')) {
      const to = form.dataset.fallbackEmail;
      const body = `${data.get('messaggio')}\n\n${data.get('nome')} · ${data.get('email')}`;
      window.location.href = `mailto:${to}?subject=${encodeURIComponent('Contatto dal portfolio: ' + data.get('motivo'))}&body=${encodeURIComponent(body)}`;
      return;
    }

    submit.disabled = true;
    submit.textContent = 'Invio in corso…';
    try {
      const res = await fetch(endpoint, { method: 'POST', body: data, headers: { Accept: 'application/json' } });
      if (!res.ok) throw new Error();
      form.hidden = true;
      success.hidden = false;
      success.querySelector('h2').focus();
    } catch {
      submit.disabled = false;
      submit.textContent = 'Invia messaggio';
      summaryList.innerHTML = '';
      summary.querySelector('strong').textContent = 'Il messaggio non è partito per un problema di connessione. Riprova, oppure scrivimi direttamente via email.';
      summary.hidden = false;
      summary.focus();
    }
  });

  // Motivo del contatto: chip a scelta singola
  const motivo = form.querySelector('[data-motivo]');
  const hidden = form.querySelector('input[name="motivo"]');
  motivo?.addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!b) return;
    motivo.querySelectorAll('button').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
    hidden.value = b.textContent.trim();
  });
})();
