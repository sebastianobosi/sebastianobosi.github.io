#!/usr/bin/env python3
"""Genera le pagine HTML del portfolio a partire da parti condivise.

Uso:  python3 tools/build.py            (rigenera le pagine nella cartella del sito)
Le pagine usano link relativi, quindi funzionano su GitHub Pages, in locale e in anteprima.
Per cambiare email, LinkedIn o CV, modifica CONFIG qui sotto e rigenera.
"""
import sys, os, shutil, html, hashlib
import i18n

LANG = "it"   # cambia durante la build: "it" per le pagine alla radice, "en" per quelle in en/

CONFIG = {
    "site_url": "https://sebastianobosi.github.io",
    "name": "Sebastiano Bosi",
    "email": "sebastianobosi@icloud.com",
    "linkedin": "https://www.linkedin.com/in/sebastiano-bosi-24674016a",
    "cv_ats": "assets/sebastiano-bosi-cv-ats.pdf",            # CV solo testo, generato da tools/cv_ats.py
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
    full_title = f"{title} — {CONFIG['name']}" if title != CONFIG["name"] else f"{CONFIG['name']} — UX/UI Designer a Milano"
    site = CONFIG["site_url"]
    it_url, en_url = site + "/" + page, site + "/en/" + page
    canonical = en_url if LANG == "en" else it_url
    if page == "404":
        alternates, switch, menu_switch = "", "", ""
    else:
        alternates = (f'<link rel="alternate" hreflang="it" href="{it_url}">\n<link rel="alternate" hreflang="en" href="{en_url}">\n'
                      f'<link rel="alternate" hreflang="x-default" href="{it_url}">\n')
        if LANG == "en":
            other = ("../" * (depth + 1)) + page
            switch = f'<a class="nav__lang" href="{other}" hreflang="it" lang="it" aria-label="Leggi in italiano">IT</a>'
        else:
            switch = f'<a class="nav__lang" href="{r}en/{page}" hreflang="en" lang="en" aria-label="Read in English">EN</a>'
        menu_switch = switch.replace('class="nav__lang"', 'class="menu__lang"')
    return f"""<!doctype html>
<html lang="{LANG}">
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
<meta property="og:locale" content="{'en_GB' if LANG == 'en' else 'it_IT'}">
{alternates}
<meta name="author" content="{CONFIG['name']}">
<meta name="copyright" content="© 2026 {CONFIG['name']}. Tutti i diritti riservati.">
<meta name="tdm-reservation" content="1">
<meta name="tdm-policy" content="{CONFIG['site_url']}/note-legali/">
<meta name="theme-color" content="#07080f">
{structured_data(page, title, description)}
<link rel="icon" href="{r}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&display=swap">
<link rel="stylesheet" href="{r}assets/css/style.css?v={v}">
<script>document.documentElement.classList.add('js')</script>
<script src="{r}assets/js/main.js?v={v}" defer></script>
{extra_head}</head>
<body>
<a class="skip-link" href="#contenuto">Vai al contenuto</a>

<header class="site-header">
  <div class="wrap">
    <nav class="nav" aria-label="Principale">
      <a class="nav__logo" href="{r or './'}">{CONFIG['name']}</a>
      <div class="nav__right">
        <ul class="nav__links">{links}</ul>
        <a class="nav__cta" href="{r}contatti/">Contattami</a>
        {switch}
        <button class="nav__menu-btn" type="button" data-menu-open aria-expanded="false" aria-controls="menu">Menu {icon("menu")}</button>
      </div>
    </nav>
  </div>
</header>

<div class="menu" id="menu" hidden role="dialog" aria-modal="true" aria-label="Menu">
  <div class="menu__bar">
    <a class="nav__logo" href="{r or './'}">{CONFIG['name']}</a>
    <button class="nav__menu-btn" type="button" data-menu-close>Chiudi {icon("close")}</button>
  </div>
  {menu_switch}
  <ul class="menu__list">{menu_links}</ul>
  <div class="actions">
    <a class="btn btn--primary" href="{r}contatti/">Contattami</a>
    <a class="btn btn--secondary" href="{r}cv/">CV</a>
  </div>
</div>

<main id="contenuto">
{body}
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer">
      <div class="footer__invite">
        <h2>Lavoriamo insieme.</h2>
        <p class="footer__lead">Hai un progetto o una domanda sul mio lavoro? Scrivimi: di solito rispondo entro due giorni lavorativi.</p>
        <a class="btn btn--primary" href="{r}contatti/">Scrivimi {icon("arrow-up-right", 18)}</a>
      </div>
      <nav class="footer__links" aria-label="Contatti">
        <a href="mailto:{CONFIG['email']}">{CONFIG['email']}</a>
        <a href="{CONFIG['linkedin']}" rel="me noopener" target="_blank">LinkedIn</a>
        <a href="{r}cv/">CV</a>
      </nav>
      <div class="footer__legal">
        <p>© 2026 {CONFIG['name']}. Tutti i diritti riservati.</p>
        <ul><li><a href="{r}note-legali/">Note legali</a></li><li><a href="#contenuto">Torna su {icon("arrow-up", 16)}</a></li></ul>
      </div>
    </div>
  </div>
  <span class="footer__name" aria-hidden="true">{CONFIG['name']}</span>
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
    dict(slug="lavori/uci-cinemas/", title="UCI Cinemas", kind="App mobile · brand identity · progetto personale",
         desc="Il redesign dell’app: biglietti in pochi tocchi e Iris, l’assistente che sceglie il film con te. 85 schermate e 80 componenti in due temi.",
         tags="app design-system",
         img="assets/img/uci-cover.webp", alt="Iris, la mascotte gialla dell’app, sopra il logo UCI Cinemas e il claim «Il cinema, a modo tuo»",
         detail="assets/img/uci-design-system.webp", detail_alt="Una tavola del design system UCI in tema scuro: biglietto, mappa dei posti, carta fedeltà"),
    dict(slug="lavori/jet-hr/", title="Jet HR", kind="Web app e app mobile · progetto personale",
         desc="L’area dipendente e una busta paga che si capisce: le domande vere dei dipendenti al centro, gli stessi componenti su desktop e mobile.",
         tags="web app design-system",
         img="assets/img/jethr-cover.webp", alt="La home di Jet HR su desktop e su smartphone, con lo stipendio nascosto e la data di accredito",
         detail="assets/img/jethr-d-home.webp", detail_alt="La home della web app Jet HR: stipendio, tempo libero, cose da fare e settimana del team"),
    dict(slug="lavori/idealista/", title="idealista", kind="Brand identity e app mobile · progetto personale",
         desc="Nuova identità e app per trovare casa con prezzi chiari e annunci verificati: 39 schermate, 54 icone e un solo pixel quadrato.",
         tags="app design-system",
         img="assets/img/idealista-cover.webp", alt="La copertina del progetto idealista: il nuovo logo con il pixel quadrato e le schermate dell’app su fondo lime",
         detail="assets/img/idealista-b-pixel.webp", detail_alt="Il pixel quadrato del logo usato come sistema: app icon, pin della mappa e indicatori",
         video="assets/video/idealista-brand-video.mp4", poster="assets/img/idealista-video-poster.webp"),
]

def work_block(p, r, n, heading="h3"):
    href = r + p["slug"]
    if p.get("video"):
        visual = (f'<video muted loop playsinline preload="none" width="1600" height="900" poster="{r + p["poster"]}" data-autoplay '
                  f'aria-label="Il video del brand idealista, senza audio: il pixel lime diventa il logo, poi colori, tipografia e mappa">'
                  f'<source src="{r + p["video"]}" type="video/mp4"></video>')
    else:
        visual = f'<img src="{r + p["img"]}" alt="{html.escape(p["alt"])}" loading="lazy" width="1600" height="900">'
    return f"""<article class="work-block work-block--{n}" data-tags="{p['tags']}">
  <div class="work-block__visual">{visual}</div>
  <div class="work-block__cluster">
    <div class="work-block__detail"><img src="{r + p['detail']}" alt="{html.escape(p['detail_alt'])}" loading="lazy" width="1600" height="1000"></div>
    <{heading} class="work-block__title"><a href="{href}">{p['title']}</a></{heading}>
    <p class="work-block__kind">{p['kind']}</p>
    <p>{p['desc']}</p>
    <a class="link" href="{href}" tabindex="-1" aria-hidden="true">Leggi il case study{icon("arrow-up-right", 18)}</a>
  </div>
</article>"""

def work_blocks(r, heading="h3"):
    return '<div class="work projects">' + "".join(work_block(p, r, i, heading) for i, p in enumerate(PROJECTS, 1)) + "</div>"

def next_block(p, r):
    href = r + p["slug"]
    return f"""<section class="section next" aria-labelledby="prossimo">
    <div class="stack" style="--gap:16px">
      <h2 id="prossimo" class="h2"><a href="{href}">Prossimo progetto: {p['title']}</a></h2>
      <p class="muted">{p['kind']}</p>
      <p>{p['desc']}</p>
    </div>
    <div class="next__visual"><img src="{r + p['img']}" alt="{html.escape(p['alt'])}" loading="lazy" width="1600" height="900"></div>
  </section>"""

METODO = [
    ("Ricerca", "Parlo con chi usa il prodotto e verifico le mie ipotesi con piccoli test, prima di aprire Figma."),
    ("Interfacce", "Disegno anche i casi meno belli: cosa succede se manca la rete, se una lista è vuota, se qualcosa va storto."),
    ("Design system", "Ogni componente ha un nome, poche regole e un registro delle modifiche, così design e codice restano uguali."),
    ("Accessibilità", "Mentre disegno controllo che i testi si leggano bene, che i pulsanti si tocchino facilmente e che tutto funzioni anche con lo screen reader."),
]

def method_html(heading_id="metodo-titolo"):
    items = "".join(f'<li><span class="poster__word">{w}</span><span class="poster__fact">{f}</span></li>' for w, f in METODO)
    return f"""<div class="method-head"><h2 id="{heading_id}" class="h2">Come lavoro</h2><p class="lead">Quattro cose che faccio in ogni progetto.</p></div>
    <ul class="poster">{items}</ul>"""

BIO_BREVE = "UX/UI designer a Milano: app, web app e design system."
BIO = "Prima di disegnare voglio capire dove le persone si bloccano. Le ascolto, metto per iscritto i dubbi e li verifico con un test. Poi disegno le schermate, comprese quelle che si dimenticano spesso, come gli errori o le pagine vuote, e le raccolgo in un design system che gli sviluppatori possono usare senza interpretazioni."
ESPERIENZA = [
    ("UX/UI Designer", "Collecto app · Milano · tempo pieno", "gen 2026 – oggi"),
    ("UX/UI Designer, stage", "Collecto app · Milano", "lug 2025 – gen 2026"),
    ("Fashion Photographer", "Freelance · Milano", ""),
    ("Photo Retoucher & Video Editor", "PixelModa · Milano", "feb 2023 – lug 2023"),
]
FORMAZIONE = [
    ("Master in UX/UI Design", "Start2Impact", "ott 2023 – mag 2025"),
    ("Accademia di Fotografia di moda", "Ferrari Fashion School", "ott 2019 – set 2022"),
    ("Istituto Tecnico, Grafica e comunicazione", "Istituto Salesiano San Zeno", "2014 – 2019"),
]
HARD_SKILLS = ["Discovery", "Wireframing", "Prototyping", "User testing", "Grafica", "Scrittura", "HTML", "CSS"]
STRUMENTI = ["Figma", "CleverTap", "Claude", "ChatGPT", "Photoshop"]
SOFT_SKILLS = ["Team working", "Networking", "Impatto sociale", "Proattività", "Precisione", "Mentoring", "People oriented", "Creatività"]
DETTAGLI = {
    "UX/UI Designer": "Progetto e miglioro le esperienze digitali di Collecto in un ruolo trasversale tra design, prodotto e marketing. UX/UI e product design: interfacce, user flow e funzionalità dell’app, design system e identità visiva. Digital design: newsletter, landing page, template e componenti visivi per i canali di comunicazione. CRM e marketing automation: customer journey e automazioni multicanale con CleverTap, email e notifiche push per onboarding, engagement, retention e riattivazione degli utenti.",
    "UX/UI Designer, stage": "Stage in UX/UI design, proseguito con l’assunzione a tempo pieno.",
    "Fashion Photographer": "Servizi fotografici di moda, dalla direzione visiva alla post-produzione.",
    "Photo Retoucher & Video Editor": "Fotoritocco e montaggio video per contenuti moda, con attenzione alla precisione e alla coerenza visiva.",
}
KNOWS_ABOUT = ["UX design", "UI design", "Product design", "User research", "Discovery", "Usability testing", "Wireframing",
               "Prototipazione", "Architettura dell’informazione", "Design system", "Design token", "Accessibilità WCAG 2.2",
               "Brand identity", "Motion design", "User flow", "Customer journey", "CRM e marketing automation", "Email e newsletter", "Landing page", "Figma", "CleverTap", "HTML", "CSS"]
LINGUE = [("Italiano", "Madrelingua", ""), ("Inglese", "Intermedio", "")]

SKILLS = ["Discovery", "Wireframing", "Prototyping", "User testing", "Design system", "Accessibilità", "Figma"]

def in_breve(items):
    cells = "".join(f'<div><h3>{t}</h3><p>{d}</p></div>' for t, d in items)
    return f'<section class="brief" aria-labelledby="breve"><h2 id="breve" class="visually-hidden">In breve</h2>{cells}</section>'

def lezioni(testo, prossimi):
    first = "".join(f'<p class="lead">{t}</p>' for t in testo)
    return f"""<section class="section lessons" aria-label="Lezioni e prossimi passi">
    <div><h2 class="h2">Cosa ho imparato</h2>{first}</div>
    <div><h2 class="h2">Prossimi passi</h2><p class="lead">{prossimi}</p></div>
  </section>"""

def stats_html(stats):
    cells = "".join(f'<div class="stat"><p class="stat__value">{v}</p><p>{l}</p></div>' for v, l in stats)
    return f'<section class="section" aria-labelledby="numeri"><h2 id="numeri" class="h2 section-head">Il progetto in numeri</h2><div class="stats">{cells}</div></section>'

def steps_html(steps, sub):
    rows = "".join(f'<li><h3>{t}</h3><p>{d}</p></li>' for _, t, d in steps)
    return f"""<section class="section" aria-labelledby="processo">
    <div class="section-head"><h2 id="processo" class="h2">Processo</h2><p class="lead">{sub}</p></div>
    <ol class="steps">{rows}</ol>
  </section>"""

def cs_intro(title, lead, meta, row_label, phones_html):
    dl = "".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in meta)
    return f"""<section class="cs-intro intro" aria-labelledby="titolo">
    <h1 id="titolo" class="display">{title}</h1>
    <div class="cs-intro__side">
      <p class="lead">{lead}</p>
      <dl class="meta">{dl}</dl>
      <p><a class="back" href="../">{icon("arrow-left", 18)} Tutti i lavori</a></p>
    </div>
  </section>
  <div class="stage">
    <div class="phone-row" role="img" aria-label="{row_label}">{phones_html}</div>
  </div>"""

def callouts(items, cols="grid--3"):
    return f'<div class="grid {cols}">' + "".join(f'<div class="callout glass"><p class="callout__label">{t}</p><p>{d}</p></div>' for t, d in items) + "</div>"

def chips(items):
    return '<ul class="chips">' + "".join(f'<li class="chip">{s}</li>' for s in items) + "</ul>"

def timeline(items):
    return '<ul class="timeline">' + "".join(
        f'<li><span><strong>{a}</strong><span class="label">{b}</span></span><span class="label">{c}</span></li>'
        for a, b, c in items) + "</ul>"

# ---------------------------------------------------------------------------
# Pagine
# ---------------------------------------------------------------------------
HERO_SCREENS = [
    ("lavori/uci-cinemas/", "UCI Cinemas", "assets/img/uci-posti.webp", "UCI Cinemas: la scelta dei posti in sala"),
    ("lavori/jet-hr/", "Jet HR", "assets/img/jethr-m-stipendio.webp", "Jet HR: lo stipendio del mese con le differenze spiegate"),
    ("lavori/idealista/", "idealista", "assets/img/idealista-a1.webp", "idealista: la scheda annuncio con il costo mensile totale"),
]

def home():
    r = ""
    screens = "".join(
        f'<li><a href="{h}"><span class="phone"><span class="phone__screen"><img src="{src}" alt="{html.escape(alt)}" width="390" height="844"></span></span>'
        f'<span class="hero__screen-name">{t}</span></a></li>'
        for h, t, src, alt in HERO_SCREENS)
    body = f"""
<div class="wrap">
  <section class="hero" aria-labelledby="titolo">
    <div class="hero__copy">
      <h1 id="titolo" class="hero__title">UX/UI designer a Milano</h1>
      <p class="hero__lead">Ciao, sono Sebastiano. Progetto app e web app: studio come le usano le persone, disegno ogni schermata e la preparo perché gli sviluppatori possano costruirla così com’è.</p>
      <div class="hero__actions">
        <a class="btn btn--primary" href="#lavori">Guarda i lavori {icon("arrow-up-right", 18)}</a>
        <a class="btn btn--secondary" href="cv/">CV</a>
      </div>
    </div>
    <ul class="hero__screens">{screens}</ul>
  </section>

  <section class="section" id="lavori" aria-labelledby="lavori-titolo">
    <div class="work-head"><h2 id="lavori-titolo" class="h2">Lavori</h2><p class="lead">Tre case study, dalla discovery al prototipo. Progetti personali, realizzati in autonomia.</p></div>
    {work_blocks(r)}
  </section>

  <section class="section" id="metodo" aria-labelledby="metodo-titolo">
    {method_html()}
  </section>

  <section class="section" aria-labelledby="chi-titolo">
    <div class="section-head"><h2 id="chi-titolo" class="h2">Chi sono</h2></div>
    <div class="about">
      <div class="about__side">
        <div class="about__portrait"><img src="assets/img/ritratto.webp" alt="Ritratto di Sebastiano Bosi" width="960" height="1200" loading="lazy"></div>
        <dl class="facts">
          <div><dt>Ruolo</dt><dd>UX/UI Designer</dd></div>
          <div><dt>Base</dt><dd>Milano</dd></div>
          <div><dt>Mi occupo di</dt><dd>App, web app e design system</dd></div>
        </dl>
      </div>
      <div class="about__text">
        <p class="about__para">{BIO}</p>
        <div class="actions actions--stack-mobile">
          <a class="btn btn--primary" href="cv/">CV</a>
          <a class="btn btn--secondary" href="chi-sono/">Più su di me</a>
        </div>
      </div>
    </div>
    <div class="record">
      <p class="record__word">Il percorso</p>
      <div><h3>Esperienza</h3><ul>{"".join(f'<li><span>{a} · {b.split(" · ")[0]}</span><span>{c}</span></li>' for a, b, c in ESPERIENZA)}</ul></div>
      <div><h3>Formazione</h3><ul>{"".join(f'<li><span>{a} · {b}</span><span>{c}</span></li>' for a, b, c in FORMAZIONE)}</ul></div>
    </div>
  </section>
</div>"""
    return layout("", 0, CONFIG["name"], "Sebastiano Bosi, UX/UI Designer a Milano: user research, interfacce per app e web app, design system e accessibilità. Case study UCI Cinemas, Jet HR e idealista.", body, [])

def lavori():
    r = "../"
    body = f"""
<div class="wrap">
  <section class="page-intro intro" aria-labelledby="titolo">
    <h1 id="titolo" class="display">Lavori</h1>
    <p class="lead">Tre case study, dal problema al prototipo: discovery, interfacce, design system e accessibilità. Sono progetti personali, realizzati in autonomia. Ti racconto volentieri anche quelli che non trovano spazio qui.</p>
  </section>
  <section class="section" style="margin-top:clamp(56px,6vw,96px)" aria-label="Progetti">{work_blocks(r, "h2")}</section>
</div>"""
    return layout("lavori/", 1, "Lavori", "Case study di Sebastiano Bosi, UX/UI Designer: redesign di app mobile e web app, brand identity, design system e accessibilità.", body, [])

def uci():
    r = "../../"
    stats = [("85", "schermate, con percorsi principali e stati alternativi"), ("9", "aree, dal primo accesso al profilo e fedeltà"),
             ("80", "componenti nel design system, in due temi"), ("1", "assistente AI, Iris, al posto dell’acquisto rapido")]
    steps = [("search", "Discovery", "Problema riformulato e assunzioni mappate prima di disegnare qualsiasi schermata."),
             ("components", "Brand e design system", "Nuova identità, token e componenti con varianti, stati e changelog."),
             ("layout", "Flussi", "85 schermate: percorso principale, errori, vuoti, offline e caricamento per ogni area."),
             ("accessibility", "Accessibilità", "Leggibilità e contrasti verificati in entrambi i temi, con le correzioni riportate nel design system.")]
    areas = ["Onboarding e accesso", "Home", "Acquisto classico", "Acquisto con Iris", "I miei biglietti", "Ordina al bar", "Film", "Cinema", "Profilo e fedeltà"]
    rules = ["Barre flottanti sopra il contenuto (Tab Bar, riepilogo, azioni), con sfumatura al bordo di scorrimento.",
             "Forme coerenti a ogni livello, dalle card ai pulsanti, per un’interfaccia morbida e ordinata.",
             "Icone essenziali e azioni sempre nello stesso punto: chi usa l’app sa dove guardare."]
    acc = [("Leggibile in ogni tema", "Contrasti verificati nel tema blu e in quello scuro, per testi e stati sempre chiari."),
           ("Facile da toccare", "Pulsanti e controlli con aree ampie, comodi anche con una mano sola."),
           ("Per tutte le persone", "Testi che si ingrandiscono, supporto agli screen reader e informazioni mai affidate al solo colore.")]
    next_p = dict(PROJECTS[1]); next_p["large"] = True; next_p["eyebrow"] = "Prossimo progetto · Web e mobile"
    img = r + "assets/img/"
    palette = [("#3433FF", "Brand", "Sfondo principale e tema Blue", "#FEFEFE"), ("#FFDA33", "Accento", "Ellisse, azioni principali, Iris", "#272727"),
               ("#FEFEFE", "Superfici", "Testi e superfici chiare", "#3433FF"), ("#272727", "Inchiostro", "Testi su giallo e tema Dark", "#FFDA33"),
               ("#010073", "Profondo", "Card e livelli in profondità", "#CCECFF"), ("#33B4FF", "Luce", "Informazioni e stati attivi", "#010073"),
               ("#CCECFF", "Tenue", "Testi secondari su blu", "#3433FF")]
    ucicons = [("ellisse", "L’ellisse che sbuca dal buco: il simbolo in movimento"), ("occhi", "Gli occhi: guardare il cinema meglio"),
               ("popcorn", "Il popcorn a righe del bar"), ("cinepresa", "La cinepresa"), ("maschere", "Le maschere del teatro"), ("biglietto", "Il biglietto")]
    film_scenes = ["Iris sbuca da un buco nero, salta fuori e si presenta.", "Il manifesto «Watching movies better» con gli occhi delle ucicons.",
                   "Il logo e le sue varianti su bianco, nero e giallo, poi il simbolo da solo.", "La palette: sette colori, ognuno con il suo codice esadecimale e il suo ruolo.",
                   "La tipografia: Rubik per i titoli, Outfit per i testi.", "Le sei ucicons animate.",
                   "L’app in una serata: chiedi a Iris, lei cerca e trova il film, scegli i posti, confermi tu il pagamento, entri con il QR, ordini al bar senza fila e guadagni punti myUCI.",
                   "Chiusura: Iris, il logo e «Il cinema, a modo tuo»."]
    body = f"""
<div class="wrap">
  {cs_intro("UCI Cinemas", "Il redesign dell’app per comprare biglietti, ordinare al bar e farsi consigliare da Iris, un’assistente AI.", [("Ruolo", "UX/UI Designer · progetto personale"), ("Piattaforma", "App mobile"), ("Strumenti", "Figma")], "Schermate principali dell’app UCI Cinemas: Home, Iris, scelta dei posti, biglietto e bar", f'''{phone("UCI · Home", img + "uci-home.webp")}{phone("UCI · Iris", img + "iris-proposte.webp")}{phone("UCI · Posti", img + "uci-posti.webp")}{phone("UCI · Biglietto", img + "uci-biglietto.webp")}{phone("UCI · Bar", img + "uci-bar.webp")}''')}
  {in_breve([("Problema", "Comprare un biglietto richiede troppi passaggi, e l’acquisto rapido non aiuta a scegliere il film."),
              ("Il mio ruolo", "Progetto individuale: discovery, brand identity, UX, UI, design system, accessibilità e motion."),
              ("Cosa ho fatto", "Nuova identità, 85 schermate in 9 aree, 80 componenti e Iris, l’assistente AI che guida l’acquisto."),
              ("Risultato", "Un prototipo completo e accessibile, con un’identità riconoscibile, pronto per i test con utenti.")])}

  <section class="section" aria-labelledby="film">
    <div class="section-head"><h2 id="film" class="h2">Il film del progetto</h2></div>
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
      <aside class="callout glass"><p class="callout__label">Nota</p><p>Progetto non commissionato da UCI. Prezzi, titoli dei film e alcuni dati sono esempi plausibili, da verificare. Concept, testi, schermate e video sono opera originale di Sebastiano Bosi e sono protetti dal diritto d’autore (<a href="../../note-legali/">note legali</a>).</p></aside>
    </div>
  </section>

  {stats_html(stats)}

  {steps_html(steps, "Dalla discovery all’accessibilità, con il design system al centro.")}

  <section class="section" aria-labelledby="brand">
    <div class="section-head"><h2 id="brand" class="h2">Brand identity</h2></div>
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
    <div class="section-head"><h2 id="aree" class="h2">Le 9 aree dell’app</h2></div>
    <ol class="areas">{"".join(f'<li>{a}</li>' for a in areas)}</ol>
    <figure class="figure" style="margin-top:16px">
      <div class="figure__frame glass">{media("Mappa dei flussi", "figure__media figure__media--fit", img + "uci-mappa-flussi.webp", "Mappa dei flussi: dall’onboarding alla Home, e dalla Home ad acquisto classico, acquisto con Iris, film, cinema, biglietti, profilo; dal biglietto al bar e al promemoria")}</div>
      <figcaption>Mappa dei flussi: tutte le aree e i collegamenti del prototipo completo.</figcaption>
    </figure>
  </section>

  <section class="section" aria-labelledby="ds">
    <div class="section-head"><h2 id="ds" class="h2">Design system</h2></div>
    <p class="lead" style="margin-bottom:24px">Ogni schermata usa componenti del design system: prima si riusa ciò che esiste, poi si crea il nuovo e lo si aggiunge alla libreria, con ogni modifica nel changelog.</p>
    <ul class="notes">{"".join(f'<li><p>{t}</p></li>' for t in rules)}</ul>
    <figure class="figure" style="margin-top:16px">
      <div class="figure__frame glass">{media("Design system", "figure__media figure__media--fit", img + "uci-design-system.webp", "Design system UCI Cinemas: titolo e una tavola di componenti reali dell’app in tema Dark")}</div>
      <figcaption>Alcuni componenti del design system in tema scuro: dalla mappa dei posti al biglietto, dal bar alla carta fedeltà.</figcaption>
    </figure>
  </section>

  <section class="section" aria-labelledby="a11y">
    <div class="section-head"><h2 id="a11y" class="h2">Accessibilità</h2></div>
    <ul class="notes">{"".join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in acc)}</ul>
  </section>

  {lezioni(["Partire dal design system ha reso più veloci le 85 schermate: ogni componente nuovo entrava subito in libreria, con il suo changelog.",
            "Rifarei la scelta di far confermare sempre il pagamento all’utente: un’assistente AI deve aiutare a decidere, non decidere al posto tuo.",
            "Cambierei il momento della verifica di accessibilità: alcuni contrasti li ho corretti a schermate finite. Oggi li controllo già quando definisco i colori."],
           "Test con utenti, pagamenti digitali, immagini definitive e passaggio agli sviluppatori.")}

  {next_block(next_p, r)}
