#!/usr/bin/env python3
"""Build the polished PDF for Japan's fourth substantive chit: The Responsibility Matrix."""

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
OUTPUT = ROOT / "substantive_chits" / "SUBSTANTIVE_CHIT_4.pdf"

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
PALE_STEEL = colors.HexColor("#E8EDF1")
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
MATRIX_TITLE = ParagraphStyle(
    "MatrixTitle",
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
    footer = "SUBSTANTIVE CHIT 04  |  THE RESPONSIBILITY MATRIX  |  SOURCE · BENEFIT · CAPACITY"
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
            title="Substantive Chit 04 — The Responsibility Matrix",
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
        ("3", "COLUMNS OF<br/>RESPONSIBILITY"),
        ("1", "PRIMARY COLUMN:<br/>SOURCE"),
        ("0", "EQUAL FINANCIAL<br/>QUOTAS"),
        ("2013", "JAPAN RANET CBC<br/>TRAINING RUNNING SINCE"),
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


def matrix_card(number, title, sub, bullets, accent, col_w):
    head_text = P(f"{number}  |  {title}<br/><font size='7.4' color='#E8DCC0'>{sub}</font>", MATRIX_TITLE)
    bullet_flow = [P(f"• {b}", BULLET) for b in bullets]
    inner = Table([[head_text], [bullet_flow]], colWidths=[col_w])
    inner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), accent),
        ("BACKGROUND", (0, 1), (0, 1), WHITE),
        ("BOX", (0, 0), (-1, -1), 0.55, colors.HexColor("#C6CFD8")),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (0, 0), 5),
        ("BOTTOMPADDING", (0, 0), (0, 0), 5),
        ("TOPPADDING", (0, 1), (0, 1), 6),
        ("BOTTOMPADDING", (0, 1), (0, 1), 5),
    ]))
    return inner


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
            [P("JAPAN", ParagraphStyle("C4M1", parent=FACT_LABEL, fontSize=9.2)),
             P("UN GENERAL ASSEMBLY", ParagraphStyle("C4M2", parent=FACT_LABEL, fontSize=9.2)),
             P("DIFFERENTIATED RESPONSIBILITIES OF SOURCE · BENEFICIARY · ADVOCATE STATES", ParagraphStyle("C4M3", parent=FACT_LABEL, fontSize=7.7))],
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

    # PAGE 1 — the matrix.
    story += [
        P("SUBSTANTIVE CHIT 04  /  POLISHED SUBMISSION  /  PART I", KICKER),
        P("THE RESPONSIBILITY MATRIX", TITLE),
        P("SOURCE · BENEFIT · CAPACITY — Who must do what, and why", SUBTITLE),
        metadata(), Spacer(1, 7),
        thesis_box("<font color='#BC002D'>THE DOCTRINE:</font><br/>Responsibility follows the source of harm, the security benefit received and the capacity to act. Source responsibility stays primary; every capable voice acquires an implementation burden."),
        Spacer(1, 8),
        P("THE MATRIX", SECTION),
    ]
    col_w = (CONTENT_W - 4) / 3
    matrix = [
        matrix_card("01", "SOURCE", "PRIMARY", [
            "Preserve and index records of tests, production and releases.",
            "Release non-sensitive plume, dose and environmental data.",
            "Provide technical experts and site characterization.",
            "Lead remediation, monitoring and measurable outcomes.",
        ], NAVY, col_w),
        matrix_card("02", "BENEFIT", "SUPPLEMENTARY", [
            "Provide early-warning nodes and emergency contacts.",
            "Register assistance capacities under IAEA RANET.",
            "Contribute laboratories, verification research and exercises.",
            "Support voluntary financing and risk-reduction diplomacy.",
        ], CRIMSON, col_w),
        matrix_card("03", "CAPACITY", "PROPORTIONAL", [
            "Contribute laboratories, experts and training.",
            "Support victim assistance and community participation.",
            "Host repositories, workshops and translation services.",
            "Provide independent review and audit.",
        ], STEEL, col_w),
    ]
    story += [Table([matrix], colWidths=[col_w] * 3, hAlign="LEFT"),
              Spacer(1, 6),
              thesis_box("<font color='#0B1F3A'>SOURCE — primary. BENEFIT — supplementary, not liability. CAPACITY — proportional, never equal quotas.</font>"),
              Spacer(1, 9),
              P("CONTINUE TO PAGE 2  →", ParagraphStyle("Continue", parent=KICKER, alignment=TA_CENTER, fontSize=8.2)),
              PageBreak(),
    ]

    # PAGE 2 — Japan's declaration + register.
    story += [
        P("SUBSTANTIVE CHIT 04  /  POLISHED SUBMISSION  /  PART II", KICKER),
        P("THE RESPONSIBILITY MATRIX  /  JAPAN DECLARES ITS OWN COLUMNS", TITLE),
        P("Self-inoculation before any demand — Japan answers the Matrix first", SUBTITLE),
        P("JAPAN DECLARES ITS OWN COLUMNS", SECTION),
        P("Japan is a beneficiary of United States extended deterrence; the United States has reaffirmed its commitment to the defence of Japan using the full range of its capabilities, including nuclear.<super>[2]</super> Japan does not exempt itself. <b>Security benefit creates responsibility.</b>"),
        P("Japan hosts an IAEA RANET Capacity-Building Centre in Fukushima Prefecture that has delivered international emergency-preparedness training since 2013;<super>[4]</super> maintains monitoring and laboratory capacity; publishes nuclear-material data; and supports international assistance and verification research."),
        thesis_box("<font color='#BC002D'>Japan asks every beneficiary and every advocate: which column will you fill?</font>"),
        Spacer(1, 9),
        P("VOLUNTARY RESPONSIBILITY REGISTER", SECTION),
    ]
    register = [
        "Contributions are recorded, not coerced.",
        "Existing contributions receive credit.",
        "No double counting of the same contribution.",
        "Outcomes are measured: victims assisted, samples analysed, land restored.",
    ]
    reg_rows = [[P("• " + x, CARD_BODY)] for x in register]
    reg_table = Table(reg_rows, colWidths=[CONTENT_W])
    reg_table.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, MIST]),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#BBC5CF")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story += [reg_table, Spacer(1, 9),
              P("EXISTING CONTRIBUTIONS THE REGISTER CREDITS", SECTION),
              P("The Register records contributions once, credits them, and measures outcomes — it does not score politics. Japan: RANET training and published nuclear-material data. Kazakhstan: the Semipalatinsk legacy — 456 tests between 1949 and 1989 — and cooperation with the IAEA on site remediation. The United States: an official stockpile-transparency record and a Department of Energy cleanup programme whose remaining liability has been estimated above half a trillion dollars. The United Kingdom: a published aggregate warhead ceiling and bilateral verification research. Norway: verification research protecting classified attributes through information barriers. South Africa: dismantlement and NPT accession. Austria: humanitarian-impact advocacy and host of IAEA and CTBTO institutions. Mexico, the Philippines and affected-State leaders: sustained advocacy under resolutions 78/240 and 79/60."),
              Spacer(1, 8),
              thesis_box("<font color='#0B1F3A'>A NUCLEAR UMBRELLA CANNOT DELIVER SECURITY ABOVE THE BORDER<br/>WHILE ECOLOGICAL RESPONSIBILITY DISAPPEARS BELOW IT.</font>"),
              PageBreak(),
    ]

    # PAGE 3 — draft recommendations + firewall + counters.
    story += [
        P("SUBSTANTIVE CHIT 04  /  POLISHED SUBMISSION  /  PART III", KICKER),
        P("DRAFT-READY RECOMMENDATIONS", TITLE),
        P("UNGA-safe verbs; nothing commands a sovereign State", SUBTITLE),
        P("DRAFT RECOMMENDATIONS", SECTION),
    ]
    recs = [
        "<b>Requests</b> the Secretary-General to establish, through existing institutions and without creating new organs, a voluntary Responsibility Register recording contributions to monitoring, victim assistance and remediation of transboundary radiological harm;",
        "<b>Invites</b> source States to preserve and release non-sensitive environmental records and to lead remediation, with measurable outcomes reported to the Register;",
        "<b>Encourages</b> extended-deterrence beneficiaries to contribute warning infrastructure, laboratories, training and voluntary financing, without creating liability for any other State's conduct;",
        "<b>Encourages</b> capable States to contribute expertise, victim assistance, independent review and community participation, proportional to capacity;",
        "<b>Calls upon</b> all contributors to credit existing work and to avoid double counting;",
        "<b>Decides</b> to remain seized of the matter.",
    ]
    for i, x in enumerate(recs, 1):
        story += [numbered_recommendation(i, x), Spacer(1, 5)]
    story += [Spacer(1, 4), P("LEGAL FIREWALL", SECTION),
              thesis_box("This matrix is a policy proposal, not an assertion of treaty law. It creates no automatic liability, assigns no equal burden between source and beneficiary, and neither assistance nor monitoring adjudicates compensation. Nothing here requires the disclosure of weapon designs, current operational locations or readiness information."),
              Spacer(1, 8), P("DEBATE COUNTERS", SECTION)]
    counters = [
        ("Beneficiary: “We are not a nuclear-weapon State; why should we contribute?”",
         "NATO itself states that nuclear sharing ensures the benefits, responsibilities and risks of nuclear deterrence are shared among Allies. Japan accepts the same logic for its own security. The question is not whether beneficiaries contribute — it is which column they fill."),
        ("Advocate: “We have no nuclear legacy; we owe nothing.”",
         "Capacity is a column, not a fine. Laboratories, experts, victim assistance and independent review are proportional to capacity. No State is assigned an equal financial quota; every capable voice acquires an implementation burden."),
        ("Source State: “We already do enough.”",
         "Then the Register costs nothing: record it, credit it, and show the outcome. The Matrix does not demand more than a State can prove it is already doing."),
    ]
    for head, body in counters:
        story += [thesis_box(f"<font color='#BC002D'>{head}</font><br/><font color='#0B1F3A'>{body}</font>"), Spacer(1, 6)]
    story += [PageBreak()]

    # PAGE 4 — sources.
    story += [
        P("EVIDENCE LEDGER", KICKER),
        P("SOURCES + PRECISION DECLARATIONS", TITLE),
        P("Ten official or high-quality records supporting the Matrix", SUBTITLE),
    ]
    sources = [
        source_row(1, "NATO — Secretary General Jens Stoltenberg, op-ed", "“NATO's nuclear sharing is a multilateral arrangement that ensures the benefits, responsibilities and risks of nuclear deterrence are shared among Allies.”", "https://www.nato.int/cps/en/natohq/opinions_175663.htm"),
        source_row(2, "Ministry of Foreign Affairs of Japan — Japan–U.S. Extended Deterrence Dialogue", "The United States reaffirmed the commitment to the defence of Japan “using the full range of U.S. defense capabilities, including nuclear.”", "https://www.mofa.go.jp/press/release/pressite_000001_02104.html"),
        source_row(3, "IAEA — Response and Assistance Network (RANET)", "The IAEA mechanism through which States register assistance capacities and request emergency assistance.", "https://www.iaea.org/newscenter/news/assistance-regardless-of-distance-about-the-iaeas-response-and-assistance-network-ranet"),
        source_row(4, "IAEA — RANET Capacity-Building Centre, Fukushima", "International emergency-preparedness training hosted in Fukushima Prefecture since 2013.", "https://www.iaea.org/newscenter/news/advancing-emergency-radiation-monitoring-skills-at-iaea-workshop-in-fukushima"),
        source_row(5, "UN General Assembly — Resolution 79/60 (2 December 2024)", "Victim assistance and environmental remediation for legacy-affected States; requested a one-day international meeting in 2026.", "https://documents.un.org/doc/undoc/gen/n24/391/05/pdf/n2439105.pdf"),
        source_row(6, "UN General Assembly — Resolution 78/240 (22 December 2023)", "Originating text on the legacy of nuclear weapons, recalled by resolution 79/60.", "https://digitallibrary.un.org/record/4043195"),
        source_row(7, "Treaty on the Prohibition of Nuclear Weapons — Articles 6 and 7", "Victim assistance, environmental remediation and cooperation obligations for States parties.", "https://documents.unoda.org/wp-content/uploads/2017/07/NPT.2017.Vol.I-E.pdf"),
        source_row(8, "U.S. Government Accountability Office — DOE cleanup", "Remaining DOE environmental-liability estimates and legacy cleanup oversight.", "https://www.gao.gov/products/gao-26-107820"),
        source_row(9, "IAEA — Semipalatinsk testing-site environmental impact", "Technical cooperation and remediation assessment with Kazakhstan.", "https://www-pub.iaea.org/MTCD/Publications/PDF/Pub1063_web.pdf"),
        source_row(10, "CTBTO — World overview of nuclear testing", "456 tests conducted at the Semipalatinsk test site between 1949 and 1989.", "https://www.ctbto.org/nuclear-testing/history-of-nuclear-testing/world-overview/"),
    ]
    story += [source_table(sources), Spacer(1, 9), P("PRECISION DECLARATIONS", SECTION)]
    precision = [
        "The NATO quotation is the Alliance's own stated policy; it does not prove a legal duty of any member State.",
        "The Japan–U.S. dialogue statement is a diplomatic commitment, not a treaty obligation.",
        "The RANET Capacity-Building Centre claim is limited to what the IAEA reports: training and workshops hosted since 2013.",
        "Resolution 79/60 requested the Secretary-General to convene a meeting in 2026; this chit does not claim the meeting has already occurred.",
        "TPNW Articles 6 and 7 bind States parties only; the chit cites them as design precedent, not as universal law.",
        "The DOE cleanup figure is a GAO-reported estimate, not an appropriation; the Register is voluntary and creates no liability, equal quotas or compensation awards.",
    ]
    for x in precision:
        story.append(P("• " + x, BULLET))
    return story


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = NumberedDocTemplate(str(OUTPUT))
    doc.build(build_story())
    print(OUTPUT)


if __name__ == "__main__":
    main()
