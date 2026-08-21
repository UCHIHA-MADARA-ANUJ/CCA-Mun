#!/usr/bin/env python3
"""
Build the VANGUARD Draft Resolution 1.2 PDF — "the best PDF ever".
- A4, navy+gold UN-style double border on every page
- Embedded VANGUARD bloc logo (roster v2: Barbados in)
- Masthead: distr. block, DRAFT RESOLUTION 1.1, committee + agenda,
  resolution title plate, SPONSORS box (10 bloc members), SIGNATORIES box
- PREAMBULAR PARAGRAPHS (PP1-14) + OPERATIVE PARAGRAPHS (OP1-17)
- Internal custody tags [MX anchor], **[IRAN — lane]** etc. are STRIPPED
  (this is the circulation version)
- Footer + continuation header + light gold VANGUARD watermark

Usage: python3 scripts/build_dr_pdf.py
Output: drafts/VANGUARD_DR1.2.pdf
"""
import html as _html
import os
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, HRFlowable,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DR_PATH = os.path.join(ROOT, "drafts", "VANGUARD_DR1.2.md")
OUT_PATH = os.path.join(ROOT, "drafts", "VANGUARD_DR1.2.pdf")
LOGO_PATH = os.path.join(ROOT, "assets", "vanguard_logo_final.png")
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

NAVY = colors.HexColor("#0B1E3A")
GOLD = colors.HexColor("#C9A227")
LIGHT = colors.HexColor("#E8EEF7")
GRAY = colors.HexColor("#5A5A5A")
DARK = colors.HexColor("#222222")
GOLD_TINT = colors.HexColor("#F9F5E9")

