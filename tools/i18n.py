"""Traduzione delle pagine generate.

La versione inglese nasce dall'HTML italiano: ogni testo visibile, testo alternativo, etichetta per gli
screen reader, titolo e descrizione viene cercato nel dizionario tools/i18n/en.json (italiano → inglese).
Un testo che manca nel dizionario resta in italiano e viene elencato in tools/i18n/en.missing.json,
così basta aggiungere la traduzione e rigenerare.
"""
import html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
DICT_PATH = os.path.join(HERE, "i18n", "en.json")
MISSING_PATH = os.path.join(HERE, "i18n", "en.missing.json")

ATTRS = ("alt", "aria-label", "title", "placeholder", "content")
META_CONTENT = re.compile(r'<meta (?:name|property)="(?:description|og:title|og:description|copyright)" content="([^"]*)"')


def load():
    if not os.path.exists(DICT_PATH):
        return {}
    return json.load(open(DICT_PATH, encoding="utf-8"))


def needs_translation(text):
    return bool(re.search(r"[A-Za-zÀ-ÿ]", text))


def norm(text):
    return " ".join(html.unescape(text).split())


class Translator:
    def __init__(self):
        self.table = load()
        self.missing = {}

    def get(self, text):
        key = norm(text)
        if not key or not needs_translation(key):
            return None
        if key in self.table and self.table[key]:
            return self.table[key]
        self.missing.setdefault(key, "")
        return None

    # -- testi tra i tag --------------------------------------------------------------
    def _text(self, m):
        raw = m.group(1)
        tr = self.get(raw)
        if tr is None:
            return m.group(0)
        lead = raw[: len(raw) - len(raw.lstrip())]
        trail = raw[len(raw.rstrip()):]
        return ">" + lead + html.escape(tr, quote=False) + trail + "<"

    # -- attributi ----------------------------------------------------------------------
    def _attr(self, m):
        name, val = m.group(1), m.group(2)
        tr = self.get(val)
        return m.group(0) if tr is None else f'{name}="{html.escape(tr, quote=True)}"'

    def _meta(self, m):
        tr = self.get(m.group(1))
        return m.group(0) if tr is None else m.group(0).replace(f'content="{m.group(1)}"', f'content="{html.escape(tr, quote=True)}"')

    # -- dati strutturati ---------------------------------------------------------------
    def _json(self, node):
        if isinstance(node, dict):
            return {k: (self._json(v) if k not in ("@id", "url", "image", "email", "sameAs", "@type", "@context") else v) for k, v in node.items()}
        if isinstance(node, list):
            return [self._json(v) for v in node]
        if isinstance(node, str):
            if node == "it-IT":
                return "en"
            tr = self.table.get(norm(node))
            return tr or node
        return node

    def _ld(self, m):
        data = json.loads(m.group(1).replace("<\\/", "</"))
        out = json.dumps(self._json(data), ensure_ascii=False)
        return '<script type="application/ld+json">' + out.replace("</", "<\\/") + "</script>"

    def page(self, doc):
        # le parti che non sono testo da leggere restano fuori dalla traduzione
        parts = re.split(r"(<script\b.*?</script>|<style\b.*?</style>)", doc, flags=re.S)
        out = []
        for part in parts:
            if part.startswith('<script type="application/ld+json">'):
                out.append(re.sub(r'<script type="application/ld\+json">(.*)</script>', self._ld, part, flags=re.S))
            elif part.startswith(("<script", "<style")):
                out.append(part)
            else:
                part = META_CONTENT.sub(self._meta, part)
                part = re.sub(r'\b(alt|aria-label|title|placeholder)="([^"]*)"', self._attr, part)
                part = re.sub(r">([^<>]+)<", self._text, part)
                out.append(part)
        return "".join(out)

    def save_missing(self):
        if self.missing:
            json.dump(self.missing, open(MISSING_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        elif os.path.exists(MISSING_PATH):
            os.remove(MISSING_PATH)
        return len(self.missing)


def relocate(doc):
    """Le pagine inglesi stanno un livello più in basso (en/…): i file in assets/ restano alla radice."""
    return re.sub(r'\b(src|href|poster)="((?:\.\./)*)assets/', lambda m: f'{m.group(1)}="../{m.group(2)}assets/', doc)