</div>"""
    glows = [("blue", "-14%", "-240px", "62vw", "620px", .42), ("lavender", "55%", "-160px", "56vw", "520px", .3),
             ("warm", "60%", "700px", "28vw", "320px", .22), ("lavender", "-10%", "2600px", "50vw", "600px", .16), ("blue", "50%", "4600px", "50vw", "600px", .16)]
    fonts = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rubik:wght@900&family=Outfit:wght@400;600&display=swap">\n'
    return layout("lavori/uci-cinemas/", 2, "UCI Cinemas, case study", "Case study del redesign dell’app UCI Cinemas: brand identity, design system, assistente AI Iris e accessibilità.", body, glows, fonts)

def jethr():
    r = "../../"
    img = r + "assets/img/"
    stats = [("20", "schermate tra web app e app mobile"), ("1", "sola libreria di componenti per desktop e mobile"),
             ("1", "busta paga riprogettata, chiara e completa"), ("4", "domande dei dipendenti al centro dell’esperienza")]
    steps = [("search", "Discovery", "Problema riformulato, domande reali dei dipendenti e vincoli di legge prima di disegnare."),
             ("components", "Design system", "Il brand del sito esteso in token, stili di testo e componenti con variante desktop e mobile."),
             ("layout", "Desktop e mobile", "Web app e app con gli stessi componenti, per un’esperienza coerente ovunque."),
             ("accessibility", "Busta paga e verifica", "Cedolino riprogettato, busta paga spiegata voce per voce, piano di test e verifica di accessibilità.")]
    questions = [("Quanto ricevo, e quando?", "Netto e data di accredito sono la prima cosa in home. Il netto è nascosto finché non tocchi l’occhio."),
                 ("Perché è diverso dal mese scorso?", "Ogni busta paga dice cosa è cambiato rispetto al mese prima, con le voci che spiegano la differenza."),
                 ("Quanti giorni di ferie ho?", "Ferie e permessi in giorni, con le ore come dettaglio e la stima al 31 dicembre."),
                 ("Dove finiscono i soldi tra lordo e netto?", "Una barra divisa in tre: quello che resta a te, i contributi per la pensione e le tasse.")]
    legal = [("Forma libera", "La busta paga non ha un modello fisso: si può riorganizzare, purché contenga tutti i dati."),
             ("Stessi dati, nuove parole", "Importi e codici restano quelli ufficiali: cambia solo come si leggono."),
             ("Privacy prima di tutto", "Dati personali protetti per default: lo stipendio resta nascosto finché non lo vuoi vedere."),
             ("Trasparenza", "Dal profilo si possono chiedere le informazioni sulla retribuzione del proprio ruolo.")]
    rules = ["Stessi componenti su desktop e mobile: chi passa dal computer al telefono ritrova le stesse righe, card e pulsanti.",
             "Forme coerenti a ogni livello, con pulsanti a capsula e card morbide, fedeli al brand.",
             "La stessa tipografia ovunque, dai titoli agli importi, anche negli elementi di sistema."]
    palette = [("#DFEB57", "Lime", "Accento del brand e stati in evidenza", "#11150A"), ("#11150A", "Nero", "Testi, pulsanti principali e card dello stipendio", "#DFEB57"),
               ("#F8FAF5", "Pagina", "Sfondo delle schermate", "#11150A"), ("#FFFFFF", "Card", "Superfici e liste", "#11150A"),
               ("#0BB098", "Ferie", "Categoria nel calendario", "#11150A"), ("#4330B2", "Permesso", "Categoria e contributi", "#FFFFFF"),
               ("#B01F42", "Malattia", "Categoria e tasse", "#FFFFFF")]
    acc = [("Leggibile", "Contrasti verificati sui colori del brand, perché importi e date si leggano al primo colpo."),
           ("Facile da usare", "Aree di tocco ampie e azioni sempre nello stesso punto, su desktop e mobile."),
           ("Chiara per tutti", "Parole semplici al posto delle sigle, per chi non conosce il linguaggio delle paghe.")]
    next_p = dict(PROJECTS[2]); next_p["eyebrow"] = "Prossimo progetto · Brand identity e app"
    body = f"""
