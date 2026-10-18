# Portfolio di Sebastiano Bosi

Sito pubblicato su **https://sebastianobosi.github.io** con GitHub Pages. HTML, CSS e JavaScript senza dipendenze: non serve installare nulla.

## Come modificare

| Cosa | Dove |
|---|---|
| Colori, caratteri, spaziature | `assets/css/style.css`, blocco `:root` in cima (sono i token del file Figma «Notturno») |
| Testi delle pagine | `tools/build.py`, nelle funzioni `home()`, `lavori()`, `uci()`, `chi_sono()`, `contatti()` |
| Email, LinkedIn, CV, modulo | `tools/build.py`, blocco `CONFIG` in cima |
| Menu, filtri, modulo contatti | `assets/js/main.js` |

Dopo aver modificato `tools/build.py`, rigenera le pagine:

```
python3 tools/build.py
```

Un piccolo testo puoi cambiarlo anche direttamente nel file `.html` della pagina, ma alla prossima rigenerazione verrebbe sovrascritto: meglio cambiarlo in `tools/build.py`.

## Immagini

Metti le immagini in `assets/img/` (meglio WebP, larghe al massimo 1600 px) e sostituisci i riquadri segnaposto `<span class="placeholder">…</span>` con `<img src="…" alt="descrizione">`.

File previsti:
- `uci-home.webp`, `uci-iris.webp`, `uci-biglietto.webp`: schermate per i telefoni (390 × 844)
- `iris-benvenuto.webp`, `iris-proposte.webp`, `iris-riepilogo.webp`
- `uci-cover.webp` (card del progetto), `uci-mappa-flussi.webp`, `uci-design-system.webp`
- `ritratto.webp` (4:5), `og.png` (1200 × 630, anteprima quando condividi il link)
- `sebastiano-bosi-cv.pdf` in `assets/`

## Modulo contatti

Finché `form_action` in `CONFIG` contiene `TUO_ID`, il pulsante «Invia messaggio» apre il programma di posta con il messaggio già scritto. Per ricevere i messaggi direttamente: crea un modulo gratuito su formspree.io, copia l'indirizzo (`https://formspree.io/f/...`) in `form_action` e rigenera.

## Pubblicazione

GitHub Pages pubblica il ramo `main` dalla cartella principale (Settings → Pages → Deploy from a branch → `main` / `root`). Ogni modifica caricata su `main` va online in un paio di minuti.

Design: file Figma «Portfolio» (stile Notturno).
