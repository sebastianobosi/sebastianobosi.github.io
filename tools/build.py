#!/usr/bin/env python3
"""Genera le pagine HTML del portfolio a partire da parti condivise.

Uso:  python3 tools/build.py            (rigenera le pagine nella cartella del sito)
Le pagine usano link relativi, quindi funzionano su GitHub Pages, in locale e in anteprima.
Per cambiare email, LinkedIn o CV, modifica CONFIG qui sotto e rigenera.
"""
import sys, os, shutil, html, hashlib

CONFIG = {
    "site_url": "https://sebastianobosi.github.io",
    "name": "Sebastiano Bosi",
    "email": "nome@dominio.it",                     # TODO: la tua email
    "linkedin": "https://www.linkedin.com/",        # TODO: il tuo profilo
    "cv": "assets/sebastiano-bosi-cv.pdf",          # TODO: carica il PDF con questo nome
}

ICONS = {
    "arrow-up-right": '<path d="M7 17 17 7M8 7h9v9"/>',
    "arrow-left": '<path d="M19 12H5m6-6-6 6 6 6"/>',
    "arrow-up": '<path d="M12 19V5m-6 6 6-6 6 6"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6 6 18"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "layout": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M3 9h18M9 21V9"/>',
    "components": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    "accessibility": '<circle cx="12" cy="4.5" r="1.5"/><path d="M5 8.5 12 10l7-1.5M12 10v4m0 0-3 6m3-6 3 6"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>',
        }

def icon(name, size=None):
    s = f' style="width:{size}px;height:{size}px"' if size else ""
    return f'<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"{s}>{ICONS[name]}</svg>'

NAV = [("Lavori", "lavori/"), ("Metodo", "#metodo"), ("Chi sono", "chi-sono/")]

def asset_version():
    """Breve impronta di CSS e JS: cambia a ogni modifica, così il browser non usa la versione vecchia."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    h = hashlib.sha1()
    for f in ("assets/css/style.css", "assets/js/main.js"):
        h.update(open(os.path.join(root, f), "rb").read())
    return h.hexdigest()[:8]

def layout(page, depth, title, description, body, glows, extra_head=""):
    r = "../" * depth
    v = asset_version()
    def href(p):
        if p.startswith("#"):
            return (r or "./") + p if depth else p
        return r + p
    links = "".join(
        f'<li><a href="{href(p)}"{" aria-current=\"page\"" if page == p else ""}>{label}</a></li>'
        for label, p in NAV
    )
    menu_links = "".join(
        f'<li><a href="{href(p)}"{" aria-current=\"page\"" if page == p else ""}>{label}{icon("arrow-up-right")}</a></li>'
        for label, p in NAV + [("Contatti", "contatti/")]
    )
    glow_html = "".join(
        f'<div class="glow glow--{c}" style="left:{x};top:{y};width:{w};height:{h};opacity:{o}"></div>'
        for c, x, y, w, h, o in glows
    )
    full_title = f"{title} — {CONFIG['name']}" if title != CONFIG["name"] else f"{CONFIG['name']} — Product designer"
    canonical = CONFIG["site_url"] + "/" + ("" if page == "" else page)
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{CONFIG['site_url']}/assets/img/og.png">
<meta name="theme-color" content="#07080f">
<link rel="icon" href="{r}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&display=swap">
<link rel="stylesheet" href="{r}assets/css/style.css?v={v}">
<script src="{r}assets/js/main.js?v={v}" defer></script>
{extra_head}</head>
<body>
<a class="skip-link" href="#contenuto">Vai al contenuto</a>
<div class="glows" aria-hidden="true">{glow_html}</div>

<header class="site-header">
  <div class="wrap">
    <nav class="nav glass" aria-label="Principale">
      <a class="nav__logo" href="{r or './'}">{CONFIG['name']}</a>
      <ul class="nav__links">{links}</ul>
      <a class="btn btn--primary nav__cta" href="{r}contatti/">Contattami</a>
      <button class="nav__menu-btn" type="button" data-menu-open aria-expanded="false" aria-controls="menu" aria-label="Apri il menu">{icon("menu")}</button>
    </nav>
  </div>
</header>

<div class="menu" id="menu" hidden role="dialog" aria-modal="true" aria-label="Menu">
  <div class="nav glass menu__bar">
    <a class="nav__logo" href="{r or './'}">{CONFIG['name']}</a>
    <button class="nav__menu-btn" type="button" data-menu-close aria-label="Chiudi il menu">{icon("close")}</button>
  </div>
  <ul class="menu__list">{menu_links}</ul>
  <div class="actions">
    <a class="btn btn--primary" href="{r}contatti/">Contattami</a>
    <a class="btn btn--secondary" href="{r}{CONFIG['cv']}" download>Scarica il CV</a>
  </div>
</div>

<main id="contenuto">
{body}
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer">
      <p class="muted">© 2026 {CONFIG['name']}</p>
      <nav aria-label="Contatti"><ul>
        <li><a href="{CONFIG['linkedin']}" rel="me noopener" target="_blank">LinkedIn</a></li>
        <li><a href="mailto:{CONFIG['email']}">Email</a></li>
        <li><a href="{r}{CONFIG['cv']}" download>CV</a></li>
      </ul></nav>
      <a href="#contenuto">Torna su {icon("arrow-up", 16)}</a>
    </div>
  </div>
</footer>
</body>
</html>
"""

def phone(label, img=None, alt=""):
    inner = f'<img src="{img}" alt="{html.escape(alt)}" loading="lazy">' if img else f'<span class="placeholder">{label}</span>'
    return f'<div class="phone"><div class="phone__screen">{inner}</div></div>'

def media(label, cls="project__media", img=None, alt=""):
    inner = f'<img src="{img}" alt="{html.escape(alt)}" loading="lazy">' if img else f'<span class="placeholder">{label}</span>'
    return f'<div class="{cls}">{inner}</div>'

PROJECTS = [
    dict(slug="lavori/uci-cinemas/", title="UCI Cinemas", eyebrow="Case study · App mobile · 2026",
         desc="Il redesign dell’app: biglietti in pochi tocchi e Iris, l’assistente che sceglie il film con te.",
         media="Schermate UCI: Home, Iris, biglietto", tags="app design-system", large=True, cta="Leggi il case study",
         img="assets/img/uci-cover.webp", alt="Iris, la mascotte gialla dell’app, sopra il logo UCI Cinemas e il claim «Il cinema, a modo tuo»"),
    dict(slug="lavori/jet-hr/", title="Jet HR", eyebrow="Case study · Web app e iOS · 2026",
         desc="L’area dipendente e una busta paga che si capisce, su desktop e iPhone.", media="Jet HR: web app e app iOS",
         tags="web app design-system", large=False, cta="Leggi il case study",
         img="assets/img/jethr-cover.webp", alt="La home di Jet HR su desktop e su iPhone, con lo stipendio nascosto e la data di accredito"),
    dict(slug=None, title="Progetto tre", eyebrow="Segnaposto · Categoria · Anno",
         desc="Una riga con il problema risolto e il risultato ottenuto.", media="Immagine del progetto",
         tags="design-system", large=False, cta="In arrivo"),
]