<div class="wrap">
  {cs_intro("Jet HR", "Il redesign dell’area dipendente di Jet HR, su desktop e mobile, e una busta paga che si capisce anche senza conoscere le sigle.", [("Ruolo", "UX/UI Designer · progetto personale"), ("Piattaforma", "Desktop e mobile"), ("Strumenti", "Figma")], "Schermate dell’app mobile di Jet HR: home, tempo libero, stipendio, busta paga spiegata e calcolo dell’IRPEF", f'''{phone("Jet HR · Home", img + "jethr-m-home.webp")}{phone("Jet HR · Tempo libero", img + "jethr-m-tempo.webp")}{phone("Jet HR · Stipendio", img + "jethr-m-stipendio.webp")}{phone("Jet HR · Busta paga", img + "jethr-m-busta.webp")}{phone("Jet HR · Calcolo IRPEF", img + "jethr-m-irpef.webp")}''')}
  {in_breve([("Problema", "L’app è il desktop rimpicciolito e la busta paga parla la lingua del consulente del lavoro."),
              ("Il mio ruolo", "Progetto individuale: discovery, ricerca normativa, UX, UI, design system e piano di test."),
              ("Cosa ho fatto", "Web app e app mobile con gli stessi componenti, un nuovo cedolino e una busta paga spiegata voce per voce."),
              ("Risultato", "Un’area dipendente che risponde subito alle domande più frequenti, pronta per i test con utenti.")])}

  <section class="section split" aria-labelledby="progetto">
    <h2 id="progetto" class="h3">Il progetto</h2>
    <div class="stack">
      <p class="lead lead--primary">Jet HR gestisce le paghe di molte piccole aziende italiane. L’area dei dipendenti è dove si guarda la busta paga, si chiedono le ferie, si caricano gli scontrini e si scaricano i documenti. Oggi l’app mobile è la versione desktop rimpicciolita, e la busta paga parla la lingua del consulente del lavoro. Ho riprogettato entrambe partendo da una domanda: cosa vuole sapere davvero un dipendente quando apre l’app?</p>
      <aside class="callout glass"><p class="callout__label">Nota</p><p>Concept personale, non commissionato né approvato da Jet HR. Persone, aziende e importi sono fittizi. I vincoli di legge vengono da una ricerca su fonti pubbliche, usata solo a scopo progettuale: non sono consulenza legale o fiscale. Concept, testi, schermate e video sono opera originale di Sebastiano Bosi e sono protetti dal diritto d’autore (<a href="../../note-legali/">note legali</a>).</p></aside>
    </div>
  </section>

  {stats_html(stats)}

  {steps_html(steps, "Dalle domande dei dipendenti ai test, con un solo design system.")}

  <section class="section" aria-labelledby="domande">
    <div class="section-head"><h2 id="domande" class="h2">Le domande giuste</h2></div>
    <p class="lead" style="max-width:760px;margin-bottom:24px">Chi apre l’area dipendente ha quasi sempre una domanda precisa. Ho messo in ordine quelle più frequenti e ho costruito la home e la busta paga per rispondere prima a quelle.</p>
    <ul class="notes">{"".join(f'<li><h3>{q}</h3><p>{a}</p></li>' for q, a in questions)}</ul>
    <figure class="figure" style="margin-top:16px">
      <div class="figure__frame glass">{media("Domande dei dipendenti", "figure__media figure__media--fit", img + "jethr-domande.webp", "Tavola di discovery: le domande di un dipendente raggruppate per tema, da «Quanto e quando» a «Dov’è il documento»")}</div>
      <figcaption>Le domande raggruppate per tema e frequenza: guidano l’ordine dei contenuti in home e nella busta paga.</figcaption>
    </figure>
  </section>

  <section class="section" aria-labelledby="legge">
    <div class="section-head"><h2 id="legge" class="h2">Cosa si può cambiare</h2></div>
    <p class="lead" style="max-width:760px;margin-bottom:24px">Prima di ridisegnare la busta paga ho verificato cosa è obbligatorio e cosa no. La forma è libera, il contenuto no.</p>
    <ul class="notes">{"".join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in legal)}</ul>
  </section>

  <section class="section" aria-labelledby="desktop">
    <div class="section-head"><h2 id="desktop" class="h2">La web app</h2></div>
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
      <h2 id="ios" class="h2">L’app mobile</h2>
      <p class="lead">Gli elementi di sistema restano quelli nativi, così l’app è subito familiare. Dentro, gli stessi componenti della web app: chi passa dal computer al telefono ritrova le stesse righe, le stesse card e gli stessi pulsanti.</p>
      <aside class="callout glass"><p class="callout__label">Decisione</p><p>Nella barra in basso le sezioni usano le icone di Jet HR, le stesse della versione desktop: il brand si riconosce ovunque.</p></aside>
    </div>
    <div class="phones phones--compact" role="img" aria-label="Tre schermate dell’app mobile: richiesta di assenza, stipendio e calcolo dell’IRPEF">
      {phone("Richiedi un’assenza", img + "jethr-m-assenza.webp")}{phone("Stipendio", img + "jethr-m-stipendio.webp")}{phone("Tasse sul reddito", img + "jethr-m-irpef.webp")}
    </div>
  </section>

  <section class="section" aria-labelledby="busta">
    <div class="section-head"><h2 id="busta" class="h2">La busta paga</h2></div>
    <p class="lead" style="max-width:760px;margin-bottom:24px">Il PDF ufficiale resta il documento legale, ma riorganizzato per domande. Nell’app, la vista spiegata mette ogni voce in parole semplici, con il nome ufficiale e il codice accanto. Gli importi sono gli stessi, cambiano le parole.</p>
    <figure class="figure">
      <div class="figure__frame glass">{media("Busta paga spiegata", "figure__media figure__media--fit", img + "jethr-d-busta.webp", "Busta paga di settembre spiegata: netto, differenze rispetto ad agosto, dal lordo al netto e tutte le voci")}</div>
      <figcaption>Busta paga spiegata: cosa è cambiato rispetto ad agosto, dove vanno i soldi tra lordo e netto, ogni voce con il suo calcolo (dettaglio della schermata).</figcaption>
    </figure>
    <div class="grid grid--2" style="margin-top:16px;align-items:start">
      <figure class="figure">
        <div class="figure__frame glass">{media("Cedolino", "figure__media figure__media--fit", img + "jethr-cedolino.webp", "Cedolino riprogettato: dati del datore e del lavoratore, riepilogo, competenze, trattenute, ferie, TFR e presenze del mese")}</div>
        <figcaption>Il cedolino: riepilogo in alto, poi competenze e trattenute con codici e spiegazione breve.</figcaption>
      </figure>
      <figure class="figure">
        <div class="figure__frame glass">{media("Dal documento alla spiegazione", "figure__media figure__media--fit", img + "jethr-strategia.webp", "Tavola di strategia: per ogni domanda dell’utente, dove trova la risposta nell’app; per ogni dato obbligatorio, dove sta nel PDF")}</div>
        <figcaption>Ogni domanda dell’utente ha il suo posto nell’app, ogni dato obbligatorio il suo posto nel PDF.</figcaption>
      </figure>
    </div>
  </section>

  <section class="section" aria-labelledby="ds">
    <div class="section-head"><h2 id="ds" class="h2">Design system</h2></div>
    <p class="lead" style="max-width:760px;margin-bottom:24px">Colori e caratteri vengono dal sito di Jet HR. Li ho trasformati in variabili e stili, poi ho aggiunto i componenti che servivano all’app, ognuno con una variante desktop e una mobile.</p>
    <h3 class="h4 brand-sub">Colore</h3>
    <ul class="swatches">{"".join(f'<li class="swatch" style="background:{h};color:{fg}"><span class="swatch__hex">{h}</span><span class="swatch__name">{n}</span><span class="swatch__use">{u}</span></li>' for h, n, u, fg in palette)}</ul>
    <h3 class="h4 brand-sub">Tipografia</h3>
    <div class="grid grid--2">
      <div class="type-card glass"><p class="type-card__sample" style="font-family:'Mona Sans',sans-serif;font-weight:800">Aa</p><div><p class="type-card__name" style="font-family:'Mona Sans',sans-serif;font-weight:800">Mona Sans</p><p class="muted">Titoli e importi</p></div></div>
      <div class="type-card glass"><p class="type-card__sample" style="font-family:'Wix Madefor Display',sans-serif">Aa</p><div><p class="type-card__name" style="font-family:'Wix Madefor Display',sans-serif">Wix Madefor Display</p><p class="muted">Testi ed etichette</p></div></div>
    </div>
    <ul class="notes" style="margin-top:clamp(32px,4vw,48px)">{"".join(f'<li><p>{t}</p></li>' for t in rules)}</ul>
    <figure class="figure" style="margin-top:16px">
      <div class="figure__frame glass">{media("Componenti condivisi", "figure__media figure__media--fit", img + "jethr-componenti.webp", "Tavola dei componenti condivisi: Toggle, Riga lista, Intestazione sezione, Controllo segmentato, Card netto e Scelta tipo, ognuno in versione desktop e mobile")}</div>
      <figcaption>I componenti condivisi, ognuno con la variante desktop e quella mobile.</figcaption>
    </figure>
  </section>

  <section class="section" aria-labelledby="a11y">
    <div class="section-head"><h2 id="a11y" class="h2">Accessibilità e test</h2></div>
    <ul class="notes">{"".join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in acc)}</ul>
    <aside class="callout glass" style="margin-top:16px"><p class="callout__label">Prossima verifica</p><p>Usability test con dipendenti su desktop e mobile, sui compiti di ogni giorno: capire quanto si riceve e quando, spiegare una voce della busta paga, chiedere un giorno di ferie, caricare una spesa, trovare la Certificazione Unica.</p></aside>
  </section>

  {lezioni(["Studiare i vincoli di legge prima di disegnare ha cambiato il progetto: la forma della busta paga è libera, il contenuto no. Questo mi ha detto esattamente quanto potevo osare.",
            "Rifarei la scelta di usare gli stessi componenti su desktop e mobile: l’esperienza è coerente e il design system resta piccolo.",
            "La prossima volta porterei prima le domande dei dipendenti davanti a persone vere, invece di partire solo da fonti pubbliche."],
           "Usability test con dipendenti veri, verifica dei testi con un consulente del lavoro, modalità scura e Dynamic Type, passaggio agli sviluppatori.")}

  {next_block(next_p, r)}