# ---------------------------------------------------------------- fonts
pdfmetrics.registerFont(TTFont("Serif", os.path.join(FONT_DIR, "DejaVuSerif.ttf")))
pdfmetrics.registerFont(TTFont("Serif-Bold", os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Sans", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("Sans-Bold", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-Bold", italic="Serif", boldItalic="Serif-Bold")
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold", italic="Sans", boldItalic="Sans-Bold")

# ---------------------------------------------------------------- parse DR
PP_RE = re.compile(r"\*\*(PP\d+[A-Z]?)\.\*\*(.*?)(?=\n\*\*PP\d+[A-Z]?\.\*\*|\Z)", re.S)
OP_RE = re.compile(r"\*\*(OP\d+[A-Z]?)\.\*\*(.*?)(?=\n\*\*OP\d+[A-Z]?\.\*\*|\Z)", re.S)


def strip_custody(body: str) -> str:
    """Remove trailing internal custody tags like '; **[IRAN — lane]**' or ', [MX anchor]'."""
    body = re.sub(r"\s*-{3,}.*$", "", body)  # drop any trailing section separator
    body = re.sub(r"\s*\*\*\[[^\]]*\]\*\*\s*$", "", body)
    body = re.sub(r"\s*\[[^\]]*\]\s*$", "", body)
    body = re.sub(r"\s*\*+\s*$", "", body)
    return body.strip()


def to_markup(body: str) -> str:
    body = _html.escape(body, quote=False)
    body = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", body)
    body = re.sub(r"\*(.+?)\*", r"<i>\1</i>", body)
    return body


def first_verb_bold(body: str) -> str:
    """Make the leading operative/preamble verb bold (UN style)."""
    m = re.search(r"<i>[^<]*</i>", body)
    if m:
        return body[: m.start()] + "<b>" + m.group(0) + "</b>" + body[m.end():]
    return body


def parse_section(text: str, regex) -> list:
    out = []
    for m in regex.finditer(text):
        label = m.group(1)
        body = " ".join(m.group(2).split())
        body = strip_custody(body)
        body = to_markup(body)
        body = first_verb_bold(body)
        out.append((label, body))
    return out


raw = open(DR_PATH, encoding="utf-8").read()
preamble = raw.split("## PREAMBULAR PARAGRAPHS")[1].split("## OPERATIVE PARAGRAPHS")[0]
operative = raw.split("## OPERATIVE PARAGRAPHS")[1].split("## ANNEX A")[0]
pps = parse_section(preamble, PP_RE)
ops = parse_section(operative, OP_RE)

# ---------------------------------------------------------------- styles
st_body = ParagraphStyle("body", fontName="Serif", fontSize=10.5, leading=14.8,
                         alignment=TA_JUSTIFY, textColor=DARK)
st_pp = ParagraphStyle("pp", parent=st_body, leftIndent=16, firstLineIndent=-16,
                       spaceBefore=3.5, spaceAfter=0)
st_op = ParagraphStyle("op", parent=st_body, leftIndent=16, firstLineIndent=-16,
                       spaceBefore=5.5, spaceAfter=0)
st_center = ParagraphStyle("center", parent=st_body, alignment=TA_CENTER)
st_mast_small = ParagraphStyle("mast_small", fontName="Sans", fontSize=7.5, leading=10,
                               textColor=GRAY)
st_title = ParagraphStyle("title", fontName="Sans-Bold", fontSize=19, leading=23,
                          alignment=TA_CENTER, textColor=NAVY, spaceBefore=2, spaceAfter=0)
st_sub = ParagraphStyle("sub", fontName="Sans", fontSize=8.5, leading=12,
                        alignment=TA_CENTER, textColor=GRAY)
st_comm = ParagraphStyle("comm", fontName="Sans", fontSize=8.5, leading=12.5,
                         alignment=TA_CENTER, textColor=DARK)
st_plate = ParagraphStyle("plate", fontName="Serif-Bold", fontSize=13, leading=17,
                          alignment=TA_CENTER, textColor=NAVY)
st_sponsor_lab = ParagraphStyle("sponsor_lab", fontName="Sans-Bold", fontSize=9.5,
                                leading=13, textColor=NAVY)
st_sponsor_names = ParagraphStyle("sponsor_names", fontName="Sans-Bold", fontSize=9.5,
                                  leading=14, alignment=TA_JUSTIFY, textColor=DARK)
st_sponsor_note = ParagraphStyle("sponsor_note", fontName="Sans", fontSize=7.5,
                                 leading=10.5, textColor=GRAY)
st_marker = ParagraphStyle("marker", fontName="Sans-Bold", fontSize=9.5, leading=13,
                           alignment=TA_CENTER, textColor=NAVY, spaceBefore=8, spaceAfter=6)
st_ga = ParagraphStyle("ga", fontName="Serif-Bold", fontSize=10.5, leading=14,
                       textColor=NAVY, spaceBefore=4, spaceAfter=2)
st_end = ParagraphStyle("end", fontName="Sans-Bold", fontSize=9.5, leading=13,
                        alignment=TA_CENTER, textColor=NAVY)

CW = A4[0] - 112  # content width

# ---------------------------------------------------------------- page furniture
def draw_page(canvas, doc):
    W, H = A4
    canvas.saveState()
    # double border: navy outer + gold inner
    canvas.setStrokeColor(NAVY)
    canvas.setLineWidth(2.2)
    canvas.rect(22, 22, W - 44, H - 44, stroke=1, fill=0)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.9)
    canvas.rect(28, 28, W - 56, H - 56, stroke=1, fill=0)

    pn = canvas.getPageNumber()
    if pn > 1:
        # continuation header
        canvas.setFont("Sans-Bold", 7)
        canvas.setFillColor(NAVY)
        canvas.drawCentredString(
            W / 2, H - 58,
            "DRAFT RESOLUTION 1.2 — \u201cGlobal Framework for Nuclear-Ecological "
            "Monitoring, Response and Remediation\u201d")
        canvas.setStrokeColor(GOLD)
        canvas.setLineWidth(0.7)
        canvas.line(48, H - 62, W - 48, H - 62)
        # watermark
        canvas.saveState()
        canvas.setFillColor(GOLD)
        canvas.setFillAlpha(0.05)
        canvas.translate(W / 2, H / 2)
        canvas.rotate(42)
        canvas.setFont("Sans-Bold", 130)
        canvas.drawCentredString(0, 0, "VANGUARD")
        canvas.restoreState()

    # footer
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.7)
    canvas.line(48, 52, W - 48, 52)
    canvas.setFillColor(NAVY)
    canvas.setFont("Sans", 7)
    canvas.drawString(48, 42, "CCA MUN \u201926 \u00b7 UNGA \u2014 Delegation of Japan \u00b7 VANGUARD Bloc")
    canvas.drawRightString(W - 48, 42, "Draft Resolution 1.2 \u2014 Page %d" % pn)
    canvas.restoreState()


# ---------------------------------------------------------------- story
story = []

# distr row
distr = Table(
    [[Paragraph("Distr.: LIMITED", st_mast_small),
      Paragraph("A/UNGA/2026/DR1.2 &nbsp;\u00b7&nbsp; 20 August 2026", st_mast_small)]],
    colWidths=[CW / 2, CW / 2])
distr.setStyle(TableStyle([
    ("LEFTPADDING", (0, 0), (0, 0), 0),
    ("RIGHTPADDING", (1, 0), (1, 0), 0),
    ("ALIGN", (0, 0), (0, 0), "LEFT"),
    ("ALIGN", (1, 0), (1, 0), "RIGHT"),
]))
story.append(distr)

story.append(Spacer(1, 6))
story.append(Image(LOGO_PATH, width=116, height=116, hAlign="CENTER"))
story.append(Spacer(1, 6))
story.append(Paragraph("DRAFT RESOLUTION 1.2", st_title))
story.append(HRFlowable(width=220, thickness=1.4, color=GOLD, hAlign="CENTER",
                        spaceBefore=3, spaceAfter=5))
story.append(Paragraph("Submitted by the Delegation of Japan &nbsp;\u00b7&nbsp; on behalf of the "
                       "<b>VANGUARD Bloc</b>", st_sub))
