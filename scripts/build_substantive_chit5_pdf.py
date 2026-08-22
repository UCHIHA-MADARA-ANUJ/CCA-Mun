#!/usr/bin/env python3
"""Build the handwritten-ready PDF for Japan's fifth substantive chit: The Three-Key Evidence Standard."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "substantive_chits" / "SUBSTANTIVE_CHIT_5.pdf"

pdfmetrics.registerFont(TTFont("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

PAGE_W, PAGE_H = A4
TOTAL_PAGES = 4
NAVY = colors.HexColor("#0B1F3A")
CRIMSON = colors.HexColor("#BC002D")
GOLD = colors.HexColor("#C6A15B")
INK = colors.HexColor("#1D2633")
MUTED = colors.HexColor("#5E6875")
PAPER = colors.HexColor("#FAF8F3")
MIST = colors.HexColor("#EEF2F5")
PALE_RED = colors.HexColor("#F8E9EC")
PALE_GOLD = colors.HexColor("#F6F0E3")
STEEL = colors.HexColor("#485F75")
WHITE = colors.white

LEFT = 18 * mm
RIGHT = 18 * mm
TOP = 28 * mm
BOTTOM = 18 * mm
CONTENT_W = PAGE_W - LEFT - RIGHT

styles = getSampleStyleSheet()

BODY = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    fontName="DejaVuSans",
    fontSize=9.7,
    leading=12.9,
    textColor=INK,
    alignment=TA_JUSTIFY,
    spaceAfter=5.5,
    allowWidows=0,
    allowOrphans=0,
)
BODY_SMALL = ParagraphStyle(
    "BodySmall",
    parent=BODY,
    fontSize=8.9,
    leading=11.5,
    spaceAfter=4,
)
TITLE = ParagraphStyle(
    "Title",
    parent=styles["Title"],
    fontName="DejaVuSans-Bold",
    fontSize=20,
    leading=22,
    textColor=NAVY,
    alignment=TA_LEFT,
    spaceAfter=5,
)
SUBTITLE = ParagraphStyle(
    "Subtitle",
    parent=BODY,
    fontName="DejaVuSans-Bold",
    fontSize=10.3,
    leading=13,
    textColor=CRIMSON,
    alignment=TA_LEFT,
    spaceAfter=8,
)
KICKER = ParagraphStyle(
    "Kicker",
    parent=BODY,
    fontName="DejaVuSans-Bold",
    fontSize=7.5,
    leading=9,
    textColor=CRIMSON,
    tracking=1.3,
    spaceAfter=4,
)
SECTION = ParagraphStyle(
    "Section",
    parent=BODY,
    fontName="DejaVuSans-Bold",
    fontSize=11.4,
    leading=13,
    textColor=NAVY,
    spaceBefore=5,
    spaceAfter=5,
)
CARD_BODY = ParagraphStyle(
    "CardBody",
    parent=BODY_SMALL,
    fontSize=8.2,
    leading=10.4,
    spaceAfter=0,
)
BULLET = ParagraphStyle(
    "Bullet",
    parent=CARD_BODY,
    leftIndent=9,
    firstLineIndent=-5,
    bulletIndent=0,
    spaceBefore=0,
    spaceAfter=2.4,
)
SOURCE = ParagraphStyle(
    "Source",
    parent=BODY_SMALL,
    fontSize=7.6,
    leading=9.6,
    spaceAfter=1.5,
    alignment=TA_LEFT,
)
SOURCE_LINK = ParagraphStyle(
    "SourceLink",
    parent=SOURCE,
    fontSize=6.6,
    leading=8.0,
    textColor=colors.HexColor("#31577C"),
)
CENTER_SMALL = ParagraphStyle(
    "CenterSmall",
    parent=BODY_SMALL,
    alignment=TA_CENTER,
    fontName="DejaVuSans-Bold",
    fontSize=7.2,
    leading=8.5,
)
META_HEADER = ParagraphStyle(
    "MetaHeader",
    parent=CENTER_SMALL,
    textColor=WHITE,
    fontSize=7.2,
    leading=8.5,
)
FACT_NUMBER = ParagraphStyle(
    "FactNumber",
    parent=CENTER_SMALL,
    fontName="DejaVuSans-Bold",
    fontSize=16,
    leading=17,
    textColor=CRIMSON,
)
FACT_LABEL = ParagraphStyle(
    "FactLabel",
    parent=CENTER_SMALL,
    textColor=NAVY,
)
KEY_TITLE = ParagraphStyle(
    "KeyTitle",
    parent=BODY,
    fontName="DejaVuSans-Bold",
    fontSize=9.6,
    leading=11,
    textColor=WHITE,
    alignment=TA_LEFT,
    spaceAfter=0,
)
QUOTE = ParagraphStyle(
    "Quote",
    parent=BODY,
    fontName="DejaVuSans-Bold",
    fontSize=11,
    leading=14,
    textColor=NAVY,
    alignment=TA_CENTER,
    spaceAfter=0,
)


def draw_wave_motif(canvas, y, color, alpha=0.22):
    canvas.saveState()
    try:
        canvas.setStrokeAlpha(alpha)
    except Exception:
        pass
    canvas.setStrokeColor(color)
    canvas.setLineWidth(0.45)
    radius = 8 * mm
    step = 8 * mm
    x = -radius
    while x < PAGE_W + radius:
        canvas.arc(x, y - radius / 2, x + 2 * radius, y + 1.5 * radius, 0, 180)
        canvas.arc(x + step / 2, y - radius, x + step / 2 + 2 * radius, y + radius, 0, 180)
        x += step
    canvas.restoreState()


def page_decoration(canvas, doc):
    page = canvas.getPageNumber()
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setStrokeColor(NAVY)
    canvas.setLineWidth(1.0)
    canvas.rect(9 * mm, 9 * mm, PAGE_W - 18 * mm, PAGE_H - 18 * mm, fill=0, stroke=1)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.45)
    canvas.rect(11 * mm, 11 * mm, PAGE_W - 22 * mm, PAGE_H - 22 * mm, fill=0, stroke=1)
    canvas.setFillColor(NAVY)
    canvas.rect(9 * mm, PAGE_H - 23 * mm, PAGE_W - 18 * mm, 14 * mm, fill=1, stroke=0)
    canvas.setFillColor(CRIMSON)
    canvas.circle(PAGE_W - 22 * mm, PAGE_H - 16 * mm, 4.4 * mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("DejaVuSans-Bold", 7.3)
    canvas.drawString(16 * mm, PAGE_H - 15.1 * mm, "DELEGATION OF JAPAN")
    canvas.setFont("DejaVuSans", 6.7)
    canvas.drawString(16 * mm, PAGE_H - 19.2 * mm, "UNITED NATIONS GENERAL ASSEMBLY  |  CCA MUN '26")
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.1)
    canvas.line(12 * mm, PAGE_H - 25.3 * mm, PAGE_W - 12 * mm, PAGE_H - 25.3 * mm)
    draw_wave_motif(canvas, 9.4 * mm, NAVY, 0.11)
    canvas.setFillColor(NAVY)
    canvas.setFont("DejaVuSans-Bold", 6.6)
    footer = "SUBSTANTIVE CHIT 05  |  THE THREE-KEY EVIDENCE STANDARD  |  HANDWRITTEN"
    canvas.drawString(16 * mm, 12.7 * mm, footer)
    canvas.drawRightString(PAGE_W - 16 * mm, 12.7 * mm, f"PAGE {page} / {TOTAL_PAGES}")
    canvas.restoreState()


class NumberedDocTemplate(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=LEFT,
            rightMargin=RIGHT,
            topMargin=TOP,
            bottomMargin=BOTTOM,
            title="Substantive Chit 05 — The Three-Key Evidence Standard",
            author="Delegation of Japan",
            subject="CCA MUN '26 UNGA substantive submission",
        )
        frame = Frame(
            LEFT, BOTTOM, CONTENT_W, PAGE_H - TOP - BOTTOM,
            leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="content",
        )
        self.addPageTemplates([PageTemplate(id="japan", frames=[frame], onPage=page_decoration)])


def P(text, style=BODY):
    return Paragraph(text, style)


def thesis_box(text):
    table = Table([[P(text, ParagraphStyle("Thesis", parent=BODY, fontName="DejaVuSans-Bold", fontSize=10.1, leading=13, textColor=NAVY, spaceAfter=0))]], colWidths=[CONTENT_W])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE_GOLD),
        ("BOX", (0, 0), (-1, -1), 0.7, GOLD),
        ("LINEBEFORE", (0, 0), (0, -1), 4.2, CRIMSON),
        ("LEFTPADDING", (0, 0), (-1, -1), 11),
        ("RIGHTPADDING", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return table


def fact_strip():
    facts = [
        ("3", "KEYS BEFORE A FINDING<br/>IS CLOSED"),
        ("23", "LUCKY DRAGON<br/>CREW EXPOSED"),
        ("456", "TESTS AT<br/>SEMIPALATINSK"),
        ("67", "TESTS IN THE<br/>MARSHALL ISLANDS"),
    ]
    cells = []
    for number, label in facts:
        cells.append([P(number, FACT_NUMBER), P(label, FACT_LABEL)])
    table = Table([cells], colWidths=[CONTENT_W / 4] * 4)
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (-1, -1), MIST),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#B9C4CF")),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CCD4DC")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return table


def key_card(number, title, bullets, accent):
    head = Table([[P(f"KEY {number}  |  {title}", KEY_TITLE)]], colWidths=[CONTENT_W])
    head.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), accent),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 5.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5.5),
    ]))
    bullet_flow = [P(f"• {b}", BULLET) for b in bullets]
    body = Table([[bullet_flow]], colWidths=[CONTENT_W])
    body.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
        ("BOX", (0, 0), (-1, -1), 0.55, colors.HexColor("#C6CFD8")),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return KeepTogether([head, body, Spacer(1, 5)])


def numbered_recommendation(number, text):
    num = P(str(number), ParagraphStyle("RecNum", parent=FACT_NUMBER, textColor=WHITE, fontSize=11, leading=12))
    body = P(text, CARD_BODY)
    t = Table([[num, body]], colWidths=[10 * mm, CONTENT_W - 10 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), CRIMSON),
        ("BACKGROUND", (1, 0), (1, 0), PALE_RED),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D6B8C0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def source_row(number, title, claim, url):
    num = P(f"[{number}]", ParagraphStyle("SourceNum", parent=SOURCE, fontName="DejaVuSans-Bold", fontSize=8.2, textColor=CRIMSON))
    detail = P(f"<b>{title}</b><br/>{claim}", SOURCE)
    link = P(f'<link href="{url}" color="#31577C"><u>{url}</u></link>', SOURCE_LINK)
    return [num, detail, link]


def build_story():
    story = []

    def source_table(rows):
        t = Table(rows, colWidths=[13 * mm, 70 * mm, CONTENT_W - 83 * mm])
        t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, MIST]),
            ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#B9C4CF")),
            ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D1D7DD")),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        return t

    def metadata():
        t = Table([
            [P("DELEGATION", META_HEADER), P("COMMITTEE", META_HEADER), P("MODERATED-CAUCUS FOCUS", META_HEADER)],
            [P("JAPAN", ParagraphStyle("C5M1", parent=FACT_LABEL, fontSize=9.2)),
             P("UN GENERAL ASSEMBLY", ParagraphStyle("C5M2", parent=FACT_LABEL, fontSize=9.2)),
             P("SOURCE-STATE EVIDENCE AUTHORITY OVER TRANSBOUNDARY LEGACY CONTAMINATION", ParagraphStyle("C5M3", parent=FACT_LABEL, fontSize=7.7))],
        ], colWidths=[CONTENT_W * 0.18, CONTENT_W * 0.28, CONTENT_W * 0.54])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("BACKGROUND", (0, 1), (-1, 1), WHITE),
            ("BOX", (0, 0), (-1, -1), 0.6, NAVY),
            ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C8D0D8")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        return t

    # PAGE 1 — exact handwritten submission, part I.
    story += [
        P("SUBSTANTIVE CHIT 05  /  HANDWRITTEN SUBMISSION  /  COPY PART I", KICKER),
        P("THE THREE-KEY EVIDENCE STANDARD", TITLE),
        P("Who decides whether contamination exists?", SUBTITLE),
        metadata(), Spacer(1, 7),
        thesis_box("<font color='#BC002D'>COPY PAGES 1–2 AS THE SUBMISSION.</font><br/>The State that created the risk cannot remain the witness, laboratory and final judge."),
        Spacer(1, 8),
        P("EXACT HANDWRITTEN TEXT  |  PART I", SECTION),
        P("Who decides whether contamination exists? Today, too often, the answer is one State: the State that created the risk. It controls the records, selects the model, calculates the dose and publishes the conclusion — then asks affected communities to disprove it without the evidence. <b>The State that created the risk cannot remain the witness, laboratory and final judge.</b>"),
        P("Japan proposes the <b>Three-Key Evidence Standard</b>. Three independent keys must turn before an ecological threat is declared absent, contained or resolved."),
        P("KEY ONE — SOURCE RECORD PACKAGE", SECTION),
        P("The source State preserves and releases non-sensitive records: test dates and locations, release estimates, plume data, environmental sampling results and monitoring history, with chain-of-custody notes. Security-sensitive material is protected; the ecological record is not."),
        P("CONTINUE DIRECTLY TO PAGE 2  →", ParagraphStyle("Continue", parent=KICKER, alignment=TA_CENTER, fontSize=8.2)),
        PageBreak(),
    ]

    # PAGE 2 — exact handwritten submission, part II.
    story += [
        P("SUBSTANTIVE CHIT 05  /  HANDWRITTEN SUBMISSION  /  COPY PART II", KICKER),
        P("THE THREE-KEY EVIDENCE STANDARD  /  CONTINUED", TITLE),
        P("Exact handwritten text • continue without adding a second heading", SUBTITLE),
        P("KEY TWO — AFFECTED-STATE COUNTER-ASSESSMENT", SECTION),
        P("Affected States may conduct or commission independent environmental sampling, receive the underlying data and technical support, and submit a counter-assessment on equal footing. <b>A claim cannot be disproved with evidence that the claimant controls.</b>"),
        P("KEY THREE — PROTECTED INDEPENDENT REVIEW", SECTION),
        P("A protected technical review, using information barriers and managed access, examines whether conclusions are supported by the evidence. No unannounced inspections. No weapon designs. No operational locations. No readiness information. No automatic liability."),
        P("EVIDENCE DISCIPLINE", SECTION),
        P("Every finding is labelled: <b>measured data</b>, <b>modelled estimate</b> or <b>unresolved uncertainty</b>. Every dataset carries sampling location and date, detection limits, chain of custody, model assumptions, confidence range and version history. Labels, not adjectives, decide what the world may rely on."),
        Spacer(1, 6),
        thesis_box("<font color='#BC002D'>CLASSIFICATION CAN PROTECT A SECRET.<br/>IT CANNOT MANUFACTURE INNOCENCE.</font>"),
        Spacer(1, 8),
        P("HANDWRITING CHECKLIST", SECTION),
    ]
    checklist = [
        "Write the inline source numbers [1]–[9] where shown.",
        "Keep the three keys in order; do not merge Key Two and Key Three.",
        "Keep the final bold line as the final sentence.",
        "If space is short, shorten the Marshall Islands example — never shorten the three keys.",
    ]
    check_table = Table([[P("• " + x, CARD_BODY)] for x in checklist], colWidths=[CONTENT_W])
    check_table.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, MIST]),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#BBC5CF")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story += [check_table, Spacer(1, 8), P("END OF TEXT TO HANDWRITE", ParagraphStyle("EndCopy", parent=KICKER, alignment=TA_CENTER, fontSize=8.3)), PageBreak()]

    # PAGE 3 — supporting architecture, not mandatory to copy.
    story += [
        P("RESEARCH SUPPORT  /  DO NOT COPY UNLESS SPACE PERMITS", KICKER),
        P("THE EVIDENTIARY MONOPOLY, EXPOSED", TITLE),
        P("Six shifts the Three-Key Standard demands", SUBTITLE),
        P("THE SHIFT TABLE", SECTION),
    ]
    shift_rows = [
        ("Element", "Today", "Under the Standard"),
        ("Records", "Held exclusively by the source State", "Source Record Package with chain of custody"),
        ("Data access", "Discretionary", "Affected-State access to non-sensitive data"),
        ("Modelling", "Source selects the model", "Assumptions and confidence ranges disclosed"),
        ("Dose conclusion", "Source publishes alone", "Counter-assessment on equal footing"),
        ("Dispute resolution", "Self-assessment", "Protected independent review"),
        ("Burden", "Affected State must disprove", "Evidence must carry its own label"),
    ]
    shift_cells = [[P(c, ParagraphStyle(f"SH{0}_{i}", parent=CARD_BODY, fontName="DejaVuSans-Bold" if i == 0 else "DejaVuSans")) for i, c in enumerate(row)] for row in shift_rows]
    shift_table = Table(shift_cells, colWidths=[CONTENT_W * 0.22, CONTENT_W * 0.39, CONTENT_W * 0.39])
    shift_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, MIST]),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#B9C4CF")),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D1D7DD")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    proof_rows = [
        ("01  |  SOURCE RECORD PACKAGE", "ALREADY PRACTISED IN PART", "IAEA cooperation with Kazakhstan on the Semipalatinsk site relied on preserved records and technical assessments; release of non-sensitive ecological data is the minimum, while security-sensitive material stays protected."),
        ("02  |  AFFECTED-STATE COUNTER-ASSESSMENT", "A RIGHT IN OTHER FIELDS", "International environmental practice gives affected States access to information and participation in assessment; the Standard applies the same logic to nuclear legacies with technical support from existing institutions."),
        ("03  |  PROTECTED INDEPENDENT REVIEW", "ALREADY PROVEN TECHNICALLY", "The UK–Norway Initiative demonstrated managed access and information barriers for verification without exposing secrets; if barriers can protect warhead attributes, they can protect environmental records."),
    ]
    proof_cells = []
    for num_title, tag, body in proof_rows:
        proof_cells.append([
            P(f"<b><font color='#0B1F3A'>{num_title}</font></b><br/><font size='7' color='#BC002D'>{tag}</font>", CARD_BODY),
            P(body, CARD_BODY),
        ])
    proof_table = Table(proof_cells, colWidths=[CONTENT_W * 0.36, CONTENT_W * 0.64])
    proof_table.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, MIST]),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#B9C4CF")),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D1D7DD")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story += [shift_table, Spacer(1, 9), P("WHY EACH KEY IS ACHIEVABLE", SECTION),
              proof_table, Spacer(1, 9),
              P("DRAFT-READY LANGUAGE", SECTION),
              ]
    recs = [
        "<b>Invites</b> source States to publish, on a voluntary basis, a non-sensitive environmental record package for nuclear-testing and weapons-production legacies;",
        "<b>Encourages</b> affected States to conduct independent sampling and counter-assessment with technical support from existing institutions;",
        "<b>Recommends</b> protected independent review of contested findings, using information barriers and managed access;",
        "<b>Calls upon</b> all States to label findings as measured, modelled or unresolved, with the data fields set out above;",
        "<b>Decides</b> to remain seized of the matter.",
    ]
    for i, x in enumerate(recs, 1):
        story += [numbered_recommendation(i, x), Spacer(1, 5)]
    story += [Spacer(1, 4), P("SECURITY AND LEGAL SAFEGUARDS", SECTION),
              thesis_box("The Standard requires no disclosure of weapon designs, locations, readiness or doctrine; creates no new inspection powers; establishes no liability; and does not prejudice any State's position on the legality of nuclear weapons."),
              PageBreak()]

    # PAGE 4 — sources and precision.
    story += [
        P("EVIDENCE LEDGER", KICKER),
        P("SOURCES + PRECISION DECLARATIONS", TITLE),
        P("Nine official or high-quality records supporting the handwritten submission", SUBTITLE),
    ]
    sources = [
        source_row(1, "Hiroshima Peace Memorial Museum — Lucky Dragon", "The Daigo Fukuryu Maru operated outside the declared United States danger area; all 23 crew members were exposed to radioactive fallout.", "https://hpmmuseum.jp/virtual/VirtualMuseum_e/exhibit_e/exh0307_e/exh03078_e.html"),
        source_row(2, "CTBTO — World overview of nuclear testing", "456 tests conducted at the Semipalatinsk test site between 1949 and 1989.", "https://www.ctbto.org/nuclear-testing/history-of-nuclear-testing/world-overview/"),
        source_row(3, "IAEA — Semipalatinsk testing-site environmental impact", "Technical cooperation and remediation assessment for the Semipalatinsk legacy.", "https://www-pub.iaea.org/MTCD/Publications/PDF/Pub1063_web.pdf"),
        source_row(4, "U.S. Government Accountability Office — GAO-24-104082", "The Marshall Islands nuclear testing legacy: 67 tests conducted between 1946 and 1958.", "https://www.gao.gov/assets/gao-24-104082.pdf"),
        source_row(5, "United Kingdom–Norway Initiative — NPT working paper", "Managed access and information barriers protecting national-security and proliferation-sensitive information during verification research.", "https://assets.publishing.service.gov.uk/media/5a79015fed915d04220670ca/npt_revcon_2010_jwp.pdf"),
        source_row(6, "UN General Assembly — Resolution 79/60 (2 December 2024)", "Addressing the legacy of nuclear weapons: victim assistance and environmental remediation.", "https://documents.un.org/doc/undoc/gen/n24/391/05/pdf/n2439105.pdf"),
        source_row(7, "CTBTO — International Monitoring System", "The global verification network whose radionuclide stations detect airborne radioactive particles and gases.", "https://www.ctbto.org/our-work/verification-regime"),
        source_row(8, "UNSCEAR", "Independent scientific assessment of radiation levels and effects.", "https://www.unscear.org/"),
        source_row(9, "International Court of Justice — Advisory Opinion, 8 July 1996", "Environmental considerations and the conduct of military operations.", "https://www.icj-cij.org/index.php/node/103787"),
    ]
    story += [source_table(sources), Spacer(1, 9), P("PRECISION DECLARATIONS", SECTION)]
    precision = [
        "The Lucky Dragon claim is limited to what the Hiroshima Peace Memorial Museum documents: the vessel was outside the declared danger area and the crew was exposed.",
        "The Semipalatinsk and Marshall Islands figures are verified historical test counts; the chit does not claim every former test site is uniformly contaminated.",
        "The IAEA Semipalatinsk programme is cited as an example of record-based technical cooperation, not as proof that all contamination there is resolved.",
        "The UK–Norway Initiative concerned research and exercises, not a currently binding universal inspection regime.",
        "The Three-Key Standard creates no inspection powers, no liability and no disclosure of weapon designs, locations, readiness or doctrine.",
        "The Standard is a voluntary policy proposal; nothing in it binds any State or prejudges any legal position.",
    ]
    for x in precision:
        story.append(P("• " + x, BULLET))
    story += [Spacer(1, 9),
              thesis_box("<font color='#0B1F3A'>JAPAN'S THREE KEYS:</font><br/><font color='#BC002D'>Source record package. Affected-State counter-assessment. Protected independent review.</font>")]
    return story


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = NumberedDocTemplate(str(OUTPUT))
    doc.build(build_story())
    print(OUTPUT)


if __name__ == "__main__":
    main()