</div>"""
    glows = [("blue", "-14%", "-240px", "62vw", "620px", .42), ("lavender", "55%", "-160px", "56vw", "520px", .3),
             ("warm", "60%", "700px", "28vw", "320px", .22), ("lavender", "-10%", "2600px", "50vw", "600px", .16), ("blue", "50%", "4600px", "50vw", "600px", .16)]
    fonts = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Mona+Sans:wght@800&family=Wix+Madefor+Display:wght@400&display=swap">\n'
    return layout("lavori/jet-hr/", 2, "Jet HR, case study", "Case study del redesign dell’area dipendente di Jet HR: web app e app mobile con gli stessi componenti e una busta paga che si capisce.", body, glows, fonts)

IDEALISTA_ICONS = {"Casa": "<path d=\"M9 43.5L36 21L63 43.5V75H45V57H27V75H9V43.5Z\"/>", "Cerca": "<path d=\"M31.5 22.5A21 21 0 1 0 31.5 64.5A21 21 0 1 0 31.5 22.5Z\"/><path d=\"M48 60L63 75\"/>", "Mappa": "<path d=\"M9 30L27 21L45 30L63 21V66L45 75L27 66L9 75V30Z\"/><path d=\"M27 21V66\"/><path d=\"M45 30V75\"/>", "Preferiti": "<path d=\"M36 72L12 48V33L21 24H30L36 30L42 24H51L60 33V48L36 72Z\"/>", "Messaggi": "<path d=\"M9 24H63V63H27L9 75V24Z\"/>", "Filtri": "<path d=\"M9 33H39\"/><path d=\"M51 33H63\"/><path d=\"M39 24H51V42H39V24Z\"/><path d=\"M9 63H21\"/><path d=\"M33 63H63\"/><path d=\"M21 54H33V72H21V54Z\"/>", "Avvisi": "<path d=\"M18 63V39C18 29 26 21 36 21C46 21 54 29 54 39V63L60 69H12L18 63Z\"/><path d=\"M30 75H42\"/>", "Profilo": "<path d=\"M24 21H48V45H24V21Z\"/><path d=\"M12 75V66L21 57H51L60 66V75\"/>"}

def idealista_icon(name):
    return (f'<svg viewBox="0 0 72 84" width="48" height="56" fill="none" stroke="currentColor" stroke-width="6" '
            f'stroke-linecap="square" stroke-linejoin="miter" aria-hidden="true">{IDEALISTA_ICONS[name]}</svg>')

def idealista():
    r = "../../"
    img = r + "assets/img/"
    stats = [("39", "schermate, dalla ricerca alla pubblicazione"), ("54", "icone ridisegnate sulla geometria del brand"),
             ("7", "flussi completi, con stati vuoti, errori e conferme"), ("1", "sola azione magenta per schermata: la CTA")]
    steps = [("search", "Discovery", "Sito, app e recensioni pubbliche analizzati: problemi riformulati in assunzioni da validare."),
             ("components", "Brand identity", "Logo, pixel, colore, tipografia, icone, tono di voce, fotografia e motion."),
             ("layout", "Architettura e flussi", "Navigazione a 5 voci e 39 schermate, con stati vuoti, errori e conferme."),
             ("accessibility", "Design system", "Token del brand, componenti con varianti, modalità scura e verifica di accessibilità.")]
    insights = [("Prezzi poco chiari", "Il canone non dice quanto si spende davvero: spese, riscaldamento e deposito arrivano dopo, spesso in chat."),
                ("Fiducia da conquistare", "Annunci falsi e richieste di caparra prima della visita sono la paura più citata nelle recensioni."),
                ("Ricerca rigida", "I filtri sono tanti e nascosti. Chi cerca ragiona per frasi: «trilocale con balcone a Isola sotto 1.400 €».")]
    palette = [("#E1F56E", "Lime", "Superficie di brand, mai testo su chiaro", "#141414"), ("#141414", "Nero", "Testi e stati attivi", "#FAFBF9"),
               ("#B62682", "Magenta", "Solo azione: una CTA per schermata", "#FFFFFF"), ("#FAFBF9", "Carta", "Sfondo dell’interfaccia", "#141414")]
    icon_rules = [("Griglia comune", "Tutte le icone nascono dalla stessa griglia."), ("Tratto deciso", "Terminali squadrati, come il pixel del logo."),
                  ("Geometria", "Linee rette, curve solo dove servono."), ("Stato attivo", "Icona su nero con il pixel lime sopra.")]
    brand_slides = [("b-pixel", "Il pixel come sistema", "Il pixel quadrato del logo diventa il modulo: app icon, pin della mappa, indicatori di novità e pattern."),
                    ("b-griglia", "La griglia", "La griglia che regola impaginati, schermate e applicazioni."),
                    ("b-tono", "Tono di voce", "Diretto, con i numeri in vista, mai ironico nei momenti di rischio."),
                    ("b-foto", "Fotografia", "Case vere e luce naturale: le foto aiutano a decidere, non a sognare."),
                    ("b-applicazioni", "Applicazioni", "Il sistema applicato a cartelli, comunicazione e touchpoint."),
                    ("b-motion", "Motion", "Il pixel si muove a scatti, l’interfaccia scorre in modo fluido.")]
    flows = [("Ricerca", "Cerca come parli", "La frase diventa filtri visibili e modificabili. I filtri di fiducia, «Solo verificati» ed «Escludi aste», sono chip sempre in vista. Sulla mappa il pixel dice cosa è nuovo, selezionato o già visto.",
              [("r2", "Ricerca in linguaggio naturale: la frase trilocale con balcone a Isola tradotta in filtri"), ("r3", "Risultati con i chip Solo verificati e prezzo massimo"), ("r4", "Mappa con i prezzi nei pin quadrati")]),
             ("Annuncio e contatto", "Quanto spendi davvero", "Sopra la piega: prezzo, €/m² e costo mensile totale con spese e riscaldamento. Una sola CTA, «Contatta». Il messaggio è già pronto e la visita si prenota in app.",
              [("a1", "Scheda annuncio con il costo mensile totale"), ("a3", "Messaggio precompilato con domande rapide"), ("a5", "Richiesta di visita inviata, con i consigli per la visita")]),
             ("Salvati e sicurezza", "Sicurezza nel momento del rischio", "Le ricerche salvate restano vive: modifichi un filtro e si aggiorna da sola, con Annulla. Se in chat qualcuno chiede soldi prima della visita, l’app avvisa, oscura l’IBAN e fa segnalare in due tocchi.",
              [("s2", "Ricerche salvate con avvisi regolabili"), ("s3", "Ricerca salvata aggiornata, con il toast Annulla"), ("m3", "Chat con l’allerta sulla richiesta di denaro")]),
             ("Pubblica", "Chi pubblica sa il prezzo", "Pubblicare un annuncio in 5 passi, con bozza automatica e indirizzo privato di default. Il prezzo arriva da idealista/valuta e la verifica dell’identità dà il badge «Verificato».",
              [("c1", "Pubblica: annunci dell’utente e servizi per proprietari"), ("c6", "Passo 5: canone con la forbice di mercato di idealista/valuta"), ("c8", "Annuncio online e verificato")])]
    nav = ["Home", "Salvati", "Messaggi", "Pubblica", "Profilo"]
    rules = ["Una sola azione magenta per schermata: è sempre la CTA principale.",
             "Stato attivo come nel brand: tile nero, pixel lime sopra l’icona, etichetta bianca.",
             "La modalità scura nasce dagli stessi token, senza duplicare i componenti."]
    acc = [("Contrasti verificati", "In modalità chiara e scura, con il lime usato come superficie e mai come testo."),
           ("Facile da toccare", "Chip, pin della mappa e pulsanti pensati per il pollice."),
           ("Stati chiari", "Ogni stato usa più di un segnale: colore, icona o testo.")]
    film_scenes = ["Su nero compare un pixel lime, poi una griglia di pixel che si accende.", "La griglia diventa il logo idealista, con il claim «Ora è il momento».",
                   "Su lime, «Colore con un ruolo»: nero per la lettura, magenta per l’azione, carta per lo sfondo.",
                   "La tipografia: Funnel Display, con un prezzo nel cartellino lime.", "La mappa: i prezzi nei pin, e il pin selezionato diventa nero con il pixel lime.",
                   "L’app icon «id» con il pixel.", "Chiusura su lime: il logo, il claim «Ora è il momento. Segui il tuo intuito.» e la firma del progetto."]
    next_p = dict(PROJECTS[0]); next_p["large"] = True; next_p["eyebrow"] = "Prossimo progetto · App mobile"
    def phones3(items):
        return "".join(phone(n, img + f"idealista-{n}.webp", a) for n, a in items)
    body = f"""