def project_card(p, r, heading="h3"):
    href = (r + p["slug"]) if p["slug"] else None
    title = f'<a href="{href}">{p["title"]}</a>' if href else p["title"]
    link = (f'<a class="link" href="{href}" tabindex="-1" aria-hidden="true">{p["cta"]}{icon("arrow-up-right", 18)}</a>'
            if href else f'<span class="label">{p["cta"]}</span>')
    cls = "project glass" + (" project--large" if p["large"] else "")
    return f"""<article class="{cls}" data-tags="{p['tags']}">
  <div class="project__text">
    <p class="label">{p['eyebrow']}</p>
    <{heading}>{title}</{heading}>
    <p class="{'lead' if p['large'] else 'muted'}">{p['desc']}</p>
    {link if p['large'] else ''}
  </div>
  {media(p['media'], img=(r + p['img']) if p.get('img') else None, alt=p.get('alt', ''))}
  {'' if p['large'] else link}
</article>"""

SERVICES = [
    ("search", "Ricerca UX", "Interviste, mappe delle assunzioni e test per partire dal problema giusto."),
    ("layout", "Interfacce e prototipi", "Flussi completi, con stati di errore, vuoti e offline, prototipati prima dello sviluppo."),
    ("components", "Design system", "Token, componenti e regole documentate, con un changelog che allinea design e codice."),
    ("accessibility", "Accessibilità", "Contrasti, aree di tocco e screen reader verificati sulle WCAG 2.2 dal primo componente."),
]

def services_html(items=SERVICES):
    return '<div class="grid grid--4">' + "".join(
        f'<article class="card glass service"><div class="service__icon">{icon(i)}</div><h3>{t}</h3><p class="muted">{d}</p></article>'
        for i, t, d in items) + "</div>"

SKILLS = ["UX research", "Interfacce", "Design system", "Accessibilità WCAG 2.2", "Prototipi", "AI conversazionale", "Figma"]

def chips(items):
    return '<ul class="chips">' + "".join(f'<li class="chip">{s}</li>' for s in items) + "</ul>"

def timeline(items):
    return '<ul class="timeline">' + "".join(
        f'<li class="glass"><span><strong>{a}</strong><span class="label">{b}</span></span><span class="label">{c}</span></li>'
        for a, b, c in items) + "</ul>"

# ---------------------------------------------------------------------------
# Pagine
# ---------------------------------------------------------------------------
def home():
    r = ""
    cards = "".join(project_card(p, r) for p in PROJECTS)
    body = f"""
<div class="wrap">
  <section class="hero" aria-labelledby="titolo">
    <div class="hero__text intro">
      <p class="chip chip--status">Product designer · Portfolio 2026–27</p>
      <h1 id="titolo" class="display hero__title">Interfacce chiare per prodotti complessi.</h1>
      <p class="lead">Ricerca, UI e design system: porto i prodotti dal problema giusto a componenti accessibili, pronti per lo sviluppo.</p>
      <div class="actions actions--stack-mobile">
        <a class="btn btn--primary" href="#lavori">Guarda i lavori</a>
        <a class="btn btn--secondary" href="chi-sono/">Chi sono</a>
      </div>
    </div>
    <div class="phones" role="img" aria-label="Schermate dai progetti: la home dell’app UCI Cinemas, la home dell’app Jet HR e l’assistente Iris di UCI">
      {phone("UCI · Home", "assets/img/uci-home.webp")}{phone("Jet HR · Home", "assets/img/jethr-m-home.webp")}{phone("UCI · Iris", "assets/img/iris-benvenuto.webp")}
    </div>
  </section>

  <section class="section" id="lavori" aria-labelledby="lavori-titolo">
    <div class="section-head"><h2 id="lavori-titolo" class="h2">Lavori selezionati</h2><p class="label">3 progetti</p></div>
    <div class="projects">{cards}</div>
  </section>

  <section class="section" id="metodo" aria-labelledby="metodo-titolo">
    <div class="section-head"><h2 id="metodo-titolo" class="h2">Come lavoro</h2><p class="label">Dal problema al componente</p></div>
    {services_html()}
  </section>

  <section class="section" aria-labelledby="chi-titolo">
    <div class="grid grid--2" style="align-items:start">
      <div class="card glass stack" style="--gap:24px;border-radius:var(--r-card);padding:clamp(24px,3.4vw,48px)">
        <div class="phone__screen" style="width:80px;height:80px;border-radius:50%;border:1px solid var(--border-glass)" role="img" aria-label="Foto di Sebastiano (da inserire)"></div>
        <h2 id="chi-titolo" class="h3">Ciao, sono Sebastiano.</h2>
        <p class="lead">[Racconta in due o tre righe il tuo percorso, cosa ti appassiona del design e che tipo di lavoro cerchi.]</p>
        <div class="actions actions--stack-mobile">
          <a class="btn btn--primary" href="{CONFIG['cv']}" download>Scarica il CV</a>
          <a class="btn btn--secondary" href="chi-sono/">Più su di me</a>
        </div>
      </div>
      <div class="stack" style="--gap:12px">
        <h3 class="h4">Esperienza e formazione</h3>
        {timeline([("[Ruolo]", "[Azienda o scuola]", "[Anno – Anno]")]*4)}
      </div>
    </div>
  </section>

  <section class="section" aria-label="Competenze">{chips(SKILLS).replace('class="chips"', 'class="chips chips--center"')}</section>

  <section class="closing" aria-labelledby="contatti-titolo">
    <h2 id="contatti-titolo" class="display">Lavoriamo insieme.</h2>
    <p class="lead">Hai un progetto o una posizione aperta? Scrivimi.</p>
    <div class="actions actions--stack-mobile">
      <a class="btn btn--primary" href="contatti/">Scrivimi</a>
      <a class="btn btn--secondary" href="{CONFIG['linkedin']}" rel="me noopener" target="_blank">LinkedIn</a>
    </div>
  </section>
</div>"""
    glows = [("blue", "-14%", "-260px", "62vw", "700px", .5), ("lavender", "52%", "-140px", "56vw", "620px", .32),
             ("warm", "66%", "520px", "30vw", "360px", .26), ("blue", "-18%", "1400px", "60vw", "700px", .2),
             ("lavender", "20%", "calc(100% - 900px)", "62vw", "520px", .18)]
    return layout("", 0, CONFIG["name"], "Portfolio di Sebastiano Bosi, product designer: ricerca, interfacce e design system. Case study UCI Cinemas e Jet HR.", body, glows)

