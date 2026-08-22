#!/usr/bin/env python3
"""Build the polished PDF for Japan's first substantive chit: From Fallout Records to Remediation (expanded detailed edition)."""

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
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "substantive_chits" / "SUBSTANTIVE_CHIT_1.pdf"

pdfmetrics.registerFont(TTFont("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

PAGE_W, PAGE_H = A4
TOTAL_PAGES = 6
NAVY = colors.HexColor("#0B1F3A")
CRIMSON = colors.HexColor("#BC002D")
GOLD = colors.HexColor("#C6A15B")
INK = colors.HexColor("#1D2633")
PAPER = colors.HexColor("#FAF8F3")
MIST = colors.HexColor("#EEF2F5")
PALE_RED = colors.HexColor("#F8E9EC")
PALE_GOLD = colors.HexColor("#F6F0E3")
STEEL = colors.HexColor("#485F75")
WHITE = colors.white

LEFT = 18 * mm
RIGHT = 18 * mm
TOP = 26 * mm
BOTTOM = 16 * mm
CONTENT_W = PAGE_W - LEFT - RIGHT

styles = getSampleStyleSheet()

BODY = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    fontName="DejaVuSans",
    fontSize=9.4,
    leading=12.4,
    textColor=INK,
    alignment=TA_JUSTIFY,
    spaceAfter=5,
    allowWidows=0,
    allowOrphans=0,
)
BODY_SMALL = ParagraphStyle(
    "BodySmall",
    parent=BODY,
    fontSize=8.7,
    leading=11.2,
    spaceAfter=3.5,
)
TITLE = ParagraphStyle(
    "Title",
    parent=styles["Title"],
    fontName="DejaVuSans-Bold",
    fontSize=19,
    leading=21,
    textColor=NAVY,
    alignment=TA_LEFT,
    spaceAfter=5,
)
SUBTITLE = ParagraphStyle(
    "Subtitle",
    parent=BODY,
    fontName="DejaVuSans-Bold",
    fontSize=10.1,
    leading=12.8,
    textColor=CRIMSON,
    alignment=TA_LEFT,
    spaceAfter=7,
)
KICKER = ParagraphStyle(
    "Kicker",
    parent=BODY,
    fontName="DejaVuSans-Bold",
    fontSize=7.4,
    leading=8.8,
    textColor=CRIMSON,
    tracking=1.3,
    spaceAfter=4,
)
SECTION = ParagraphStyle(
    "Section",
    parent=BODY,
    fontName="DejaVuSans-Bold",
    fontSize=11,
    leading=12.6,
    textColor=NAVY,
    spaceBefore=4,
    spaceAfter=4.5,
)
CARD_BODY = ParagraphStyle(
    "CardBody",
    parent=BODY_SMALL,
    fontSize=8.1,
    leading=10.2,
    spaceAfter=0,
)
BULLET = ParagraphStyle(
    "Bullet",
    parent=CARD_BODY,
    leftIndent=9,
    firstLineIndent=-5,
    bulletIndent=0,
    spaceBefore=0,
    spaceAfter=2.2,
)
SOURCE = ParagraphStyle(
    "Source",
    parent=BODY_SMALL,
    fontSize=7.1,
    leading=8.9,
    spaceAfter=1.4,
    alignment=TA_LEFT,
)
SOURCE_LINK = ParagraphStyle(
    "SourceLink",
    parent=SOURCE,
    fontSize=6.2,
    leading=7.6,
    textColor=colors.HexColor("#31577C"),
)
CENTER_SMALL = ParagraphStyle(
    "CenterSmall",
    parent=BODY_SMALL,
    alignment=TA_CENTER,
    fontName="DejaVuSans-Bold",
    fontSize=7.1,
    leading=8.4,
)
META_HEADER = ParagraphStyle(
    "MetaHeader",
    parent=CENTER_SMALL,
    textColor=WHITE,
)
FACT_NUMBER = ParagraphStyle(
    "FactNumber",
    parent=CENTER_SMALL,
    fontName="DejaVuSans-Bold",
    fontSize=15,
    leading=16,
    textColor=CRIMSON,
)
FACT_LABEL = ParagraphStyle(
    "FactLabel",
    parent=CENTER_SMALL,
    textColor=NAVY,
)
LAYER_TITLE = ParagraphStyle(
    "LayerTitle",
    parent=BODY,
    fontName="DejaVuSans-Bold",
    fontSize=9.4,
    leading=11,
    textColor=WHITE,
    alignment=TA_LEFT,
    spaceAfter=0,
)
QUOTE = ParagraphStyle(
    "Quote",
    parent=BODY,
    fontName="DejaVuSans-Bold",
    fontSize=10.6,
    leading=13.6,
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
    footer = "SUBSTANTIVE CHIT 01  |  NUCLEAR LEGACY EVIDENCE + RESPONSE MECHANISM  |  MONITOR · RESPOND · REMEDIATE"
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
            title="Substantive Chit 01 — From Fallout Records to Remediation",
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
    table = Table([[P(text, ParagraphStyle("Thesis", parent=BODY, fontName="DejaVuSans-Bold", fontSize=9.8, leading=12.4, textColor=NAVY, spaceAfter=0))]], colWidths=[CONTENT_W])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE_GOLD),
        ("BOX", (0, 0), (-1, -1), 0.7, GOLD),
        ("LINEBEFORE", (0, 0), (0, -1), 4.2, CRIMSON),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return table


def fact_strip():
    facts = [
        ("23", "LUCKY DRAGON<br/>CREW EXPOSED"),
        ("456", "TESTS AT<br/>SEMIPALATINSK"),
        ("67", "US TESTS IN THE<br/>MARSHALL ISLANDS"),
        (">$500B", "REMAINING US DOE<br/>CLEANUP ESTIMATE"),
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
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def layer_card(number, title, bullets, accent):
    head = Table([[P(f"{number}  |  {title}", LAYER_TITLE)]], colWidths=[CONTENT_W])
    head.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), accent),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
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
    return [head, body]