<div class="wrap">
  {cs_intro("idealista", "Una nuova brand identity e l’app che ne nasce: trovare casa con prezzi chiari e annunci verificati, dalla ricerca alla visita.", [("Ruolo", "Brand e UX/UI Designer · progetto personale"), ("Piattaforma", "App mobile"), ("Strumenti", "Figma")], "Schermate principali dell’app idealista: onboarding, Home, risultati, scheda annuncio e pubblicazione", f'''{phone("idealista · Onboarding", img + "idealista-o1.webp")}{phone("idealista · Home", img + "idealista-r1.webp")}{phone("idealista · Risultati", img + "idealista-r3.webp")}{phone("idealista · Annuncio", img + "idealista-a1.webp")}{phone("idealista · Pubblica", img + "idealista-c8.webp")}''')}
  {in_breve([("Problema", "Prezzi poco chiari, paura degli annunci falsi e filtri rigidi rendono difficile scegliere casa."),
              ("Il mio ruolo", "Progetto individuale: brand identity, discovery, architettura, UI, design system e video del brand."),
              ("Cosa ho fatto", "Rebrand evolutivo, 54 icone, 39 schermate in 7 flussi e un design system con modalità scura."),
              ("Risultato", "Costo mensile totale in vista, ricerca in linguaggio naturale e avvisi anti-truffa in chat.")])}

  <section class="section" aria-labelledby="film">
    <div class="section-head"><h2 id="film" class="h2">Il video del brand</h2></div>
    <figure class="figure">
      <div class="figure__frame glass">
        <video class="film film--idealista" controls playsinline preload="none" width="1920" height="1080" poster="{img}idealista-video-poster.webp" aria-describedby="film-descrizione">
          <source src="{r}assets/video/idealista-brand-video.mp4" type="video/mp4">
          <a href="{r}assets/video/idealista-brand-video.mp4">Scarica il video (MP4)</a>
        </video>
      </div>
      <figcaption>La nuova brand identity di idealista in 20 secondi.</figcaption>
    </figure>
    <details class="details glass" id="film-descrizione">
      <summary>Descrizione del video</summary>
      <ol>{"".join(f"<li>{t}</li>" for t in film_scenes)}</ol>
    </details>
  </section>


  <section class="section split" aria-labelledby="progetto">
    <h2 id="progetto" class="h3">Il progetto</h2>
    <div class="stack">
      <p class="lead lead--primary">Ho ripensato idealista partendo dal marchio: il logo a griglia di pixel diventa un carattere vero, e il pixel quadrato resta come segno di tutto il sistema. Da lì ho riprogettato l’app partendo dal sito attuale, con un obiettivo: far capire subito quanto costa davvero una casa e di chi fidarsi.</p>
      <aside class="callout glass"><p class="callout__label">Nota</p><p>Concept non ufficiale, non commissionato da idealista. Prezzi, indirizzi e annunci sono esempi; le foto della fotografia sono generate con AI per illustrare il trattamento. Concept, testi, schermate e video sono opera originale di Sebastiano Bosi e sono protetti dal diritto d’autore (<a href="../../note-legali/">note legali</a>).</p></aside>
    </div>
  </section>

  {stats_html(stats)}

  {steps_html(steps, "Dal marchio all’app, con gli stessi token dal primo all’ultimo passo.")}

  <section class="section" aria-labelledby="brand">
    <div class="section-head"><h2 id="brand" class="h2">Brand identity</h2></div>
    <p class="lead" style="max-width:760px;margin-bottom:24px">Il vecchio logo era una griglia di 7 moduli: forte, ma rigido e poco leggibile in piccolo. Il nuovo usa Funnel Display Bold e tiene un solo pixel, quello sulla «i»: sempre quadrato, mai arrotondato.</p>
    <div class="brand-grid">
      <div class="brand-tile brand-tile--idealista"><img src="{img}brand/idealista-logo.svg" alt="Logo idealista: scritta bianca su nero, con il puntino della prima i come pixel quadrato lime" width="271" height="49"></div>
      <div class="brand-tile brand-tile--idealista-claim"><p class="brand-claim brand-claim--funnel">Ora è il momento. Segui il tuo intuito.</p></div>
    </div>
    <figure class="figure" style="margin-top:16px">
      <div class="figure__frame glass">{media("Logo prima e dopo", "figure__media figure__media--fit", img + "idealista-b-logo.webp", "Il logo prima e dopo: dalla griglia di pixel alla scritta in Funnel Display con i puntini quadrati")}</div>
      <figcaption>Il logo, prima e dopo.</figcaption>
    </figure>
    <h3 class="h4 brand-sub">Colore</h3>
    <ul class="swatches swatches--4">{"".join(f'<li class="swatch" style="background:{h};color:{fg}"><span class="swatch__hex swatch__hex--funnel">{h}</span><span class="swatch__name">{n}</span><span class="swatch__use">{u}</span></li>' for h, n, u, fg in palette)}</ul>
    <h3 class="h4 brand-sub">Tipografia</h3>
    <div class="grid grid--2">
      <div class="type-card glass"><p class="type-card__sample type-card__sample--funnel-d">Aa</p><div><p class="type-card__name type-card__name--funnel-d">Funnel Display</p><p class="muted">Titoli e prezzi, in Bold</p></div></div>
      <div class="type-card glass"><p class="type-card__sample type-card__sample--funnel-s">Aa</p><div><p class="type-card__name type-card__name--funnel-s">Funnel Sans</p><p class="muted">Interfaccia e testi, da Regular a SemiBold</p></div></div>
    </div>
    <h3 class="h4 brand-sub">Iconografia</h3>
    <ul class="id-icons">{"".join(f'<li class="id-icon{" id-icon--active" if n == "Casa" else ""}">{idealista_icon(n)}<span>{n}</span></li>' for n in IDEALISTA_ICONS)}</ul>
    <ul class="notes" style="margin-top:16px">{"".join(f'<li><h3>{a}</h3><p>{b}</p></li>' for a, b in icon_rules)}</ul>
    <h3 class="h4 brand-sub">Il sistema</h3>
    <div class="grid grid--2" style="align-items:start">{"".join(f'<figure class="figure"><div class="figure__frame glass">{media(t, "figure__media figure__media--fit", img + f"idealista-{n}.webp", d)}</div><figcaption><strong>{t}.</strong> {d}</figcaption></figure>' for n, t, d in brand_slides)}</div>
  </section>

  <section class="section" aria-labelledby="discovery">
    <div class="section-head"><h2 id="discovery" class="h2">Discovery</h2></div>
    <div class="grid grid--3">{"".join(f'<div class="card glass stack" style="--gap:12px;border-radius:var(--r-card);padding:clamp(24px,3vw,40px)"><h3 class="h4">{t}</h3><p class="muted">{d}</p></div>' for t, d in insights)}</div>
    <aside class="callout glass" style="margin-top:16px"><p class="callout__label">Limite</p><p>Discovery da desk research: sito, store e recensioni pubbliche. Le assunzioni vanno validate con test di usabilità e interviste a chi cerca e affitta casa.</p></aside>
  </section>

  <section class="section" aria-labelledby="architettura">
    <div class="section-head"><h2 id="architettura" class="h2">Architettura</h2></div>
    <p class="lead" style="max-width:760px;margin-bottom:24px">Una navigazione con le etichette di tutte le app immobiliari. «Pubblica» raccoglie quello che sul sito è sparso nella home: i tuoi annunci, idealista/valuta, i mutui e le agenzie.</p>
    <ol class="areas">{"".join(f'<li>{a}</li>' for a in nav)}</ol>
    <div class="grid grid--2" style="margin-top:16px;align-items:start">
      <figure class="figure"><div class="figure__frame glass">{media("Mappa dell’app", "figure__media figure__media--fit", img + "idealista-mappa.webp", "Mappa dell’app: le cinque voci della tab bar e le schermate di ognuna")}</div><figcaption>La mappa dell’app.</figcaption></figure>
      <figure class="figure"><div class="figure__frame glass">{media("Flussi", "figure__media figure__media--fit", img + "idealista-flussi.webp", "I sette flussi: onboarding, ricerca, annuncio e contatto, salvati, messaggi, pubblica, profilo")}</div><figcaption>I sette flussi, dall’onboarding al profilo.</figcaption></figure>
    </div>
  </section>

  {"".join(f"""<section class="section split split--wide" aria-labelledby="flusso-{k}">
    <div class="stack">
      <h2 id="flusso-{k}" class="h2">{t}</h2>
      <p class="lead"><strong>{lab}.</strong> {d}</p>
    </div>
    <div class="phones phones--compact" role="img" aria-label="{html.escape(' · '.join(a for _, a in ph))}">{phones3(ph)}</div>
  </section>""" for k, (lab, t, d, ph) in enumerate(flows, 1))}

  <section class="section" aria-labelledby="ds">
    <div class="section-head"><h2 id="ds" class="h2">Design system</h2></div>
    <p class="lead" style="margin-bottom:24px">Brand e app parlano la stessa lingua: colori, spazi e componenti nascono dagli stessi token, in modalità chiara e scura, e ogni componente è documentato.</p>
    <ul class="notes">{"".join(f'<li><p>{t}</p></li>' for t in rules)}</ul>
    <div class="grid grid--2" style="margin-top:16px;align-items:start">
      <figure class="figure"><div class="figure__frame glass">{media("Componenti", "figure__media figure__media--fit", img + "idealista-componenti.webp", "Tavola dei componenti: ListingCard, TabBar, Button, PricePin e Badge con le loro varianti")}</div><figcaption>Alcuni componenti: ListingCard, TabBar, Button, PricePin e Badge.</figcaption></figure>
      <figure class="figure"><div class="figure__frame glass">{media("Icone", "figure__media figure__media--fit", img + "idealista-icone.webp", "Parte del set di 54 icone con terminali squadrati")}</div><figcaption>Una parte delle 54 icone.</figcaption></figure>
    </div>
  </section>

  <section class="section" aria-labelledby="a11y">
    <div class="section-head"><h2 id="a11y" class="h2">Accessibilità</h2></div>
    <ul class="notes">{"".join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in acc)}</ul>
  </section>

  {lezioni(["Un rebrand evolutivo è più difficile di uno da zero: il lavoro vero è decidere cosa tenere. Tenere solo il pixel quadrato ha dato coerenza a logo, icone, mappa e motion.",
            "Rifarei la regola di una sola azione magenta per schermata: ha semplificato decine di decisioni sull’interfaccia.",
            "Cambierei l’ordine: farei qualche intervista prima di chiudere i flussi. Le recensioni dicono cosa non funziona, non sempre perché."],
           "Test di usabilità, interviste a chi affitta da privato, foto reali al posto dei segnaposto e passaggio agli sviluppatori.")}

  {next_block(next_p, r)}