def lavori():
    r = "../"
    cards = "".join(project_card(p, r, "h2") for p in PROJECTS)
    body = f"""
<div class="wrap">
  <section class="intro" style="padding-top:clamp(72px,8vw,120px);display:grid;gap:20px;justify-items:start">
    <h1 class="display">Lavori</h1>
    <p class="lead">Progetti di ricerca, interfacce e design system, dal problema al prodotto finito.</p>
    <div class="chips" data-filters role="group" aria-label="Filtra i progetti">
      <button class="chip" type="button" data-filter="tutti" aria-pressed="true">Tutti</button>
      <button class="chip" type="button" data-filter="app" aria-pressed="false">App mobile</button>
      <button class="chip" type="button" data-filter="web" aria-pressed="false">Web</button>
      <button class="chip" type="button" data-filter="design-system" aria-pressed="false">Design system</button>
    </div>
    <p class="visually-hidden" aria-live="polite" data-filter-status>3 progetti</p>
  </section>
  <div class="projects" style="margin-top:48px">{cards}</div>
  <section class="section band glass" aria-labelledby="altri">
    <div class="stack" style="--gap:8px"><h2 id="altri" class="h3">Vuoi vedere altri lavori?</h2>
    <p class="lead">Ti racconto volentieri anche i progetti che non trovano spazio qui.</p></div>
    <a class="btn btn--primary" href="../contatti/">Scrivimi</a>
  </section>
</div>"""
    glows = [("blue", "-14%", "-240px", "62vw", "620px", .42), ("lavender", "55%", "-160px", "56vw", "520px", .3), ("blue", "-10%", "900px", "50vw", "500px", .18)]
    return layout("lavori/", 1, "Lavori", "Progetti di Sebastiano Bosi: ricerca UX, interfacce e design system.", body, glows)