story.append(Spacer(1, 2))
story.append(Paragraph("GENERAL ASSEMBLY (UNGA) &nbsp;\u2014&nbsp; Agenda: "
                       "\u201cAssessing the ecological threats of nuclear proliferation "
                       "on global boundaries.\u201d &nbsp;\u00b7&nbsp; 21\u201322 August 2026", st_comm))
story.append(Spacer(1, 8))

# title plate
plate = Table([[Paragraph("\u201cGlobal Framework for Nuclear-Ecological Monitoring, "
                          "Response and Remediation\u201d", st_plate)]], colWidths=[CW])
plate.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
    ("BOX", (0, 0), (-1, -1), 0.9, NAVY),
    ("TOPPADDING", (0, 0), (-1, -1), 9),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
]))
story.append(plate)
story.append(Spacer(1, 7))

# sponsors box
sponsors = Table(
    [[Paragraph("<b>SPONSORS (11)</b> \u2014 the VANGUARD Bloc", st_sponsor_lab)],
     [Paragraph("JAPAN \u00b7 INDIA \u00b7 MEXICO \u00b7 CANADA \u00b7 IRAN \u00b7 SWITZERLAND \u00b7 "
                "EGYPT \u00b7 PHILIPPINES \u00b7 BARBADOS \u00b7 SOUTH AFRICA \u00b7 KAZAKHSTAN", st_sponsor_names)],
     [Paragraph("VANGUARD \u2014 Voluntary Alliance for Nuclear Oversight, Global "
                "Accountability and Remediation Directives", st_sponsor_note)]],
    colWidths=[CW])
sponsors.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.white),
    ("BOX", (0, 0), (-1, -1), 1.3, GOLD),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 9),
    ("RIGHTPADDING", (0, 0), (-1, -1), 9),
]))
story.append(sponsors)
story.append(Spacer(1, 5))

# signatories box
signatories = Table(
    [[Paragraph("<b>SIGNATORIES</b> \u2014 target list, to be confirmed", st_sponsor_lab)],
     [Paragraph("NORWAY \u00b7 GERMANY \u00b7 REPUBLIC OF KOREA \u00b7 SINGAPORE \u00b7 NEW ZEALAND",
                st_sponsor_names)],
     [Paragraph("Delegations wishing to co-sponsor or sign may approach the "
                "Delegation of Japan.", st_sponsor_note)]],
    colWidths=[CW])
signatories.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), GOLD_TINT),
    ("BOX", (0, 0), (-1, -1), 0.9, GOLD),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 9),
    ("RIGHTPADDING", (0, 0), (-1, -1), 9),
]))
story.append(signatories)
story.append(Spacer(1, 10))

# the General Assembly
story.append(Paragraph("The General Assembly,", st_ga))

# preamble marker
story.append(Paragraph('<font color="#C9A227">\u2014</font> &nbsp;<b>PREAMBULAR PARAGRAPHS</b> '
                       '&nbsp;<font color="#C9A227">\u2014</font>', st_marker))
for label, body in pps:
    story.append(Paragraph(f'<b><font color="#0B1E3A">{label}.</font></b>&nbsp; {body}', st_pp))

# operative marker
story.append(Paragraph('<font color="#C9A227">\u2014</font> &nbsp;<b>OPERATIVE PARAGRAPHS</b> '
                       '&nbsp;<font color="#C9A227">\u2014</font>', st_marker))
for label, body in ops:
    story.append(Paragraph(f'<b><font color="#0B1E3A">{label}.</font></b>&nbsp; {body}', st_op))

# end block
story.append(Spacer(1, 12))
story.append(HRFlowable(width="100%", thickness=1.0, color=GOLD))
story.append(Spacer(1, 8))
story.append(Paragraph("\u2014&nbsp; END OF DRAFT RESOLUTION 1.2 &nbsp;\u2014", st_end))
story.append(Spacer(1, 4))
story.append(Paragraph("Submitted by the Delegation of Japan on behalf of the VANGUARD Bloc "
                       "\u00b7 CCA MUN \u201926 \u00b7 21\u201322 August 2026", st_sub))

# ---------------------------------------------------------------- build
doc = SimpleDocTemplate(
    OUT_PATH, pagesize=A4,
    leftMargin=56, rightMargin=56, topMargin=80, bottomMargin=68,
    title="Draft Resolution 1.2 — Global Framework for Nuclear-Ecological Monitoring, "
          "Response and Remediation (VANGUARD Bloc)",
    author="Delegation of Japan — CCA MUN '26 (UNGA)",
    subject="UNGA — Assessing the ecological threats of nuclear proliferation on global boundaries",
)
doc.build(story, onFirstPage=draw_page, onLaterPages=draw_page)
print(f"built {OUT_PATH} ({os.path.getsize(OUT_PATH)} bytes)")
print(f"clauses: {len(pps)} PP, {len(ops)} OP")