</div>"""
    glows = [("blue", "-14%", "-240px", "62vw", "620px", .42), ("lavender", "55%", "-160px", "56vw", "520px", .3),
             ("warm", "60%", "700px", "28vw", "320px", .22), ("lavender", "-10%", "2600px", "50vw", "600px", .16), ("blue", "50%", "4600px", "50vw", "600px", .16)]
    fonts = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Funnel+Display:wght@600;700&family=Funnel+Sans:wght@400;600&display=swap">\n'
    return layout("lavori/idealista/", 2, "idealista, case study", "Case study del rebranding di idealista e della nuova app: logo, pixel, colore, tipografia e icone, 39 schermate, design system e video del brand.", body, glows, fonts)

def chi_sono():
    body = f"""
<div class="wrap">
  <section class="about-hero" style="padding-top:clamp(64px,8vw,120px)" aria-labelledby="titolo">
    <div class="stack intro" style="--gap:clamp(20px,2vw,28px)">
      <h1 id="titolo" class="display" style="max-width:10ch">Ciao, sono Sebastiano.</h1>
      <p class="lead" style="max-width:720px">{BIO}</p>
      <div class="actions actions--stack-mobile">
        <a class="btn btn--primary" href="../cv/">CV</a>
        <a class="btn btn--secondary" href="{CONFIG['linkedin']}" rel="me noopener" target="_blank">LinkedIn</a>
      </div>
    </div>
    <div class="figure__frame glass portrait">{media("Ritratto", "figure__media", "../assets/img/ritratto.webp", "Ritratto di Sebastiano Bosi")}</div>
  </section>

  <section class="section" id="metodo" aria-labelledby="metodo-titolo">
    {method_html()}
  </section>

  <section class="section" aria-labelledby="progetti-titolo">
    <div class="section-head"><h2 id="progetti-titolo" class="h2">Dai miei progetti</h2><p class="lead">Tre case study personali, dalla discovery al prototipo.</p></div>
    <ul class="mini-work">{"".join(f'<li><a href="../{p["slug"]}"><span class="mini-work__img"><img src="../{p["img"]}" alt="{html.escape(p["alt"])}" loading="lazy" width="1600" height="900"></span><span class="h4">{p["title"]}</span><span class="muted">{p["kind"]}</span></a></li>' for p in PROJECTS)}</ul>
  </section>

  <section class="section grid grid--2 path" aria-label="Percorso">
    <div class="stack" style="--gap:12px"><h2 class="h3">Esperienza</h2>{timeline(ESPERIENZA)}</div>
    <div class="stack" style="--gap:12px"><h2 class="h3">Formazione</h2>{timeline(FORMAZIONE)}<p><a class="link" href="../cv/">Leggi il CV{icon("arrow-up-right", 18)}</a></p></div>
  </section>

  <section class="section stack" aria-labelledby="skill">
    <h2 id="skill" class="h3">Competenze e strumenti</h2>
    <div class="grid grid--2" style="gap:32px;align-items:start">
      <div class="stack" style="--gap:12px"><h3 class="h4">Hard skill</h3>{chips(HARD_SKILLS + ["Design system", "Accessibilità"])}</div>
      <div class="stack" style="--gap:12px"><h3 class="h4">Strumenti</h3>{chips(STRUMENTI)}</div>
      <div class="stack" style="--gap:12px"><h3 class="h4">Soft skill</h3>{chips(SOFT_SKILLS)}</div>
      <div class="stack" style="--gap:12px"><h3 class="h4">Lingue</h3>{timeline(LINGUE)}</div>
    </div>
  </section>