def numbered_recommendation(number, text):
    num = P(str(number), ParagraphStyle("RecNum", parent=FACT_NUMBER, textColor=WHITE, fontSize=10.5, leading=11.5))
    body = P(text, CARD_BODY)
    t = Table([[num, body]], colWidths=[9 * mm, CONTENT_W - 9 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), CRIMSON),
        ("BACKGROUND", (1, 0), (1, 0), PALE_RED),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D6B8C0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
    ]))
    return t


def source_row(number, title, claim, url):
    num = P(f"[{number}]", ParagraphStyle("SourceNum", parent=SOURCE, fontName="DejaVuSans-Bold", fontSize=7.6, textColor=CRIMSON))
    detail = P(f"<b>{title}</b> — {claim}", SOURCE)
    link = P(f'<link href="{url}" color="#31577C"><u>{url}</u></link>', SOURCE_LINK)
    return [num, detail, link]


def build_story():
    story = []

    def source_table(rows):
        t = Table(rows, colWidths=[11 * mm, 66 * mm, CONTENT_W - 77 * mm])
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
            [P("JAPAN", ParagraphStyle("C1M1", parent=FACT_LABEL, fontSize=9)),
             P("UN GENERAL ASSEMBLY", ParagraphStyle("C1M2", parent=FACT_LABEL, fontSize=9)),
             P("TRANSBOUNDARY RADIOLOGICAL CONTAMINATION FROM TESTING + PRODUCTION LEGACIES", ParagraphStyle("C1M3", parent=FACT_LABEL, fontSize=7.5))],
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

    # PAGE 1 — cover, thesis, the record.
    story += [
        P("SUBSTANTIVE CHIT 01  /  POLISHED SUBMISSION  /  PART I", KICKER),
        P("FROM FALLOUT RECORDS TO REMEDIATION", TITLE),
        P("A Voluntary Nuclear Legacy Evidence and Response Mechanism", SUBTITLE),
        metadata(), Spacer(1, 6),
        thesis_box("<font color='#BC002D'>THE THESIS:</font><br/>The debate has named the harm; it has not named the evidentiary process required to prove, monitor and remediate it. Japan proposes a voluntary, consent-based mechanism in three connected functions: MONITOR · RESPOND · REMEDIATE."),
        Spacer(1, 7),
        P("THE RECORD: BOUNDARIES ARE NOT A SAFETY SYSTEM", SECTION),
        P("The General Assembly has recognized that the consequences of nuclear-weapons use and testing have transcended national borders, contaminated environments and continued to harm health, food security and development.<super>[1]</super> The history is specific:"),
    ]
    record_rows = [
        ("MARSHALL ISLANDS", "67 nuclear tests conducted by the United States between 1946 and 1958.<super>[2]</super>"),
        ("LUCKY DRAGON NO. 5", "1 March 1954: the Japanese fishing vessel was operating well outside the declared United States danger area when Castle Bravo fallout reached it; all 23 crew members were exposed.<super>[3]</super> A line drawn around a test area did not contain the material."),
        ("SEMIPALATINSK", "456 tests between 1949 and 1989, 116 above ground, across roughly 18,500 square kilometres; IAEA-linked records document plumes extending beyond the site boundary.<super>[4][5]</super>"),
        ("PRODUCTION LEGACIES", "U.S. DOE sites remain contaminated from decades of weapons production and nuclear research; remaining Environmental Management cleanup is estimated above half a trillion dollars.<super>[6]</super> A retired warhead does not retire its waste."),
    ]
    record_cells = [[P(f"<b><font color='#BC002D'>{h}</font></b><br/>{b}", CARD_BODY)] for h, b in record_rows]
    record_table = Table(record_cells, colWidths=[CONTENT_W])
    record_table.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, MIST]),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#B9C4CF")),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D1D7DD")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story += [record_table, Spacer(1, 6),
              fact_strip(), Spacer(1, 6),
              thesis_box("<font color='#0B1F3A'>No national boundary functioned as a radiological barrier. No national archive alone can serve as the final scientific authority.</font>"),
              Spacer(1, 7),
              P("THE ASYMMETRIC EVIDENTIARY BURDEN", SECTION),
              P("Today the affected State must usually disprove a source State's assessment using evidence the source State controls — records, models, dose calculations and conclusions. The Mechanism inverts the burden: every finding is labelled <b>measured data</b>, <b>modelled estimate</b> or <b>unresolved uncertainty</b>, with assumptions and chain of custody disclosed. Labels, not adjectives, decide what the world may rely on."),
              P("CONTINUE TO PAGE 2  →", ParagraphStyle("Continue", parent=KICKER, alignment=TA_CENTER, fontSize=8.2)),
              PageBreak(),
    ]

    # PAGE 2 — institutional gap + MONITOR layer.
    story += [
        P("SUBSTANTIVE CHIT 01  /  POLISHED SUBMISSION  /  PART II", KICKER),
        P("THE INSTITUTIONAL GAP + LAYER ONE", TITLE),
        P("What exists, what is missing, and the MONITOR function", SUBTITLE),
        P("THE INSTITUTIONAL GAP", SECTION),
        P("Existing institutions are necessary but not interchangeable: the CTBTO monitoring system detects explosions but is not a remediation authority;<super>[7]</super> IAEA safeguards verify peaceful use but create no automatic right to inspect former military sites; UNSCEAR evaluates science but administers no cleanup;<super>[8]</super> the IAEA Incident and Emergency Centre and RANET provide emergency notification and requested assistance but are not standing legacy mechanisms;<super>[9]</super> ENVIRONET shares remediation expertise but compiles no universal evidence record.<super>[10]</super> Records remain fragmented across national archives, and affected States may lack the laboratories or source data to challenge a source State's assessment."),
        P("The machinery to build on exists: General Assembly resolutions 78/240, 79/60 and 80/56;<super>[11][1][12]</super> the International Meeting on Victim Assistance and Environmental Remediation to be convened on 1 September 2026;<super>[12]</super> the independent Scientific Panel on the Effects of Nuclear War, established in December 2023 and appointed in July 2025;<super>[13][14]</super> IAEA safety standards including GSG-15 on remediation;<super>[15]</super> the Early Notification and Assistance Conventions;<super>[16][17]</super> and the victim-assistance and remediation duties of the TPNW for its States parties.<super>[18]</super> The Mechanism connects these pieces into one evidentiary process; it does not invent a new bureaucracy."),
        P("LAYER ONE — MONITOR", SECTION),
        P("Each participating State would submit a common public annex through a twelve-field reporting template:", BODY),
    ]
    template_fields = [
        "Test events — dates, broad locations, atmospheric or underground classification.",
        "Production facilities — former and current sites, decommissioning status.",
        "Waste categories and inventory — types, quantities, management status.",
        "Contaminated media — soil, groundwater, sediments, marine pathways.",
        "Monitoring network and methods — stations, instruments, sampling protocols.",
        "Dose reconstruction and meteorological records — declassified data and methods.",
        "Transboundary pathway assessments — plausible routes across borders, shared waters, food chains.",
        "Remediation status and plans — completed, ongoing, planned.",
        "Expenditure and funding sources — published categories.",
        "Timelines and milestones — published schedules.",
        "Measurable completion indicators — activity distinguished from outcome.",
        "Uncertainty register — data gaps, model limitations, version history.",
    ]
    tf_rows = []
    for i, f in enumerate(template_fields, 1):
        tf_rows.append([P(f"<b>{i:02d}</b>", ParagraphStyle("TF", parent=CARD_BODY, fontName="DejaVuSans-Bold", textColor=CRIMSON)), P(f, CARD_BODY)])
    tf_table = Table(tf_rows, colWidths=[9 * mm, CONTENT_W - 9 * mm])
    tf_table.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, MIST]),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#B9C4CF")),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D1D7DD")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ]))
    story += [tf_table, Spacer(1, 6),
              thesis_box("Weapon designs, exact vulnerabilities, operational locations and proliferation-sensitive information remain protected. The template is a non-binding reporting discipline — not a treaty, not an inspection regime."),
              P("CONTINUE TO PAGE 3  →", ParagraphStyle("Continue", parent=KICKER, alignment=TA_CENTER, fontSize=8.2)),
              PageBreak(),
    ]

    # PAGE 3 — RESPOND + REMEDIATE.
    story += [
        P("SUBSTANTIVE CHIT 01  /  POLISHED SUBMISSION  /  PART III", KICKER),
        P("LAYERS TWO AND THREE", TITLE),
        P("RESPOND and REMEDIATE — consent, notification and measurable outcomes", SUBTITLE),
        P("LAYER TWO — RESPOND", SECTION),
        P("An affected territorial State could voluntarily request a technical review coordinated through a roster compiled by the Secretary-General, drawing strictly within existing mandates on the IAEA, UNSCEAR, CTBTO expertise, regional bodies and qualified national laboratories. The source State would be invited to provide original records and methodology. <b>No site visit occurs without host-State consent.</b> Findings would be published with the three-class evidence label."),
        P("When newly identified legacy contamination presents a <b>plausible significant cross-border pathway</b>, participating States would promptly notify potentially affected neighbours and share sampling methods. Plausibility criteria include:", BODY),
    ]
    notify_rows = [
        "Detection of elevated radionuclide concentrations above agreed screening levels.",
        "Model results indicating potential transboundary transport.",
        "Monitored changes at legacy sites.",
        "Any development a participating State considers potentially significant.",
    ]
    for n in notify_rows:
        story.append(P("• " + n, BULLET))
    story += [
        Spacer(1, 2),
        thesis_box("NOTIFICATION IS BEFORE ATTRIBUTION — it does not predetermine legal liability or political responsibility. Warning must not wait for blame.<super>[16]</super>"),
        Spacer(1, 7),
        P("LAYER THREE — REMEDIATE", SECTION),
        P("A voluntary technical and financial assistance window with three tracks:", BODY),
    ]
    track_rows = [
        ("TRACK A", "ASSESSMENT + MONITORING", "Laboratories, sampling equipment, training, data interpretation."),
        ("TRACK B", "HEALTH + VICTIMS", "Health screening, long-term care, psychosocial support."),
        ("TRACK C", "REMEDIATION OPERATIONS", "Source control, soil, water and food-chain measures, safe waste management."),
    ]
    track_cells = [[P(f"<b><font color='#BC002D'>{a}</font></b><br/><b>{b}</b>", CARD_BODY), P(c, CARD_BODY)] for a, b, c in track_rows]
    track_table = Table(track_cells, colWidths=[CONTENT_W * 0.32, CONTENT_W * 0.68])
    track_table.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, MIST]),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#B9C4CF")),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D1D7DD")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story += [track_table, Spacer(1, 6)]
    outcome_rows = [
        "Priority: affected population size and vulnerability; food and water pathways; limited national capacity; community request; demonstrated need.",
        "Community participation is mandatory in project design and outcome review.",
        "Donors cannot control scientific conclusions.",
        "No assistance may require an affected State to surrender its legal position.",
        "Outcomes reported publicly: people receiving care; samples analysed; contaminated material secured; water and soil trends; access restrictions reduced; livelihoods restored; completion against timelines.",
    ]
    for o in outcome_rows:
        story.append(P("• " + o, BULLET))
    story += [
        Spacer(1, 3),
        thesis_box("EVIDENCE-TO-ACTION: fragmented records → MONITOR creates common categories; contested pathways → RESPOND creates consent-based review and notification; unmeasured cleanup → REMEDIATE requires published indicators. No layer substitutes for another."),
        P("CONTINUE TO PAGE 4  →", ParagraphStyle("Continue", parent=KICKER, alignment=TA_CENTER, fontSize=8.2)),
        PageBreak(),
    ]

    # PAGE 4 — draft recommendations + implementation map + scope.
    story += [
        P("SUBSTANTIVE CHIT 01  /  POLISHED SUBMISSION  /  PART IV", KICKER),
        P("DRAFT-READY RECOMMENDATIONS", TITLE),
        P("UNGA-safe verbs; nothing commands a sovereign State", SUBTITLE),
        P("DRAFT RECOMMENDATIONS", SECTION),
    ]
    recs = [
        "<b>Requests</b> the Secretary-General, in consultation with relevant international organizations acting within their mandates, to develop a non-binding Nuclear Legacy Environmental Reporting Template and public repository;",
        "<b>Invites</b> affected States, by consent, to request independent technical review and <b>encourages</b> source States to provide declassified test, plume, dose and production records relevant to environmental assessment;",
        "<b>Encourages</b> participating States to notify potentially affected neighbours promptly where newly identified legacy contamination presents a plausible significant cross-border pathway, without predetermining liability or attribution;",
        "<b>Encourages</b> voluntary technical and financial assistance through existing mechanisms — including IAEA RANET and ENVIRONET — with affected-community participation, transparent expenditure and periodic outcome reporting;",
        "<b>Recommends</b> that participating States label environmental findings as measured data, modelled estimates or unresolved uncertainty, with chain-of-custody and confidence information;",
        "<b>Invites</b> relevant organizations to support regional laboratories, training and joint monitoring exercises for legacy-affected developing States;",
        "<b>Decides</b> to remain seized of the matter and <b>requests</b> the Secretary-General to report on implementation to the General Assembly.",
    ]
    for i, x in enumerate(recs, 1):
        story += [numbered_recommendation(i, x), Spacer(1, 4)]
    story += [
        Spacer(1, 4),
        P("IMPLEMENTATION MAP", SECTION),
    ]
    impl_rows = [
        ("SECRETARY-GENERAL / UNODA", "Consult on the template, maintain the repository, compile the technical roster, summarize participation without grading political positions."),
        ("AFFECTED TERRITORIAL STATE", "Controls consent for site access, requests review, nominates community representatives, approves publication of findings."),
        ("SOURCE STATE", "Supplies declassified records, methodology, uncertainty ranges and relevant technical experts."),
        ("TECHNICAL INSTITUTIONS", "Contribute only within existing mandates; distinguish measurement, modelling and unresolved uncertainty."),
        ("DONORS + PARTNERS", "Provide voluntary finance, laboratories, training and remediation expertise without controlling scientific conclusions."),
    ]
    impl_cells = [[P(f"<b>{a}</b>", CARD_BODY), P(b, CARD_BODY)] for a, b in impl_rows]
    impl_table = Table(impl_cells, colWidths=[CONTENT_W * 0.30, CONTENT_W * 0.70])
    impl_table.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, MIST]),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#B9C4CF")),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D1D7DD")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
    ]))
    story += [impl_table, Spacer(1, 6),
              P("SCOPE SAFEGUARDS", SECTION),
              thesis_box("No compulsory inspections. No determination of historical legal liability. No exposure of weapon designs. No claim that every test crossed a border or every site is equally dangerous. Weapons-testing and production legacies are distinguished from reactor accidents, routine safeguarded civilian operations and current regulated releases. No new organs. No new financial assessments."),
              PageBreak(),
    ]

    # PAGE 5 — sources and precision.
    story += [
        P("EVIDENCE LEDGER", KICKER),
        P("SOURCES + PRECISION DECLARATIONS", TITLE),
        P("Eighteen official or high-quality records supporting the mechanism", SUBTITLE),
    ]
    sources = [
        source_row(1, "UN General Assembly — Resolution 79/60 (2 December 2024)",
                   "Legacy of nuclear weapons; transcended borders; one-day international meeting requested for 2026.",
                   "https://documents.un.org/doc/undoc/gen/n24/391/05/pdf/n2439105.pdf"),
        source_row(2, "U.S. GAO — GAO-24-104082",
                   "Marshall Islands: 67 tests between 1946 and 1958; continuing contamination management.",
                   "https://www.gao.gov/assets/gao-24-104082.pdf"),
        source_row(3, "Hiroshima Peace Memorial Museum — Lucky Dragon",
                   "Vessel well outside the declared danger area; 23 crew exposed.",
                   "https://hpmmuseum.jp/virtual/VirtualMuseum_e/exhibit_e/exh0307_e/exh03078_e.html"),
        source_row(4, "IAEA — Radiological Conditions at the Semipalatinsk Test Site (Pub. 1063)",
                   "456 tests, 116 above ground; site characteristics.",
                   "https://www-pub.iaea.org/MTCD/Publications/PDF/Pub1063_web.pdf"),
        source_row(5, "IAEA INIS — population dose around Semipalatinsk",
                   "Off-site plume and dose-reconstruction record.",
                   "https://inis.iaea.org/records/ejdbm-x3087"),
        source_row(6, "U.S. GAO — GAO-26-107820 (2 March 2026)",
                   "DOE remaining Environmental Management cleanup above half a trillion dollars.",
                   "https://www.gao.gov/products/gao-26-107820"),
        source_row(7, "CTBTO — International Monitoring System",
                   "337 planned facilities; nearly 90 per cent operational.",
                   "https://www.ctbto.org/news-and-events/news/ctbto-upgrades-online-services-member-states"),
        source_row(8, "UNSCEAR",
                   "Independent scientific assessment of radiation levels and effects.",
                   "https://www.unscear.org/"),
        source_row(9, "IAEA — Incident and Emergency Centre + RANET",
                   "Emergency notification, information exchange and request-based assistance.",
                   "https://www.iaea.org/newscenter/news/assistance-regardless-of-distance-about-the-iaeas-response-and-assistance-network-ranet"),
        source_row(10, "IAEA — ENVIRONET",
                   "Network of Environmental Management and Remediation; legacy-site technical cooperation.",
                   "https://www.iaea.org/newscenter/news/coming-full-circle"),
        source_row(11, "UN General Assembly — Resolution 78/240 (22 December 2023)",
                   "Originating text, tabled by Kazakhstan and Kiribati; 161 votes in favour.",
                   "https://yearbook.unoda.org/en-us/2023/chapter1/"),
        source_row(12, "UNODA — International Meeting, 1 September 2026",
                   "Convened pursuant to resolutions 79/60 and 80/56.",
                   "https://meetings.unoda.org/international-meeting-on-victim-assistance-and-environmental-remediation-2026"),
        source_row(13, "United Nations — Scientific Panel announcement (17 July 2025)",
                   "21 members; report to the General Assembly in 2027.",
                   "https://press.un.org/en/2025/dc3900.doc.htm"),
        source_row(14, "Princeton SGS — Panel establishment",
                   "December 2023 resolution; 136 in favour, 3 against.",
                   "https://spia.princeton.edu/news/un-approves-sgs-backed-global-study-nuclear-war"),
        source_row(15, "IAEA — Safety Standards GSG-15 (2022)",
                   "Stepwise remediation strategy for areas affected by past activities or events.",
                   "https://www.iaea.org/resources/safety-standards"),
        source_row(16, "IAEA — Convention on Early Notification (1986)",
                   "Notification where a covered accident may produce an internationally significant transboundary release.",
                   "https://www.iaea.org/topics/nuclear-safety-conventions/convention-early-notification-nuclear-accident"),
        source_row(17, "IAEA — Convention on Assistance (1986/1987)",
                   "Framework for prompt international assistance upon request.",
                   "https://www.iaea.org/topics/nuclear-safety-conventions/convention-assistance-case-nuclear-accident-or-radiological-emergency"),
        source_row(18, "Treaty on the Prohibition of Nuclear Weapons — Articles 6 and 7",
                   "Victim assistance, environmental remediation and cooperation; binding on States parties.",
                   "https://treaties.un.org/doc/Treaties/2017/07/20170707%2003-42%20PM/Ch_XXVI_9.pdf"),
    ]
    story += [source_table(sources), PageBreak()]

    # PAGE 6 — precision declarations and closing.
    story += [
        P("PRECISION DECLARATIONS", KICKER),
        P("CLAIM NOTES + FACT SAFEGUARDS", TITLE),
        P("Every factual claim in the submission, with its exact evidentiary limit", SUBTITLE),
    ]
    precision = [
        "“More than half a trillion dollars” is the DOE estimate reported by GAO; not attributed exclusively to current warheads.",
        "Semipalatinsk plumes “beyond the site boundary” is not a claim that every plume crossed an international border.",
        "Lucky Dragon is evidence that fallout exceeded the declared danger area, not a claim about every nuclear test.",
        "Semipalatinsk area (≈18,500 km²) and counts (456 total, 116 above ground) follow IAEA and CTBTO records.",
        "The 1 September 2026 International Meeting is referenced as a scheduled process pursuant to resolutions 79/60 and 80/56.",
        "The Scientific Panel is referenced as established (December 2023) and appointed (July 2025); report anticipated 2027.",
        "TPNW Articles 6–7 bind States parties only; cited as precedent, not universal law. GSG-15 is guidance, not a treaty.",
        "The Early Notification and Assistance Conventions are design precedents; automatic application to military legacy sites is not claimed.",
        "All institutional participation is qualified by consent and existing legal mandates.",
    ]
    for x in precision:
        story.append(P("• " + x, BULLET))
    story += [Spacer(1, 7),
              thesis_box("<font color='#0B1F3A'>A LINE ON A MAP NEVER CONTAINED FALLOUT.<br/><font color='#BC002D'>A METHOD SHARED BY ALL STATES CAN.</font></font>")]
    return story


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = NumberedDocTemplate(str(OUTPUT))
    doc.build(build_story())
    print(OUTPUT)


if __name__ == "__main__":
    main()