def uci():
    r = "../../"
    stats = [("85", "schermate, con percorsi principali e stati alternativi"), ("9", "aree, dal primo accesso al profilo e fedeltà"),
             ("AA", "contrasti WCAG 2.2 verificati in tema Blue e Dark"), ("1", "assistente AI, Iris, al posto dell’acquisto rapido")]
    steps = [("search", "Discovery", "Problema riformulato e assunzioni mappate prima di disegnare qualsiasi schermata."),
             ("components", "Brand e design system", "Nuova identità, token e componenti con varianti, stati e changelog."),
             ("layout", "Flussi", "85 schermate: percorso principale, errori, vuoti, offline e caricamento per ogni area."),
             ("accessibility", "Accessibilità", "Revisione WCAG 2.2 AA in Blue e Dark, con le correzioni registrate nel design system.")]
    areas = ["Onboarding e accesso", "Home", "Acquisto classico", "Acquisto con Iris", "I miei biglietti", "Ordina al bar", "Film", "Cinema", "Profilo e fedeltà"]
    rules = ["Barre flottanti sopra il contenuto (Tab Bar, riepilogo, azioni), con sfumatura al bordo di scorrimento.",
             "Raggi annidati: raggio esterno = raggio interno + padding, con angoli smussati al 100%.",
             "Icone a tratto singolo; nei Bottom Sheet le azioni stanno sempre nel footer."]
    acc = [("2,10:1", "Rosso su blu negli errori: illeggibile, prima della correzione"), ("4,82:1", "Dopo: in tema Blue gli errori usano red/300"), ("44 pt", "Altezza minima del selettore cinema, prima era 36")]
    next_p = dict(PROJECTS[1]); next_p["large"] = True; next_p["eyebrow"] = "Prossimo progetto · Web app e iOS · 2026"
    img = r + "assets/img/"
    palette = [("#3433FF", "Brand", "Sfondo principale e tema Blue", "#FEFEFE"), ("#FFDA33", "Accento", "Ellisse, azioni principali, Iris", "#272727"),
               ("#FEFEFE", "Superfici", "Testi e superfici chiare", "#3433FF"), ("#272727", "Inchiostro", "Testi su giallo e tema Dark", "#FFDA33"),
               ("#010073", "Profondo", "Card e livelli in profondità", "#CCECFF"), ("#33B4FF", "Luce", "Informazioni e stati attivi", "#010073"),
               ("#CCECFF", "Tenue", "Testi secondari su blu", "#3433FF")]
    ucicons = [("ellisse", "L’ellisse che sbuca dal buco: il simbolo in movimento"), ("occhi", "Gli occhi: guardare il cinema meglio"),
               ("popcorn", "Il popcorn a righe del bar"), ("cinepresa", "La cinepresa"), ("maschere", "Le maschere del teatro"), ("biglietto", "Il biglietto")]
    film_scenes = ["Iris sbuca da un buco nero, salta fuori e si presenta.", "Il manifesto «Watching movies better» con gli occhi delle ucicons.",
                   "Il logo e le sue varianti su bianco, nero e giallo, poi il simbolo da solo.", "La palette: sette colori con codice e ruolo.",
                   "La tipografia: Rubik per i titoli, Outfit per i testi.", "Le sei ucicons animate.",
                   "L’app in una serata: chiedi a Iris, lei cerca e trova il film, scegli i posti, confermi tu il pagamento, entri con il QR, ordini al bar senza fila e guadagni punti myUCI.",
                   "Chiusura: Iris, il logo e «Il cinema, a modo tuo»."]
    body = f"""
<div class="wrap">
  <p style="margin-top:clamp(32px,4vw,48px)"><a class="back" href="../">{icon("arrow-left", 18)} Tutti i lavori</a></p>
  <section class="intro" style="display:grid;gap:clamp(20px,2vw,28px);justify-items:start;padding-top:16px" aria-labelledby="titolo">
    <p class="chip chip--status">Case study · App mobile · 2026</p>
    <h1 id="titolo" class="display">UCI Cinemas</h1>
    <p class="lead" style="max-width:720px">Il redesign dell’app per comprare biglietti, ordinare al bar e farsi consigliare da Iris, un’assistente AI.</p>
    <dl class="meta">
      <div><dt>Ruolo</dt><dd>Product designer · progetto personale</dd></div>
      <div><dt>Anno</dt><dd>2026</dd></div>
      <div><dt>Piattaforma</dt><dd>iOS e Android (Flutter)</dd></div>
      <div><dt>Strumenti</dt><dd>Figma</dd></div>
    </dl>
  </section>
  <div class="figure__frame glass" style="margin-top:32px;padding:0">
    <div class="phone-row" role="img" aria-label="Schermate principali dell’app UCI Cinemas: Home, Iris, scelta dei posti, biglietto e bar">
      {phone("UCI · Home", img + "uci-home.webp")}{phone("UCI · Iris", img + "iris-proposte.webp")}{phone("UCI · Posti", img + "uci-posti.webp")}{phone("UCI · Biglietto", img + "uci-biglietto.webp")}{phone("UCI · Bar", img + "uci-bar.webp")}
    </div>
  </div>

  <section class="section" aria-labelledby="film">
    <div class="section-head"><h2 id="film" class="h2">Il film del progetto</h2><p class="label">53 secondi · senza audio</p></div>
    <figure class="figure">
      <div class="figure__frame glass">
        <video class="film" controls playsinline preload="none" width="1920" height="1080" poster="{img}uci-cover.webp" aria-describedby="film-descrizione">
          <source src="{r}assets/video/uci-cinemas-brand-film.mp4" type="video/mp4">
          <a href="{r}assets/video/uci-cinemas-brand-film.mp4">Scarica il video (MP4)</a>
        </video>
      </div>
      <figcaption>Iris presenta la nuova brand identity e l’app. Motion design realizzato a partire dai file Figma del progetto.</figcaption>
    </figure>
    <details class="details glass" id="film-descrizione">
      <summary>Descrizione del video</summary>
      <ol>{"".join(f"<li>{t}</li>" for t in film_scenes)}</ol>
    </details>
  </section>

  <section class="section split" aria-labelledby="progetto">
    <h2 id="progetto" class="h3">Il progetto</h2>
    <div class="stack">
      <p class="lead lead--primary">Ho riprogettato da zero l’app UCI Cinemas come progetto personale, partendo da una brand identity nuova. L’obiettivo: rendere più semplice e veloce l’acquisto del biglietto e sostituire l’acquisto rapido con Iris, un’assistente AI che trova film, orari e posti.</p>
      <aside class="callout glass"><p class="callout__label">Nota</p><p>Progetto non commissionato da UCI. Prezzi, titoli dei film e alcuni dati sono esempi plausibili, da verificare.</p></aside>
    </div>
  </section>

  <section class="section grid grid--stats" style="margin-top:clamp(64px,6vw,96px)" aria-label="Il progetto in numeri">
    {"".join(f'<div class="card glass stat"><p class="stat__value">{v}</p><p class="muted">{l}</p></div>' for v, l in stats)}
  </section>

  <section class="section" aria-labelledby="processo">
    <div class="section-head"><h2 id="processo" class="h2">Processo</h2><p class="label">Quattro fasi</p></div>
    <ol class="grid grid--4">{"".join(f'<li class="card glass service"><div class="service__icon">{icon(i)}</div><h3>{n}. {t}</h3><p class="muted">{d}</p></li>' for n, (i, t, d) in enumerate(steps, 1))}</ol>
  </section>

  <section class="section" aria-labelledby="brand">
    <div class="section-head"><h2 id="brand" class="h2">Brand identity</h2><p class="label">Follow the yellow ellipse</p></div>
    <p class="lead" style="max-width:760px;margin-bottom:24px">Una nuova identità costruita attorno a un solo segno: l’ellisse gialla. È il logo, il simbolo dell’app, il pulsante di Iris e il gesto che lega ogni animazione.</p>
    <div class="brand-grid">
      <div class="brand-tile brand-tile--logo"><img src="{img}brand/logo.svg" alt="Logo UCI Cinemas: ellisse gialla e scritta uci cinemas in bianco" width="323" height="60"></div>
      <div class="brand-tile brand-tile--claim"><p class="brand-claim">Watching movies better.</p></div>
    </div>
    <h3 class="h4 brand-sub">Colore</h3>
    <ul class="swatches">{"".join(f'<li class="swatch" style="background:{h};color:{fg}"><span class="swatch__hex">{h}</span><span class="swatch__name">{n}</span><span class="swatch__use">{u}</span></li>' for h, n, u, fg in palette)}</ul>
    <h3 class="h4 brand-sub">Tipografia</h3>
    <div class="grid grid--2">
      <div class="type-card glass"><p class="type-card__sample type-card__sample--rubik">Aa</p><div><p class="type-card__name type-card__name--rubik">Rubik</p><p class="muted">Titoli, in Black e maiuscolo</p></div></div>
      <div class="type-card glass"><p class="type-card__sample type-card__sample--outfit">Aa</p><div><p class="type-card__name type-card__name--outfit">Outfit</p><p class="muted">Testi ed etichette, da Regular a SemiBold</p></div></div>
    </div>
    <h3 class="h4 brand-sub">Ucicons</h3>
    <ul class="ucicons">{"".join(f'<li class="ucicon glass"><div class="ucicon__art"><img src="{img}brand/{n}.svg" alt="" loading="lazy"></div><span>{d}</span></li>' for n, d in ucicons)}</ul>
  </section>

  <section class="section split split--wide" aria-labelledby="iris">
    <div class="stack">
      <h2 id="iris" class="h2">Iris, l’assistente</h2>
      <p class="lead">Al posto dell’acquisto rapido c’è Iris: un’ellisse gialla minimal con due occhi squadrati che ricordano i fori della pellicola. Si apre dalla Home e guida l’acquisto in conversazione: film, orari, posti, riepilogo.</p>
      <aside class="callout glass"><p class="callout__label">Decisione</p><p>Il pagamento lo conferma sempre l’utente con Face ID: Iris non paga mai da sola.</p></aside>
    </div>
    <div class="phones phones--compact" role="img" aria-label="Tre schermate della conversazione con Iris: benvenuto, proposte e riepilogo">
      {phone("Iris · Benvenuto", img + "iris-benvenuto.webp")}{phone("Iris · Proposte", img + "iris-proposte.webp")}{phone("Iris · Riepilogo", img + "iris-riepilogo.webp")}
    </div>
  </section>

  <section class="section" aria-labelledby="aree">
    <div class="section-head"><h2 id="aree" class="h2">Le 9 aree dell’app</h2><p class="label">85 schermate</p></div>
    <ol class="areas">{"".join(f'<li class="glass">{a}</li>' for a in areas)}</ol>
    <figure class="figure" style="margin-top:16px">
      <div class="figure__frame glass">{media("Mappa dei flussi", "figure__media figure__media--fit", img + "uci-mappa-flussi.webp", "Mappa dei flussi: dall’onboarding alla Home, e dalla Home ad acquisto classico, acquisto con Iris, film, cinema, biglietti, profilo; dal biglietto al bar e al promemoria")}</div>
      <figcaption>Mappa dei flussi: tutte le aree e i collegamenti del prototipo completo.</figcaption>
    </figure>
  </section>

  <section class="section" aria-labelledby="ds">
    <div class="section-head"><h2 id="ds" class="h2">Design system</h2><p class="label">v3.31</p></div>
    <p class="lead" style="margin-bottom:24px">Ogni schermata usa componenti del design system: prima si riusa ciò che esiste, poi si crea il nuovo e lo si aggiunge alla libreria, con ogni modifica nel changelog.</p>
    <div class="grid grid--3">{"".join(f'<div class="callout callout--small glass"><p class="callout__label">Regola</p><p>{t}</p></div>' for t in rules)}</div>
    <figure class="figure" style="margin-top:16px">
      <div class="figure__frame glass">{media("Design system", "figure__media figure__media--fit", img + "uci-design-system.webp", "Design system UCI Cinemas: titolo e una tavola di componenti reali dell’app in tema Dark")}</div>
      <figcaption>Alcuni degli 80 componenti, in tema Dark: Hero Card, Showtime Chip, Seat Map, riepilogo di Iris, Ticket Card, Food Item Card, Composer, Tab Bar e Loyalty Card.</figcaption>
    </figure>
  </section>

  <section class="section" aria-labelledby="a11y">
    <div class="section-head"><h2 id="a11y" class="h2">Accessibilità</h2><p class="label">WCAG 2.2 AA</p></div>
    <div class="grid grid--3">{"".join(f'<div class="card glass stat"><p class="stat__value">{v}</p><p class="muted">{l}</p></div>' for v, l in acc)}</div>
    <aside class="callout glass" style="margin-top:16px"><p class="callout__label">Per lo sviluppo</p><p>Testo dinamico fino al 200%, etichette per VoiceOver e TalkBack su ogni pulsante icona, rispetto di «Riduci movimento» e stati mai affidati al solo colore.</p></aside>
  </section>

  <section class="section grid grid--2" aria-label="Lezioni e prossimi passi">
    <div class="card glass stack" style="border-radius:var(--r-card);padding:clamp(24px,3.4vw,48px)"><h2 class="h3">Cosa ho imparato</h2><p class="lead">[Due o tre lezioni dal progetto: una decisione che rifaresti, una che cambieresti, cosa ti ha sorpreso.]</p></div>
    <div class="card glass stack" style="border-radius:var(--r-card);padding:clamp(24px,3.4vw,48px)"><h2 class="h3">Prossimi passi</h2><p class="lead">Test con utenti, versione Android, Google Pay e Wallet, immagini definitive e passaggio agli sviluppatori.</p></div>
  </section>

  <section class="section" aria-label="Prossimo progetto">
    <div class="projects">{project_card(next_p, r, "h2")}</div>
  </section>
</div>"""
    glows = [("blue", "-14%", "-240px", "62vw", "620px", .42), ("lavender", "55%", "-160px", "56vw", "520px", .3),
             ("warm", "60%", "700px", "28vw", "320px", .22), ("lavender", "-10%", "2600px", "50vw", "600px", .16), ("blue", "50%", "4600px", "50vw", "600px", .16)]
    fonts = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rubik:wght@900&family=Outfit:wght@400;600&display=swap">\n'
    return layout("lavori/uci-cinemas/", 2, "UCI Cinemas, case study", "Case study del redesign dell’app UCI Cinemas: brand identity, 85 schermate, design system, assistente AI Iris e revisione di accessibilità WCAG 2.2.", body, glows, fonts)

