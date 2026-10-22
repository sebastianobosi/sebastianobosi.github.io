# Portfolio di Sebastiano Bosi

Sito pubblicato su **https://sebastianobosi.github.io** con GitHub Pages. HTML, CSS e JavaScript senza dipendenze: non serve installare nulla.

## Come modificare

| Cosa | Dove |
|---|---|
| Colori, caratteri, spaziature | `assets/css/style.css`, blocco `:root` in cima (sono i token del file Figma «Notturno») |
| Testi delle pagine | `tools/build.py`, nelle funzioni `home()`, `lavori()`, `uci()`, `jethr()`, `chi_sono()`, `contatti()` |
| Email, LinkedIn, CV | `tools/build.py`, blocco `CONFIG` in cima |
| Menu, filtri, copia dell’email | `assets/js/main.js` |

Dopo aver modificato `tools/build.py`, rigenera le pagine:

```
python3 tools/build.py
```

Un piccolo testo puoi cambiarlo anche direttamente nel file `.html` della pagina, ma alla prossima rigenerazione verrebbe sovrascritto: meglio cambiarlo in `tools/build.py`.

## Immagini e video

Le immagini stanno in `assets/img/` (WebP). Il case study UCI usa:
- schermate dell’app (390 px di larghezza, esportate da Figma): `uci-home.webp`, `uci-posti.webp`, `uci-biglietto.webp`, `uci-bar.webp`, `iris-benvenuto.webp`, `iris-proposte.webp`, `iris-riepilogo.webp`
- `uci-cover.webp` (card del progetto e copertina del video), `uci-mappa-flussi.webp`, `uci-design-system.webp`
- `brand/`: logo, Iris e le sei ucicons in SVG
- `og.png` (anteprima quando condividi il link)

Il film del progetto è `assets/video/uci-cinemas-brand-film.mp4` (1080p, 60 fps, senza audio). Si carica solo quando lo avvii. Per sostituirlo, carica un nuovo file con lo stesso nome.

Il case study idealista usa le immagini `idealista-*.webp` (stesse dimensioni), il video del brand `assets/video/idealista-brand-video.mp4` (1080p, 60 fps, senza audio, poster `idealista-video-poster.webp`), il logo `brand/idealista-logo.svg` (esportato dal file Figma del brand).

Il case study Jet HR usa le immagini `jethr-*.webp` (schermate esportate da Figma a 2x e ridotte: telefoni 780 px, desktop 1800 px, copertina 1600 px).

Ritratto: `ritratto.webp` (4:5, pagina Chi sono) e `ritratto-avatar.webp` (tondo in home). CV: `assets/sebastiano-bosi-cv.pdf`; per aggiornarlo carica un nuovo PDF con lo stesso nome.

Bio, esperienza, formazione, competenze e lingue (presi dal CV) stanno in `tools/build.py`, nelle liste `BIO`, `ESPERIENZA`, `FORMAZIONE`, `HARD_SKILLS`, `STRUMENTI`, `SOFT_SKILLS`, `LINGUE`.

Per un’immagine nuova usa `phone("Etichetta", "percorso.webp")` o `media("Etichetta", classe, "percorso.webp", "descrizione")` in `tools/build.py` e rigenera.

## Recruiter e selezione automatica

Il sito è pensato anche per i software di selezione (ATS) e gli agenti AI che leggono i portfolio:
- ogni pagina ha dati strutturati schema.org (`Person`, `ProfilePage`, `CreativeWork`) generati da `structured_data()` in `tools/build.py`;
- `cv/` è il curriculum in HTML semplice, a una colonna;
- `llms.txt` riassume profilo, esperienza, competenze e case study in Markdown per gli agenti AI;
- `assets/sebastiano-bosi-cv-ats.pdf` è il CV solo testo da caricare nei portali di lavoro. Si rigenera con `python3 tools/cv_ats.py` (serve `pip install reportlab`).

Tutti questi file prendono i dati dalle liste in cima a `tools/build.py`: aggiorna lì e rigenera entrambi gli script.

## Contatti

La pagina Contatti mostra solo contatti diretti: email (con pulsante «Copia»), LinkedIn e CV. Non c'è un modulo da gestire. Per cambiarli modifica `CONFIG` in `tools/build.py` e rigenera.

## Pubblicazione

GitHub Pages pubblica il ramo `main` dalla cartella principale (Settings → Pages → Deploy from a branch → `main` / `root`). Ogni modifica caricata su `main` va online in un paio di minuti.

Design: file Figma «Portfolio» (stile Notturno).