</div>"""
    glows = [("blue", "-14%", "-240px", "62vw", "620px", .42), ("lavender", "55%", "-120px", "56vw", "560px", .32), ("blue", "50%", "1800px", "50vw", "600px", .16)]
    return layout("chi-sono/", 1, "Chi sono", "Chi è Sebastiano Bosi, UX/UI Designer a Milano: percorso, esperienza, formazione e competenze.", body, glows)

def contatti():
    body = f"""
<div class="wrap wrap--fill">
  <div class="split split--contacts" style="padding-block:clamp(64px,8vw,120px) 0">
    <section class="stack intro" style="--gap:clamp(20px,2vw,28px)" aria-labelledby="titolo">
      <div class="about__portrait"><img src="../assets/img/ritratto.webp" alt="Ritratto di Sebastiano Bosi" width="960" height="1200"></div>
      <h1 id="titolo" class="display">Scrivimi.</h1>
      <p class="lead">Che si tratti di un progetto o di una domanda sul mio lavoro, rispondo volentieri. Di solito entro due giorni lavorativi. Sono a Milano.</p>
    </section>

    <section aria-label="Contatti diretti">
      <ul class="contacts contacts--large">
        <li class="contact glass">
          <span class="contact__text"><a class="contact__value" href="mailto:{CONFIG['email']}">{CONFIG['email']}</a><span class="label-s">Email · la via più rapida</span></span>
          <button class="btn btn--secondary contact__action" type="button" data-copy="{CONFIG['email']}">Copia</button>
        </li>
        <li class="contact glass">
          <span class="contact__text"><a class="contact__value" href="{CONFIG['linkedin']}" rel="me noopener" target="_blank">LinkedIn</a><span class="label-s">Il mio profilo e il percorso</span></span>
        </li>
        <li class="contact glass">
          <span class="contact__text"><a class="contact__value" href="../cv/">CV</a><span class="label-s">Esperienza, formazione e competenze</span></span>
        </li>
      </ul>
      <p class="visually-hidden" aria-live="polite" data-copy-status></p>
    </section>
  </div>
</div>"""
    glows = [("blue", "-14%", "-240px", "62vw", "620px", .42), ("lavender", "55%", "-120px", "56vw", "560px", .3), ("warm", "62%", "500px", "30vw", "320px", .18)]
    return layout("contatti/", 1, "Contatti", "Contatta Sebastiano Bosi per un progetto o una collaborazione: email, LinkedIn e curriculum.", body, glows)

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

# ---------------------------------------------------------------------------
# Dati per recruiter e agenti AI: JSON-LD, CV in testo, llms.txt
# ---------------------------------------------------------------------------
import json

PROGETTI_TESTO = {
    "lavori/uci-cinemas/": "Redesign dell’app UCI Cinemas: nuova brand identity, app completa con assistente AI per scegliere film e posti, design system in due temi, accessibilità e video in motion design.",
    "lavori/jet-hr/": "Redesign dell’area dipendente di Jet HR, su desktop e mobile: discovery sulle domande dei dipendenti, una busta paga che si capisce, design system condiviso e piano di usability test.",
    "lavori/idealista/": "Rebranding evolutivo di idealista e nuova app: logo, colore, tipografia, icone, flussi completi dalla ricerca alla pubblicazione, design system con modalità scura e video del brand.",
}

def person_ld():
    site = CONFIG["site_url"]
    return {
        "@type": "Person", "@id": site + "/#persona", "name": CONFIG["name"], "givenName": "Sebastiano", "familyName": "Bosi",
        "jobTitle": "UX/UI Designer", "description": BIO, "url": site + "/", "image": site + "/assets/img/ritratto.webp",
        "email": "mailto:" + CONFIG["email"], "sameAs": [CONFIG["linkedin"]],
        "address": {"@type": "PostalAddress", "addressLocality": "Milano", "addressRegion": "Lombardia", "addressCountry": "IT"},
        "worksFor": {"@type": "Organization", "name": "Collecto"},
        "hasOccupation": {"@type": "Occupation", "name": "UX/UI Designer", "occupationLocation": {"@type": "City", "name": "Milano"},
                          "skills": ", ".join(HARD_SKILLS + STRUMENTI)},
        "alumniOf": [{"@type": "EducationalOrganization", "name": b} for _, b, _ in FORMAZIONE],
        "knowsAbout": KNOWS_ABOUT,
        "knowsLanguage": [{"@type": "Language", "name": "Italiano", "alternateName": "it"}, {"@type": "Language", "name": "Inglese", "alternateName": "en"}],
    }

def structured_data(page, title, description):
    if page == "404":
        return ""
    site = CONFIG["site_url"]
    url = site + ("/en/" if LANG == "en" else "/") + page
    graph = [person_ld(), {"@type": "WebSite", "@id": site + "/#sito", "url": site + "/", "name": CONFIG["name"] + " — Portfolio",
                           "inLanguage": "it-IT", "author": {"@id": site + "/#persona"}}]
    proj = next((p for p in PROJECTS if p["slug"] == page), None)
    if page in ("chi-sono/", "cv/"):
        graph.append({"@type": "ProfilePage", "@id": url, "url": url, "name": title, "description": description,
                      "inLanguage": "it-IT", "mainEntity": {"@id": site + "/#persona"}, "isPartOf": {"@id": site + "/#sito"}})
    elif proj:
        graph.append({"@type": "CreativeWork", "@id": url, "url": url, "name": proj["title"] + " — case study",
                      "headline": proj["desc"], "description": PROGETTI_TESTO[page], "image": site + "/" + proj["img"],
                      "inLanguage": "it-IT", "author": {"@id": site + "/#persona"},
                      "creator": {"@id": site + "/#persona"}, "genre": "Case study UX/UI", "isPartOf": {"@id": site + "/#sito"}})
    else:
        graph.append({"@type": "WebPage", "@id": url, "url": url, "name": title, "description": description,
                      "inLanguage": "it-IT", "about": {"@id": site + "/#persona"}, "isPartOf": {"@id": site + "/#sito"}})
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return '<script type="application/ld+json">' + data.replace("</", "<\\/") + "</script>"

def cv_page():
    r = "../"
    def esp(items, dettagli=None):
        out = ""
        for a, b, c in items:
            d = (dettagli or {}).get(a, "")
            out += f'<li class="cv-item"><div><h3 class="cv-item__title">{a}</h3><p class="label">{b}</p>{f"<p class=muted>{d}</p>" if d else ""}</div><p class="label">{c}</p></li>'
        return f'<ul class="cv-list">{out}</ul>'
    progetti = "".join(
        f'<li class="cv-item"><div><h3 class="cv-item__title"><a href="{r}{p["slug"]}">{p["title"]}</a></h3><p class="label">{p["kind"]}</p><p class="muted">{PROGETTI_TESTO[p["slug"]]}</p></div></li>'
        for p in PROJECTS)
    body = f"""