def jethr():
    r = "../../"
    img = r + "assets/img/"
    stats = [("20", "schermate: 9 per la web app desktop e 11 per l’app iOS 27"), ("6", "componenti condivisi tra desktop e iPhone, oltre a pulsanti, badge e campi"),
             ("1", "cedolino A4 riprogettato, con tutti i dati obbligatori"), ("AA", "contrasti WCAG 2.2 verificati sui token del design system")]
    steps = [("search", "Discovery", "Problema riformulato, domande reali dei dipendenti e vincoli di legge prima di disegnare."),
             ("components", "Design system", "Il brand del sito esteso in token, stili di testo e componenti con variante desktop e mobile."),
             ("layout", "Desktop e iOS 27", "Web app e app iPhone con gli stessi componenti; nativi solo quelli di sistema."),
             ("accessibility", "Busta paga e verifica", "Cedolino A4 riprogettato, vista spiegata voce per voce, piano di test e controlli WCAG.")]
    questions = [("Quanto ricevo, e quando?", "Netto e data di accredito sono la prima cosa in home. Il netto è nascosto finché non tocchi l’occhio."),
                 ("Perché è diverso dal mese scorso?", "Ogni busta paga dice cosa è cambiato rispetto al mese prima, con le voci che spiegano la differenza."),
                 ("Quanti giorni di ferie ho?", "Ferie e permessi in giorni, con le ore come dettaglio e la stima al 31 dicembre."),
                 ("Dove finiscono i soldi tra lordo e netto?", "Una barra divisa in tre: quello che resta a te, i contributi per la pensione e le tasse.")]
    legal = [("L. 4/1953", "La busta paga è obbligatoria ma non ha un modello fisso: si può riorganizzare, purché contenga tutti i dati."),
             ("LUL · D.L. 112/2008", "Il prospetto deve corrispondere al Libro Unico del Lavoro: stessi importi e codici, cambia solo come si leggono."),
             ("GDPR", "Dati minimi e privati per default: netto nascosto, IBAN mascherato, niente codice fiscale nei nomi dei file."),
             ("D.Lgs. 96/2026", "Trasparenza retributiva: dal profilo si chiedono i livelli retributivi medi per il proprio ruolo.")]
    rules = ["Stessi componenti su desktop e iPhone: Riga lista, Card netto, Controllo segmentato e gli altri hanno una variante per piattaforma. Su iOS restano nativi solo status bar, toolbar, tab bar e sheet.",
             "Raggi annidati: raggio esterno = raggio interno + padding. Card con padding 20 e raggio 40, quindi tutto ciò che tocca un angolo ha raggio 20; pulsanti a capsula.",
             "Stessi stili di testo ovunque: Mona Sans per titoli e importi, Wix Madefor Display per il testo, anche nei titoli della toolbar e nella tab bar di iOS."]
    palette = [("#DFEB57", "Lime", "Accento del brand e stati in evidenza", "#11150A"), ("#11150A", "Nero", "Testi, pulsanti principali e card dello stipendio", "#DFEB57"),
               ("#F8FAF5", "Pagina", "Sfondo delle schermate", "#11150A"), ("#FFFFFF", "Card", "Superfici e liste", "#11150A"),
               ("#0BB098", "Ferie", "Categoria nel calendario", "#11150A"), ("#4330B2", "Permesso", "Categoria e contributi", "#FFFFFF"),
               ("#B01F42", "Malattia", "Categoria e tasse", "#FFFFFF")]
    acc = [("14,2:1", "Testo nero su lime, nei pulsanti del brand"), ("3,6 → 6,1:1", "Stato «Rifiutata»: il token è stato scurito dopo la verifica"), ("≥ 44 pt", "Area di tocco su iOS, anche per i pulsanti piccoli")]
    next_p = dict(PROJECTS[0]); next_p["eyebrow"] = "Prossimo progetto · App mobile · 2026"
    body = f"""
<div class="wrap">
  <p style="margin-top:clamp(32px,4vw,48px)"><a class="back" href="../">{icon("arrow-left", 18)} Tutti i lavori</a></p>
  <section class="intro" style="display:grid;gap:clamp(20px,2vw,28px);justify-items:start;padding-top:16px" aria-labelledby="titolo">
    <p class="chip chip--status">Case study · Web app e iOS · 2026</p>
    <h1 id="titolo" class="display">Jet HR</h1>
    <p class="lead" style="max-width:760px">Il redesign dell’area dipendente di Jet HR, su desktop e iPhone, e una busta paga che si capisce anche senza conoscere le sigle.</p>
    <dl class="meta">
      <div><dt>Ruolo</dt><dd>Product designer · progetto personale</dd></div>
      <div><dt>Anno</dt><dd>2026</dd></div>
      <div><dt>Piattaforma</dt><dd>Web app desktop e iOS 27</dd></div>
      <div><dt>Strumenti</dt><dd>Figma</dd></div>
    </dl>
  </section>
  <div class="figure__frame glass" style="margin-top:32px;padding:0">
    <div class="phone-row" role="img" aria-label="Schermate dell’app iOS di Jet HR: home, tempo libero, stipendio, busta paga spiegata e calcolo dell’IRPEF">
      {phone("Jet HR · Home", img + "jethr-m-home.webp")}{phone("Jet HR · Tempo libero", img + "jethr-m-tempo.webp")}{phone("Jet HR · Stipendio", img + "jethr-m-stipendio.webp")}{phone("Jet HR · Busta paga", img + "jethr-m-busta.webp")}{phone("Jet HR · Calcolo IRPEF", img + "jethr-m-irpef.webp")}
    </div>
  </div>

  <section class="section split" aria-labelledby="progetto">
    <h2 id="progetto" class="h3">Il progetto</h2>
    <div class="stack">
      <p class="lead lead--primary">Jet HR gestisce le paghe di molte piccole aziende italiane. L’area dei dipendenti è dove si guarda la busta paga, si chiedono le ferie, si caricano gli scontrini e si scaricano i documenti. Oggi l’app mobile è la versione desktop rimpicciolita, e la busta paga parla la lingua del consulente del lavoro. Ho riprogettato entrambe partendo da una domanda: cosa vuole sapere davvero un dipendente quando apre l’app?</p>
      <aside class="callout glass"><p class="callout__label">Nota</p><p>Concept personale, non commissionato né approvato da Jet HR. Persone, aziende e importi sono fittizi. I riferimenti normativi vengono da una ricerca su fonti pubbliche (ottobre 2026), usata solo a scopo progettuale: non sono consulenza legale o fiscale.</p></aside>
    </div>
  </section>

  <section class="section grid grid--stats" style="margin-top:clamp(64px,6vw,96px)" aria-label="Il progetto in numeri">
    {"".join(f'<div class="card glass stat"><p class="stat__value">{v}</p><p class="muted">{l}</p></div>' for v, l in stats)}
  </section>

  <section class="section" aria-labelledby="processo">
    <div class="section-head"><h2 id="processo" class="h2">Processo</h2><p class="label">Quattro fasi</p></div>
    <ol class="grid grid--4">{"".join(f'<li class="card glass service"><div class="service__icon">{icon(i)}</div><h3>{n}. {t}</h3><p class="muted">{d}</p></li>' for n, (i, t, d) in enumerate(steps, 1))}</ol>
  </section>

  <section class="section" aria-labelledby="domande">
    <div class="section-head"><h2 id="domande" class="h2">Le domande giuste</h2><p class="label">Discovery</p></div>
    <p class="lead" style="max-width:760px;margin-bottom:24px">Chi apre l’area dipendente ha quasi sempre una domanda precisa. Ho messo in ordine quelle più frequenti e ho costruito la home e la busta paga per rispondere prima a quelle.</p>
    <div class="grid grid--2">{"".join(f'<div class="callout glass"><p class="callout__label">{q}</p><p>{a}</p></div>' for q, a in questions)}</div>
    <figure class="figure" style="margin-top:16px">
      <div class="figure__frame glass">{media("Domande dei dipendenti", "figure__media figure__media--fit", img + "jethr-domande.webp", "Tavola di discovery: le domande di un dipendente raggruppate per tema, da «Quanto e quando» a «Dov’è il documento»")}</div>
      <figcaption>Le domande raggruppate per tema e frequenza: guidano l’ordine dei contenuti in home e nella busta paga.</figcaption>
    </figure>
  </section>

  <section class="section" aria-labelledby="legge">
    <div class="section-head"><h2 id="legge" class="h2">Cosa si può cambiare</h2><p class="label">Vincoli di legge</p></div>
    <p class="lead" style="max-width:760px;margin-bottom:24px">Prima di ridisegnare la busta paga ho verificato cosa è obbligatorio e cosa no. La forma è libera, il contenuto no.</p>
    <div class="grid grid--2">{"".join(f'<div class="callout glass"><p class="callout__label">{t}</p><p>{d}</p></div>' for t, d in legal)}</div>
  </section>

  <section class="section" aria-labelledby="desktop">
    <div class="section-head"><h2 id="desktop" class="h2">La web app</h2><p class="label">Desktop</p></div>
    <p class="lead" style="max-width:760px;margin-bottom:24px">In home ci sono lo stipendio con la data di accredito, il tempo libero in giorni, le cose da fare e la settimana del team. Le richieste si fanno da un pannello laterale, senza perdere il calendario.</p>
    <figure class="figure">
      <div class="figure__frame glass">{media("Home desktop", "figure__media figure__media--fit", img + "jethr-d-home.webp", "Home della web app: stipendio di settembre nascosto, tempo libero, cose da fare, settimana del team e richieste")}</div>
      <figcaption>Home: il netto resta nascosto finché non tocchi l’occhio; la data di accredito è sempre visibile.</figcaption>
    </figure>
    <figure class="figure" style="margin-top:16px">
      <div class="figure__frame glass">{media("Richiesta di assenza", "figure__media figure__media--fit", img + "jethr-d-assenza.webp", "Calendario del tempo libero con il pannello per richiedere un’assenza: tipo, date, durata e riepilogo")}</div>
      <figcaption>Richiesta di ferie: tipo, date, saldo dopo la richiesta e chi del team è assente, nello stesso pannello.</figcaption>
    </figure>
  </section>

  <section class="section split split--wide" aria-labelledby="ios">
    <div class="stack">
      <h2 id="ios" class="h2">L’app iOS 27</h2>
      <p class="lead">Status bar, toolbar, tab bar e sheet vengono dalla libreria ufficiale di Apple. Dentro, gli stessi componenti della web app: chi passa dal computer al telefono ritrova le stesse righe, le stesse card e gli stessi pulsanti.</p>
      <aside class="callout glass"><p class="callout__label">Decisione</p><p>Nella tab bar le quattro sezioni usano le icone di Jet HR, non gli SF Symbols: sono le stesse della barra laterale desktop.</p></aside>
    </div>
    <div class="phones phones--compact" role="img" aria-label="Tre schermate iOS: richiesta di assenza, stipendio e calcolo dell’IRPEF">
      {phone("Richiedi un’assenza", img + "jethr-m-assenza.webp")}{phone("Stipendio", img + "jethr-m-stipendio.webp")}{phone("Tasse sul reddito", img + "jethr-m-irpef.webp")}
    </div>
  </section>

  <section class="section" aria-labelledby="busta">
    <div class="section-head"><h2 id="busta" class="h2">La busta paga</h2><p class="label">Due livelli, un solo dato</p></div>
    <p class="lead" style="max-width:760px;margin-bottom:24px">Il PDF ufficiale resta il documento legale, ma riorganizzato per domande. Nell’app, la vista spiegata mette ogni voce in parole semplici, con il nome ufficiale e il codice accanto. Gli importi sono gli stessi, cambiano le parole.</p>
    <figure class="figure">
      <div class="figure__frame glass">{media("Busta paga spiegata", "figure__media figure__media--fit", img + "jethr-d-busta.webp", "Busta paga di settembre spiegata: netto, differenze rispetto ad agosto, dal lordo al netto e tutte le voci")}</div>
      <figcaption>Busta paga spiegata: cosa è cambiato rispetto ad agosto, dove vanno i soldi tra lordo e netto, ogni voce con il suo calcolo (dettaglio della schermata).</figcaption>
    </figure>
    <div class="grid grid--2" style="margin-top:16px;align-items:start">
      <figure class="figure">
        <div class="figure__frame glass">{media("Cedolino A4", "figure__media figure__media--fit", img + "jethr-cedolino.webp", "Cedolino A4 riprogettato: dati del datore e del lavoratore, riepilogo, competenze, trattenute, ferie, TFR e presenze del mese")}</div>
        <figcaption>Il cedolino A4: riepilogo in alto, poi competenze e trattenute con codici e spiegazione breve.</figcaption>
      </figure>
      <figure class="figure">
        <div class="figure__frame glass">{media("Dal documento alla spiegazione", "figure__media figure__media--fit", img + "jethr-strategia.webp", "Tavola di strategia: per ogni domanda dell’utente, dove trova la risposta nell’app; per ogni dato obbligatorio, dove sta nel PDF")}</div>
        <figcaption>Ogni domanda dell’utente ha il suo posto nell’app, ogni dato obbligatorio il suo posto nel PDF.</figcaption>
      </figure>
    </div>
  </section>

  <section class="section" aria-labelledby="ds">
    <div class="section-head"><h2 id="ds" class="h2">Design system</h2><p class="label">Esteso dal sito di Jet HR</p></div>
    <p class="lead" style="max-width:760px;margin-bottom:24px">Colori e caratteri vengono dal sito di Jet HR. Li ho trasformati in variabili e stili, poi ho aggiunto i componenti che servivano all’app, ognuno con una variante desktop e una mobile.</p>
    <ul class="swatches">{"".join(f'<li class="swatch" style="background:{h};color:{fg}"><span class="swatch__hex">{h}</span><span class="swatch__name">{n}</span><span class="swatch__use">{u}</span></li>' for h, n, u, fg in palette)}</ul>
    <div class="grid grid--2" style="margin-top:16px">
      <div class="type-card glass"><p class="type-card__sample" style="font-family:'Mona Sans',sans-serif;font-weight:800">Aa</p><div><p class="type-card__name" style="font-family:'Mona Sans',sans-serif;font-weight:800">Mona Sans</p><p class="muted">Titoli e importi</p></div></div>
      <div class="type-card glass"><p class="type-card__sample" style="font-family:'Wix Madefor Display',sans-serif">Aa</p><div><p class="type-card__name" style="font-family:'Wix Madefor Display',sans-serif">Wix Madefor Display</p><p class="muted">Testi ed etichette</p></div></div>
    </div>
    <div class="grid grid--3" style="margin-top:16px">{"".join(f'<div class="callout callout--small glass"><p class="callout__label">Regola</p><p>{t}</p></div>' for t in rules)}</div>
    <figure class="figure" style="margin-top:16px">
      <div class="figure__frame glass">{media("Componenti condivisi", "figure__media figure__media--fit", img + "jethr-componenti.webp", "Tavola dei componenti condivisi: Toggle, Riga lista, Intestazione sezione, Controllo segmentato, Card netto e Scelta tipo, ognuno in versione desktop e mobile")}</div>
      <figcaption>I componenti condivisi, ognuno con la variante desktop e quella mobile.</figcaption>
    </figure>
  </section>

  <section class="section" aria-labelledby="a11y">
    <div class="section-head"><h2 id="a11y" class="h2">Accessibilità e test</h2><p class="label">WCAG 2.2 AA</p></div>
    <div class="grid grid--3">{"".join(f'<div class="card glass stat"><p class="stat__value">{v}</p><p class="muted">{l}</p></div>' for v, l in acc)}</div>
    <aside class="callout glass" style="margin-top:16px"><p class="callout__label">Prossima verifica</p><p>Usability test moderato da remoto con 5 persone su desktop e 5 su iPhone: capire quanto si riceve e quando, spiegare una voce della busta paga, chiedere un giorno di ferie, caricare una spesa, trovare la Certificazione Unica.</p></aside>
  </section>

  <section class="section grid grid--2" aria-label="Lezioni e prossimi passi">
    <div class="card glass stack" style="border-radius:var(--r-card);padding:clamp(24px,3.4vw,48px)"><h2 class="h3">Cosa ho imparato</h2><p class="lead">[Due o tre lezioni dal progetto: una decisione che rifaresti, una che cambieresti, cosa ti ha sorpreso.]</p></div>
    <div class="card glass stack" style="border-radius:var(--r-card);padding:clamp(24px,3.4vw,48px)"><h2 class="h3">Prossimi passi</h2><p class="lead">Usability test con dipendenti veri, verifica dei testi con un consulente del lavoro, modalità scura e Dynamic Type, passaggio agli sviluppatori.</p></div>
  </section>

  <section class="section" aria-label="Prossimo progetto">
    <div class="projects">{project_card(next_p, r, "h2")}</div>
  </section>
</div>"""
    glows = [("blue", "-14%", "-240px", "62vw", "620px", .42), ("lavender", "55%", "-160px", "56vw", "520px", .3),
             ("warm", "60%", "700px", "28vw", "320px", .22), ("lavender", "-10%", "2600px", "50vw", "600px", .16), ("blue", "50%", "4600px", "50vw", "600px", .16)]
    fonts = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Mona+Sans:wght@800&family=Wix+Madefor+Display:wght@400&display=swap">\n'
    return layout("lavori/jet-hr/", 2, "Jet HR, case study", "Case study del redesign dell’area dipendente di Jet HR: web app desktop, app iOS 27 con gli stessi componenti e una busta paga che si capisce.", body, glows, fonts)

