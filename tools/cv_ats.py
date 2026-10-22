#!/usr/bin/env python3
"""Genera il CV «solo testo» (ATS) da caricare nei portali di lavoro.

Una colonna, testo vero, niente immagini, icone o pallini: i software di selezione
(ATS) e gli agenti AI lo leggono senza errori. I dati vengono da tools/build.py,
quindi il CV resta allineato al sito.

Uso:  pip install reportlab   (una volta)
      python3 tools/cv_ats.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, B.CONFIG["cv_ats"])
C = B.CONFIG

base = ParagraphStyle("base", fontName="Helvetica", fontSize=9.5, leading=12.4)
nome = ParagraphStyle("nome", parent=base, fontName="Helvetica-Bold", fontSize=20, leading=24)
ruolo = ParagraphStyle("ruolo", parent=base, fontSize=12, leading=16)
h2 = ParagraphStyle("h2", parent=base, fontName="Helvetica-Bold", fontSize=12, leading=16, spaceBefore=10, spaceAfter=3)
voce = ParagraphStyle("voce", parent=base, fontName="Helvetica-Bold", spaceBefore=6)

def p(t, s=base):
    return Paragraph(t, s)

def main():
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=17*mm, rightMargin=17*mm, topMargin=15*mm, bottomMargin=15*mm,
                            title=f"{C['name']} - CV UX/UI Designer", author=C["name"],
                            subject="Curriculum vitae", keywords=", ".join(B.KNOWS_ABOUT))
    s = [p(C["name"], nome), p("UX/UI Designer", ruolo), Spacer(1, 4),
         p(f"Milano, Italia | Email: {C['email']} | LinkedIn: {C['linkedin']} | Portfolio: {C['site_url']}"),
         p("Profilo", h2), p(B.BIO),
         p("Esperienza", h2)]
    for a, b, c in B.ESPERIENZA:
        s.append(p(f"{a} | {b.replace(' · ', ', ')}" + (f" | {c}" if c else ""), voce))
        if a in B.DETTAGLI:
            s.append(p(B.DETTAGLI[a]))
    s.append(p("Progetti (case study)", h2))
    for pr in B.PROJECTS:
        s.append(p(f"{pr['title']} | progetto personale | {C['site_url']}/{pr['slug']}", voce))
        s.append(p(B.PROGETTI_TESTO[pr["slug"]]))
    s.append(p("Formazione", h2))
    for a, b, c in B.FORMAZIONE:
        s.append(p(f"{a} | {b} | {c}", voce))
    s += [p("Competenze", h2),
          p("Hard skill: " + ", ".join(B.HARD_SKILLS + ["Design system", "Accessibilità WCAG 2.2", "Architettura dell’informazione", "User flow", "Brand identity", "Motion design", "Newsletter e landing page", "Customer journey", "Marketing automation"])),
          p("Strumenti: " + ", ".join(B.STRUMENTI + ["Figma Sites"])),
          p("Soft skill: " + ", ".join(B.SOFT_SKILLS)),
          p("Lingue: " + ", ".join(f"{a} ({b.lower()})" for a, b, _ in B.LINGUE)),
          Spacer(1, 10),
          p("Autorizzo il trattamento dei miei dati personali ai sensi del Regolamento UE 2016/679 (GDPR).", ParagraphStyle("gdpr", parent=base, fontSize=8, leading=11))]
    doc.build(s)
    print("CV ATS generato:", OUT)

if __name__ == "__main__":
    main()