<div class="wrap">
  <article class="cv" style="padding-top:clamp(64px,8vw,120px)" aria-labelledby="titolo">
    <header class="stack" style="--gap:16px">
      <h1 id="titolo" class="display">{CONFIG['name']}</h1>
      <p class="h4">Curriculum vitae · UX/UI Designer · Milano, Italia</p>
      <p class="muted">Email: <a href="mailto:{CONFIG['email']}">{CONFIG['email']}</a> · LinkedIn: <a href="{CONFIG['linkedin']}" rel="me noopener" target="_blank">sebastiano-bosi</a> · Portfolio: <a href="{r}">sebastianobosi.github.io</a></p>
      <div class="actions actions--stack-mobile">
        <a class="btn btn--primary" href="{r}{CONFIG['cv_ats']}" download>Scarica il PDF</a>
      </div>
    </header>
    <section class="section stack" style="--gap:12px" aria-labelledby="profilo"><h2 id="profilo" class="h3">Profilo</h2><p class="lead">{BIO}</p></section>
    <section class="section stack" style="--gap:12px" aria-labelledby="esperienza"><h2 id="esperienza" class="h3">Esperienza</h2>{esp(ESPERIENZA, DETTAGLI)}</section>
    <section class="section stack" style="--gap:12px" aria-labelledby="progetti"><h2 id="progetti" class="h3">Progetti (case study)</h2><ul class="cv-list">{progetti}</ul></section>
    <section class="section stack" style="--gap:12px" aria-labelledby="formazione"><h2 id="formazione" class="h3">Formazione</h2>{esp(FORMAZIONE)}</section>
    <section class="section stack" style="--gap:16px" aria-labelledby="competenze"><h2 id="competenze" class="h3">Competenze</h2>
      <p><strong>Hard skill:</strong> {", ".join(HARD_SKILLS + ["Design system", "Accessibilità WCAG 2.2", "Architettura dell’informazione", "User flow", "Brand identity", "Motion design", "Newsletter e landing page", "Customer journey", "Marketing automation"])}</p>
      <p><strong>Strumenti:</strong> {", ".join(STRUMENTI)}</p>
      <p><strong>Soft skill:</strong> {", ".join(SOFT_SKILLS)}</p>
      <p><strong>Lingue:</strong> {", ".join(f"{a} ({b.lower()})" for a, b, _ in LINGUE)}</p>
    </section>
  </article>
</div>"""
    glows = [("blue", "-14%", "-240px", "62vw", "620px", .36), ("lavender", "55%", "-120px", "56vw", "560px", .26)]
    return layout("cv/", 1, "CV", "CV di Sebastiano Bosi, UX/UI Designer a Milano: esperienza in Collecto tra UX/UI, product design e marketing automation, Master UX/UI Design Start2Impact, competenze, strumenti e case study.", body, glows)

def llms_txt():
    site = CONFIG["site_url"]
    righe = [f"# {CONFIG['name']} — UX/UI Designer", "",
             f"> Portfolio di {CONFIG['name']}, UX/UI Designer a Milano (Italia). In Collecto app da luglio 2025 (stage, poi tempo pieno da gennaio 2026), tra UX/UI design, product design, comunicazione visiva e marketing automation con CleverTap. Si occupa di discovery, user research, user flow, wireframe, prototipi, design system e accessibilità WCAG 2.2, in Figma.", "",
             "## Profilo", "", BIO, "",
             "## Esperienza", ""]
    righe += [f"- {a}, {b} ({c or 'freelance'}): {DETTAGLI.get(a, '')}".rstrip(": ") for a, b, c in ESPERIENZA]
    righe += ["", "## Formazione", ""] + [f"- {a}, {b} ({c})" for a, b, c in FORMAZIONE]
    righe += ["", "## Competenze", "", "- Hard skill: " + ", ".join(HARD_SKILLS), "- Strumenti: " + ", ".join(STRUMENTI),
              "- Ambiti: " + ", ".join(KNOWS_ABOUT), "- Soft skill: " + ", ".join(SOFT_SKILLS),
              "- Lingue: " + ", ".join(f"{a} ({b.lower()})" for a, b, _ in LINGUE), ""]
    righe += ["## Contatti", "", f"- Email: {CONFIG['email']}", f"- LinkedIn: {CONFIG['linkedin']}", ""]
    righe += ["## Case study", ""] + [f"- [{p['title']}]({site}/{p['slug']}): {PROGETTI_TESTO[p['slug']]}" for p in PROJECTS]
    righe += ["", "## Pagine", "", f"- [Chi sono]({site}/chi-sono/): percorso, metodo, competenze", f"- [CV]({site}/cv/): curriculum completo in HTML",
              f"- [CV in PDF]({site}/{CONFIG['cv_ats']}): versione solo testo, leggibile dagli ATS", f"- [Contatti]({site}/contatti/)", ""]
    return "\n".join(righe)

def note_legali():
    body = f"""
<div class="wrap">
  <article class="cv legal" style="padding-top:clamp(64px,8vw,120px)" aria-labelledby="titolo">
    <header class="stack" style="--gap:16px">
      <h1 id="titolo" class="display">Note legali</h1>
      <p class="lead">I contenuti di questo sito sono opera originale di {CONFIG['name']}. Puoi guardarli, condividerne il link e citarli indicando l’autore. Per tutto il resto serve il mio permesso scritto.</p>
    </header>
    <section class="section stack" style="--gap:12px" aria-labelledby="dir">
      <h2 id="dir" class="h3">Diritto d’autore</h2>
      <p>Testi, case study, tavole, schermate, illustrazioni, icone, loghi riprogettati, fotografie, video e codice del sito sono protetti dalla legge italiana sul diritto d’autore (Legge 22 aprile 1941, n. 633) e dalle norme europee e internazionali applicabili. Il diritto nasce con la creazione dell’opera e non richiede registrazione.</p>
      <p>Sono vietati, senza autorizzazione scritta, la riproduzione anche parziale, la modifica, la distribuzione e l’uso commerciale dei contenuti, compreso il loro utilizzo come base per prodotti, servizi, campagne o progetti di terzi. Resta sempre riconosciuto il diritto morale dell’autore a essere indicato come tale.</p>
    </section>
    <section class="section stack" style="--gap:12px" aria-labelledby="tdm">
      <h2 id="tdm" class="h3">Estrazione di testo e dati</h2>
      <p>L’autore si riserva espressamente l’estrazione di testo e di dati (text and data mining) dai contenuti del sito, ai sensi dell’art. 70-quater della Legge 633/1941 e dell’art. 4 della Direttiva (UE) 2019/790. Questo include l’uso dei contenuti per addestrare sistemi di intelligenza artificiale. La riserva è indicata anche in forma leggibile dalle macchine. La consultazione delle pagine per valutare una candidatura resta naturalmente consentita.</p>
    </section>
    <section class="section stack" style="--gap:12px" aria-labelledby="marchi">
      <h2 id="marchi" class="h3">Marchi di terzi</h2>
      <p>I case study su UCI Cinemas, Jet HR e idealista sono concept personali, non commissionati né approvati dalle rispettive aziende. Nomi e marchi appartengono ai legittimi titolari e sono citati solo per identificare i prodotti di riferimento. La tutela dell’autore riguarda il lavoro originale: ricerca, flussi, interfacce, sistemi grafici, testi e video.</p>
    </section>
    <section class="section stack" style="--gap:12px" aria-labelledby="sel">
      <h2 id="sel" class="h3">Selezioni e prove di lavoro</h2>
      <p>I materiali condivisi durante una selezione, comprese eventuali prove o esercitazioni, restano di proprietà dell’autore e possono essere usati solo per valutare la candidatura, salvo diverso accordo scritto.</p>
    </section>
    <section class="section stack" style="--gap:12px" aria-labelledby="perm">
      <h2 id="perm" class="h3">Richieste di utilizzo</h2>
      <p>Per usare un contenuto scrivi a <a href="mailto:{CONFIG['email']}">{CONFIG['email']}</a>.</p>
    </section>
  </article>
</div>"""
    glows = [("blue", "-14%", "-240px", "62vw", "620px", .3), ("lavender", "55%", "-120px", "56vw", "560px", .2)]
    return layout("note-legali/", 1, "Note legali", "Note legali del portfolio di Sebastiano Bosi: diritto d’autore, riserva sull’estrazione di testo e dati, marchi di terzi.", body, glows)

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="18" fill="#07080f"/><circle cx="20" cy="18" r="22" fill="#1e4fd8" opacity=".55"/><circle cx="48" cy="50" r="20" fill="#9d7bea" opacity=".45"/><text x="32" y="41" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="24" fill="#f2f3f7">SB</text></svg>"""

PAGES = [("index.html", ""), ("lavori/index.html", "lavori/"), ("lavori/uci-cinemas/index.html", "lavori/uci-cinemas/"),
         ("lavori/jet-hr/index.html", "lavori/jet-hr/"), ("lavori/idealista/index.html", "lavori/idealista/"),
         ("chi-sono/index.html", "chi-sono/"), ("cv/index.html", "cv/"), ("contatti/index.html", "contatti/"),
         ("note-legali/index.html", "note-legali/")]
BUILDERS = {"index.html": lambda: home(), "lavori/index.html": lambda: lavori(), "lavori/uci-cinemas/index.html": lambda: uci(),
            "lavori/jet-hr/index.html": lambda: jethr(), "lavori/idealista/index.html": lambda: idealista(),
            "chi-sono/index.html": lambda: chi_sono(), "cv/index.html": lambda: cv_page(), "contatti/index.html": lambda: contatti(),
            "note-legali/index.html": lambda: note_legali()}

def main(out):
    global LANG
    src = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs(out, exist_ok=True)
    def write(path, content):
        p = os.path.join(out, path); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(content)
    # italiano, alla radice
    LANG = "it"
    for path, _ in PAGES:
        write(path, BUILDERS[path]())
    write("404.html", not_found())
    # inglese, in en/: stesse pagine, testi dal dizionario tools/i18n/en.json
    LANG = "en"
    tr = i18n.Translator()
    for path, _ in PAGES:
        write("en/" + path, i18n.relocate(tr.page(BUILDERS[path]())))
    LANG = "it"
    missing = tr.save_missing()
    if os.path.abspath(out) != src:
        for d in ("assets/css", "assets/js"):
            shutil.copytree(os.path.join(src, d), os.path.join(out, d), dirs_exist_ok=True)
    os.makedirs(os.path.join(out, "assets/img"), exist_ok=True)
    open(os.path.join(out, "assets/img/favicon.svg"), "w").write(FAVICON)
    open(os.path.join(out, ".nojekyll"), "w").write("")
    urls = [u for _, u in PAGES]
    open(os.path.join(out, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{CONFIG['site_url']}/{u}</loc></url>\n  <url><loc>{CONFIG['site_url']}/en/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    open(os.path.join(out, "llms.txt"), "w", encoding="utf-8").write(llms_txt())
    open(os.path.join(out, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {CONFIG['site_url']}/sitemap.xml\n")
    print("Pagine generate:", len(PAGES), "in italiano, 1 pagina 404,", len(PAGES), "in inglese (en/)")
    if missing:
        print(f"Attenzione: {missing} testi senza traduzione inglese, elencati in tools/i18n/en.missing.json")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