def chi_sono():
    body = f"""
<div class="wrap">
  <section class="about-hero" style="padding-top:clamp(64px,8vw,120px)" aria-labelledby="titolo">
    <div class="stack intro" style="--gap:clamp(20px,2vw,28px)">
      <p class="chip chip--status" style="width:max-content">Product designer</p>
      <h1 id="titolo" class="display" style="max-width:10ch">Ciao, sono Sebastiano.</h1>
      <p class="lead" style="max-width:720px">[Racconta in tre o quattro righe chi sei: il percorso che ti ha portato al product design, cosa ti appassiona, in che tipo di team ti piace lavorare e cosa cerchi adesso.]</p>
      <div class="actions actions--stack-mobile">
        <a class="btn btn--primary" href="../{CONFIG['cv']}" download>Scarica il CV</a>
        <a class="btn btn--secondary" href="{CONFIG['linkedin']}" rel="me noopener" target="_blank">LinkedIn</a>
      </div>
    </div>
    <div class="figure__frame glass portrait">{media("Il tuo ritratto, 4:5", "figure__media")}</div>
  </section>

  <section class="section" id="metodo" aria-labelledby="metodo-titolo">
    <div class="section-head"><h2 id="metodo-titolo" class="h2">Come lavoro</h2><p class="label">Dal problema al componente</p></div>
    {services_html()}
  </section>

  <section class="section grid grid--2" style="gap:48px 32px;align-items:start" aria-label="Percorso">
    <div class="stack" style="--gap:12px"><h2 class="h3">Esperienza</h2>{timeline([("[Ruolo]", "[Azienda]", "[Anno – Anno]")]*3)}</div>
    <div class="stack" style="--gap:12px"><h2 class="h3">Formazione</h2>{timeline([("[Corso o titolo]", "[Scuola o ente]", "[Anno – Anno]")]*2)}</div>
  </section>

  <section class="section stack" aria-labelledby="skill">
    <h2 id="skill" class="h3">Competenze e strumenti</h2>
    {chips(["UX research", "Interviste", "Usability test", "Architettura dell’informazione", "Interfacce", "Prototipi", "Design system", "Token", "Accessibilità WCAG 2.2", "AI conversazionale", "Figma", "Figma Sites", "Handoff a Flutter"])}
  </section>

  <section class="section band band--center glass" aria-labelledby="ct">
    <h2 id="ct" class="h2">Lavoriamo insieme.</h2>
    <p class="lead">Hai un progetto o una posizione aperta? Scrivimi.</p>
    <div class="actions actions--stack-mobile" style="justify-content:center">
      <a class="btn btn--primary" href="../contatti/">Scrivimi</a>
      <a class="btn btn--secondary" href="../{CONFIG['cv']}" download>Scarica il CV</a>
    </div>
  </section>
</div>"""
    glows = [("blue", "-14%", "-240px", "62vw", "620px", .42), ("lavender", "55%", "-120px", "56vw", "560px", .32), ("blue", "50%", "1800px", "50vw", "600px", .16)]
    return layout("chi-sono/", 1, "Chi sono", "Chi è Sebastiano Bosi, product designer: metodo, esperienza, competenze e strumenti.", body, glows)

def contatti():
    body = f"""
<div class="wrap wrap--fill">
  <div class="split split--contacts" style="padding-block:clamp(64px,8vw,120px) 0">
    <section class="stack intro" style="--gap:clamp(20px,2vw,28px)" aria-labelledby="titolo">
      <h1 id="titolo" class="display">Scrivimi.</h1>
      <p class="lead">Che si tratti di un progetto, di una posizione aperta o di una domanda sul mio lavoro, rispondo volentieri. Di solito entro due giorni lavorativi.</p>
    </section>

    <section aria-label="Contatti diretti">
      <ul class="contacts contacts--large">
        <li class="contact glass">
          <span class="service__icon">{icon("mail")}</span>
          <span class="contact__text"><span class="label-s">Email</span><a class="contact__value" href="mailto:{CONFIG['email']}">{CONFIG['email']}</a></span>
          <button class="btn btn--secondary contact__action" type="button" data-copy="{CONFIG['email']}">Copia</button>
        </li>
        <li class="contact glass">
          <span class="service__icon">{icon("arrow-up-right")}</span>
          <span class="contact__text"><span class="label-s">LinkedIn</span><a class="contact__value" href="{CONFIG['linkedin']}" rel="me noopener" target="_blank">Il mio profilo</a></span>
        </li>
        <li class="contact glass">
          <span class="service__icon">{icon("briefcase")}</span>
          <span class="contact__text"><span class="label-s">Curriculum</span><a class="contact__value" href="../{CONFIG['cv']}" download>Scarica il PDF</a></span>
        </li>
      </ul>
      <p class="visually-hidden" aria-live="polite" data-copy-status></p>
    </section>
  </div>
</div>"""
    glows = [("blue", "-14%", "-240px", "62vw", "620px", .42), ("lavender", "55%", "-120px", "56vw", "560px", .3), ("warm", "62%", "500px", "30vw", "320px", .18)]
    return layout("contatti/", 1, "Contatti", "Contatta Sebastiano Bosi per un progetto o una posizione aperta: email, LinkedIn e curriculum.", body, glows)

def not_found():
    # La 404 di GitHub Pages viene servita a qualsiasi profondità: link assoluti alla radice
    body = """
<div class="wrap wrap--fill"><section class="notfound"><div class="stack" style="--gap:20px;justify-items:center;display:grid">
  <p class="notfound__code" aria-hidden="true">404</p>
  <h1 class="h3">Questa pagina non esiste.</h1>
  <p class="lead" style="margin-inline:auto">Forse il link è cambiato. Riparti dalla home o guarda direttamente i lavori.</p>
  <div class="actions actions--stack-mobile" style="justify-content:center"><a class="btn btn--primary" href="/">Torna alla home</a><a class="btn btn--secondary" href="/lavori/">Guarda i lavori</a></div>
</div></section></div>"""
    page = layout("404", 0, "Pagina non trovata", "Questa pagina non esiste.", body,
                  [("blue", "15%", "20%", "60vw", "600px", .3), ("lavender", "45%", "35%", "50vw", "500px", .22)])
    # percorsi assoluti per CSS/JS/link nella 404
    return (page.replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/')
                .replace('href="./"', 'href="/"').replace('href="lavori/"', 'href="/lavori/"')
                .replace('href="chi-sono/"', 'href="/chi-sono/"').replace('href="contatti/"', 'href="/contatti/"')
                .replace('href="#metodo"', 'href="/#metodo"'))

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="18" fill="#07080f"/><circle cx="20" cy="18" r="22" fill="#1e4fd8" opacity=".55"/><circle cx="48" cy="50" r="20" fill="#9d7bea" opacity=".45"/><text x="32" y="41" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="24" fill="#f2f3f7">SB</text></svg>"""

def main(out):
    src = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs(out, exist_ok=True)
    pages = {"index.html": home(), "lavori/index.html": lavori(), "lavori/uci-cinemas/index.html": uci(), "lavori/jet-hr/index.html": jethr(),
             "chi-sono/index.html": chi_sono(), "contatti/index.html": contatti(), "404.html": not_found()}
    for path, content in pages.items():
        p = os.path.join(out, path); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(content)
    if os.path.abspath(out) != src:
        for d in ("assets/css", "assets/js"):
            shutil.copytree(os.path.join(src, d), os.path.join(out, d), dirs_exist_ok=True)
    os.makedirs(os.path.join(out, "assets/img"), exist_ok=True)
    open(os.path.join(out, "assets/img/favicon.svg"), "w").write(FAVICON)
    open(os.path.join(out, ".nojekyll"), "w").write("")
    urls = ["", "lavori/", "lavori/uci-cinemas/", "lavori/jet-hr/", "chi-sono/", "contatti/"]
    open(os.path.join(out, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{CONFIG['site_url']}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    open(os.path.join(out, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {CONFIG['site_url']}/sitemap.xml\n")
    print("Pagine generate:", ", ".join(pages))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
