#!/usr/bin/env python3
"""Build the decorated PDF for Japan's second substantive chit."""

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
OUTPUT = ROOT / "substantive_chits" / "SUBSTANTIVE_CHIT_2.pdf"

# Embed a Unicode-capable font so bullets, dashes and typographic punctuation
# remain visible in every PDF viewer.
pdfmetrics.registerFont(TTFont("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

PAGE_W, PAGE_H = A4
TOTAL_PAGES = 5
NAVY = colors.HexColor("#0B1F3A")
CRIMSON = colors.HexColor("#BC002D")
GOLD = colors.HexColor("#C6A15B")
INK = colors.HexColor("#1D2633")
MUTED = colors.HexColor("#5E6875")
PAPER = colors.HexColor("#FAF8F3")
MIST = colors.HexColor("#EEF2F5")
PALE_RED = colors.HexColor("#F8E9EC")
PALE_GOLD = colors.HexColor("#F6F0E3")
WHITE = colors.white

LEFT = 18 * mm
RIGHT = 18 * mm
TOP = 30 * mm
BOTTOM = 21 * mm
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
    fontSize=21,
    leading=23,
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
LAYER_TITLE = ParagraphStyle(
    "LayerTitle",
    parent=BODY,
    fontName="DejaVuSans-Bold",
    fontSize=9.7,
    leading=11,
    textColor=WHITE,
    alignment=TA_LEFT,
    spaceAfter=0,
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
    fontSize=8.05,
    leading=10.3,
    spaceAfter=2,
    alignment=TA_LEFT,
)
SOURCE_LINK = ParagraphStyle(
    "SourceLink",
    parent=SOURCE,
    fontSize=7.1,
    leading=8.8,
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
SHIELD = ParagraphStyle(
    "Shield",
    parent=CENTER_SMALL,
    textColor=WHITE,
    fontSize=7.0,
    leading=8.3,
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
    """Draw a subtle seigaiha-inspired series of arcs."""
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

    # Formal double frame.
    canvas.setStrokeColor(NAVY)
    canvas.setLineWidth(1.0)
    canvas.rect(9 * mm, 9 * mm, PAGE_W - 18 * mm, PAGE_H - 18 * mm, fill=0, stroke=1)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.45)
    canvas.rect(11 * mm, 11 * mm, PAGE_W - 22 * mm, PAGE_H - 22 * mm, fill=0, stroke=1)

    # Navy masthead and Japanese red sun.
    canvas.setFillColor(NAVY)
    canvas.rect(9 * mm, PAGE_H - 23 * mm, PAGE_W - 18 * mm, 14 * mm, fill=1, stroke=0)
    canvas.setFillColor(CRIMSON)
    canvas.circle(PAGE_W - 22 * mm, PAGE_H - 16 * mm, 4.4 * mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("DejaVuSans-Bold", 7.3)
    canvas.drawString(16 * mm, PAGE_H - 15.1 * mm, "DELEGATION OF JAPAN")
    canvas.setFont("DejaVuSans", 6.7)
    canvas.drawString(16 * mm, PAGE_H - 19.2 * mm, "UNITED NATIONS GENERAL ASSEMBLY  |  CCA MUN '26")

    # Thin gold rule below masthead.
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.1)
    canvas.line(12 * mm, PAGE_H - 25.3 * mm, PAGE_W - 12 * mm, PAGE_H - 25.3 * mm)

    # Subtle wave motif and footer.
    draw_wave_motif(canvas, 9.4 * mm, NAVY, 0.11)
    canvas.setFillColor(NAVY)
    canvas.setFont("DejaVuSans-Bold", 6.6)
    footer = "SUBSTANTIVE CHIT 02  |  REPORT • PROTECT • ACCOUNT"
    canvas.drawString(16 * mm, 12.7 * mm, footer)
    page_text = f"PAGE {page} / {TOTAL_PAGES}"
    canvas.drawRightString(PAGE_W - 16 * mm, 12.7 * mm, page_text)
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
            title="Substantive Chit 02 — The Arsenal Ledger",
            author="Delegation of Japan",
            subject="CCA MUN '26 UNGA substantive submission",
        )
        frame = Frame(
            LEFT,
            BOTTOM,
            CONTENT_W,
            PAGE_H - TOP - BOTTOM,
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
            id="content",
        )
        self.addPageTemplates([PageTemplate(id="japan", frames=[frame], onPage=page_decoration)])


def P(text, style=BODY):
    return Paragraph(text, style)


def thesis_box(text):
    table = Table([[P(text, ParagraphStyle("Thesis", parent=BODY, fontName="DejaVuSans-Bold", fontSize=10.1, leading=13, textColor=NAVY, spaceAfter=0))]], colWidths=[CONTENT_W])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE_GOLD),
                ("BOX", (0, 0), (-1, -1), 0.7, GOLD),
                ("LINEBEFORE", (0, 0), (0, -1), 4.2, CRIMSON),
                ("LEFTPADDING", (0, 0), (-1, -1), 11),
                ("RIGHTPADDING", (0, 0), (-1, -1), 11),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def fact_strip():
    facts = [
        ("67", "US TESTS IN THE<br/>MARSHALL ISLANDS"),
        ("23", "LUCKY DRAGON<br/>CREW EXPOSED"),
        ("456", "TESTS AT THE<br/>KAZAKHSTAN SITE"),
        (">$500B", "REMAINING US DOE<br/>CLEANUP ESTIMATE"),
    ]
    cells = []
    for number, label in facts:
        cells.append([P(number, FACT_NUMBER), P(label, FACT_LABEL)])
    table = Table([cells], colWidths=[CONTENT_W / 4] * 4)
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BACKGROUND", (0, 0), (-1, -1), MIST),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#B9C4CF")),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CCD4DC")),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def layer_card(number, title, bullets, accent):
    head = Table(
        [[P(f"{number}  |  {title}", LAYER_TITLE)]],
        colWidths=[CONTENT_W],
    )
    head.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), accent),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 5.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5.5),
            ]
        )
    )
    bullet_flow = [P(f"• {b}", BULLET) for b in bullets]
    body = Table([[bullet_flow]], colWidths=[CONTENT_W])
    body.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                ("BOX", (0, 0), (-1, -1), 0.55, colors.HexColor("#C6CFD8")),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return KeepTogether([head, body, Spacer(1, 5)])


def numbered_recommendation(number, text):
    num = Paragraph(str(number), ParagraphStyle("RecNum", parent=FACT_NUMBER, textColor=WHITE, fontSize=11, leading=12))
    body = P(text, CARD_BODY)
    t = Table([[num, body]], colWidths=[10 * mm, CONTENT_W - 10 * mm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), CRIMSON),
                ("BACKGROUND", (1, 0), (1, 0), PALE_RED),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D6B8C0")),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def source_row(number, title, claim, url):
    num = P(f"[{number}]", ParagraphStyle("SourceNum", parent=SOURCE, fontName="DejaVuSans-Bold", fontSize=8.2, textColor=CRIMSON))
    detail = P(f"<b>{title}</b><br/>{claim}", SOURCE)
    link = P(f'<link href="{url}" color="#31577C"><u>{url}</u></link>', SOURCE_LINK)
    return [num, detail, link]


def build_story():
    story = []

    def source_table(rows):
        table = Table(rows, colWidths=[13 * mm, 70 * mm, CONTENT_W - 83 * mm])
        table.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, MIST]),
                    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#B9C4CF")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D1D7DD")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        return table

    # PAGE 1 — record, category problem and ecological relevance.
    story += [
        P("SUBSTANTIVE CHIT 02  /  ONLINE FLAGSHIP SUBMISSION", KICKER),
        P("THE ARSENAL LEDGER", TITLE),
        P("Making stockpile transparency ecologically meaningful without exposing operations", SUBTITLE),
    ]
    meta = Table(
        [
            [P("DELEGATION", META_HEADER), P("COMMITTEE", META_HEADER), P("MODERATED-CAUCUS FOCUS", META_HEADER)],
            [P("JAPAN", ParagraphStyle("C2Meta1", parent=FACT_LABEL, fontSize=9.2)), P("UN GENERAL ASSEMBLY", ParagraphStyle("C2Meta2", parent=FACT_LABEL, fontSize=9.2)), P("STOCKPILE DISCLOSURE + ECOLOGICAL ACCOUNTABILITY", ParagraphStyle("C2Meta3", parent=FACT_LABEL, fontSize=7.9))],
        ],
        colWidths=[CONTENT_W * 0.22, CONTENT_W * 0.28, CONTENT_W * 0.50],
    )
    meta.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("BACKGROUND", (0, 1), (-1, 1), WHITE),
                ("BOX", (0, 0), (-1, -1), 0.6, NAVY),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C8D0D8")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story += [meta, Spacer(1, 7)]
    story += [
        thesis_box(
            "Stockpile opacity does not only hide warheads. It hides the scale of fissile-material production, retirement, dismantlement, radioactive waste and long-term remediation. Japan proposes three disciplines: <font color='#BC002D'>REPORT</font>, <font color='#BC002D'>PROTECT</font> and <font color='#BC002D'>ACCOUNT</font>."
        ),
        Spacer(1, 8),
    ]

    facts = [
        ("12,187", "ESTIMATED GLOBAL<br/>TOTAL INVENTORY"),
        ("9,745", "ESTIMATED MILITARY<br/>STOCKPILE"),
        ("4,012", "ESTIMATED<br/>DEPLOYED"),
        (">$500B", "REMAINING US DOE<br/>CLEANUP ESTIMATE"),
    ]
    fact_cells=[]
    for number,label in facts:
        fact_cells.append([P(number, FACT_NUMBER), P(label, FACT_LABEL)])
    fact_table=Table([fact_cells], colWidths=[CONTENT_W/4]*4)
    fact_table.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("BACKGROUND",(0,0),(-1,-1),MIST),
        ("BOX",(0,0),(-1,-1),0.6,colors.HexColor("#B9C4CF")),
        ("INNERGRID",(0,0),(-1,-1),0.35,colors.HexColor("#CCD4DC")),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
    ]))
    story += [fact_table, Spacer(1, 8), P("I  |  THE RECORD IS INCOMPLETE AND INCOMPARABLE", SECTION)]
    story += [
        P("SIPRI estimates that nine nuclear-armed States possessed approximately <b>12,187 nuclear weapons</b> in January 2026: <b>9,745</b> in military stockpiles and approximately <b>4,012 deployed</b> with operational forces.<super>[1]</super> These are estimates—not official national declarations—and SIPRI warns that reduced transparency increasingly obstructs assessment."),
        P("The first problem is definitional. A <b>military stockpile</b> includes warheads assigned for possible military use. A <b>total inventory</b> adds retired warheads awaiting dismantlement. A <b>dismantled warhead</b> is no longer a warhead, although its fissile material still requires accounting and disposition."),
        P("The United States officially reported <b>3,748 active and inactive stockpile warheads</b> as of September 2023 and <b>12,088 dismantlements</b> during fiscal years 1994–2023.<super>[2]</super> SIPRI’s later total-inventory estimate is larger because it includes another category and date. The figures are not contradictory; they answer different questions."),
        P("Disclosure remains uneven. The United Kingdom publishes a ceiling of no more than <b>260</b> while withholding operational and deployed categories.<super>[3]</super> France announced an arsenal increase and ended numerical disclosure on 2 March 2026.<super>[4]</super> China publishes no-first-use and minimum-deterrence doctrine but no official warhead total.<super>[5]</super> New START expired on 5 February 2026 without a legally binding successor.<super>[6]</super>"),
        P("II  |  THE ECOLOGICAL LIABILITY BEHIND THE COUNT", SECTION),
        P("Every stockpile implies a material lifecycle: fissile-material production and storage, manufacture, maintenance, transport, retirement, dismantlement, disposition, waste and contaminated facilities. US auditors report that Energy Department sites remain contaminated from decades of weapons production and nuclear-energy research; remaining cleanup was estimated above <b>half a trillion dollars</b>.<super>[7]</super> A warhead may leave the military stockpile years before its waste leaves the public balance sheet."),
        P("III  |  AUTHORITY AND THE REMAINING GAP", SECTION),
        P("The 2010 NPT Action Plan encouraged a standard reporting form and appropriate intervals.<super>[8]</super> A 2025 cross-regional statement called for standardized, comparable reports and interactive discussion.<super>[9]</super> The 2026 NPDI statement called for reports at least twice per Review Cycle.<super>[10]</super> Yet no universal official register exists. Ordinary IAEA safeguards do not count military warheads, and the General Assembly cannot compel classified disclosure. Japan’s framework respects those limits."),
        PageBreak(),
    ]

    # PAGE 2 — architecture.
    story += [
        P("THE PROPOSED FRAMEWORK", KICKER),
        P("IV  |  REPORT • PROTECT • ACCOUNT", TITLE),
        P("One vocabulary, three security tiers and an environmental balance sheet", SUBTITLE),
        layer_card(
            "01", "REPORT — ONE VOCABULARY + COMPARABLE CATEGORIES",
            [
                "Total military stockpile or declared ceiling, with date and definition.",
                "Aggregate deployed strategic and non-strategic categories.",
                "Reserve or non-deployed warheads; retired warheads awaiting dismantlement.",
                "Annual dismantlement and fissile material declared excess to military requirements.",
                "Broad doctrine, risk-reduction and modernization categories.",
                "Environmental Annex: former production sites, waste, contaminated soil or groundwater, cleanup spending and timelines.",
                "National data, external estimates and unresolved uncertainty labelled separately.",
            ], NAVY,
        ),
        layer_card(
            "02", "PROTECT — TRANSPARENCY WITHOUT AN OPERATIONAL BLUEPRINT",
            [
                "Tier I public aggregates: totals, ceilings, categories, dismantlement and environmental liabilities.",
                "Tier II protected exchanges: detailed type and notification data through agreed channels.",
                "Tier III negotiated verification: managed access and information barriers only under mandate and consent.",
                "Exclude exact locations, movement schedules, command-and-control and precise readiness cycles.",
                "Exclude weapon designs, proliferation-sensitive isotopic details and exploitable vulnerabilities.",
            ], CRIMSON,
        ),
        layer_card(
            "03", "ACCOUNT — INTERACTIVE REVIEW + ENVIRONMENTAL OUTCOMES",
            [
                "Public UNODA repository with dated versions and category definitions.",
                "NPT nuclear-weapon States report at least twice per Review Cycle.",
                "Parallel voluntary track for non-NPT possessors using the same public categories.",
                "Dedicated interactive sessions for questions, clarification and correction.",
                "Environmental Annex reviewed beside the force report—from stockpile to waste and remediation.",
                "Transparency remains a baseline for disarmament, never a substitute for it.",
            ], colors.HexColor("#485F75"),
        ),
        P("EVIDENCE-TO-ACTION CONTROL LOGIC", SECTION),
    ]
    ctrl=[
        [P("FAILURE MODE", META_HEADER),P("WHAT GOES WRONG", META_HEADER),P("JAPAN’S CONTROL", META_HEADER)],
        [P("INCOMPATIBLE CATEGORIES", CARD_BODY),P("False contradictions and incomparable totals",CARD_BODY),P("REPORT: glossary, dates and uncertainty labels",CARD_BODY)],
        [P("SECURITY OBJECTION",CARD_BODY),P("Legitimate secrets used to defend total opacity",CARD_BODY),P("PROTECT: public, protected and negotiated tiers",CARD_BODY)],
        [P("REPORTS WITHOUT REVIEW",CARD_BODY),P("Transparency theatre without correction",CARD_BODY),P("ACCOUNT: interactive questions + version history",CARD_BODY)],
        [P("ECOLOGY OMITTED",CARD_BODY),P("Warheads counted; waste and cleanup hidden",CARD_BODY),P("ENVIRONMENTAL ANNEX: lifecycle balance sheet",CARD_BODY)],
    ]
    ct=Table(ctrl,colWidths=[CONTENT_W*.25,CONTENT_W*.35,CONTENT_W*.40])
    ct.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,MIST]),
        ("BOX",(0,0),(-1,-1),.6,colors.HexColor("#B9C4CF")),("INNERGRID",(0,0),(-1,-1),.3,colors.HexColor("#D1D7DD")),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]))
    story += [ct, Spacer(1,7), thesis_box("<font color='#0B1F3A'>A NUMBER WITHOUT A DEFINITION IS NOT TRANSPARENCY.</font><br/>A report without questions is not accountability; an arsenal ledger without environmental liabilities is incomplete."), PageBreak()]

    # PAGE 3 — operative translation, implementation and Japan's own disclosure.
    story += [
        P("FROM FRAMEWORK TO TEXT", KICKER),
        P("V  |  DRAFT-READY<br/>COMMITTEE RECOMMENDATIONS", TITLE),
        P("Three recommendations the General Assembly can adopt without demanding operational secrets", SUBTITLE),
        numbered_recommendation(1,"<b>Requests</b> the Secretary-General, through UNODA and in consultation with interested States, to develop a non-binding Standardized Nuclear Forces and Environmental Accountability Template and public repository;"),
        Spacer(1,6),
        numbered_recommendation(2,"<b>Encourages</b> NPT nuclear-weapon States to report at least twice per Review Cycle and <b>invites</b> non-NPT possessors to submit parallel voluntary reports using comparable public categories, followed by dedicated interactive consideration;"),
        Spacer(1,6),
        numbered_recommendation(3,"<b>Calls upon</b> participating States to include an Environmental Accountability Annex while protecting locations, movement, command-and-control, readiness, design and proliferation-sensitive information."),
        Spacer(1,9),
        P("VI  |  IMPLEMENTATION + RESPONSIBILITY MAP", SECTION),
    ]
    roles=[
        [P("SECRETARY-GENERAL / UNODA",ParagraphStyle("C2Role1",parent=CARD_BODY,fontName="DejaVuSans-Bold",textColor=NAVY)),P("Consult on definitions; maintain repository and version history; convene interactive review.",CARD_BODY)],
        [P("NPT NUCLEAR-WEAPON STATES",ParagraphStyle("C2Role2",parent=CARD_BODY,fontName="DejaVuSans-Bold",textColor=NAVY)),P("Use the common template; report at least twice per cycle; answer technical questions.",CARD_BODY)],
        [P("NON-NPT POSSESSORS",ParagraphStyle("C2Role3",parent=CARD_BODY,fontName="DejaVuSans-Bold",textColor=NAVY)),P("Use a parallel voluntary route without creating an NPT obligation.",CARD_BODY)],
        [P("TECHNICAL INSTITUTIONS",ParagraphStyle("C2Role4",parent=CARD_BODY,fontName="DejaVuSans-Bold",textColor=NAVY)),P("Contribute only within mandate; ordinary IAEA safeguards do not become warhead inspections.",CARD_BODY)],
        [P("COMMUNITIES + EXPERTS",ParagraphStyle("C2Role5",parent=CARD_BODY,fontName="DejaVuSans-Bold",textColor=NAVY)),P("Provide environmental evidence and assess reported cleanup outcomes; supplement, never replace, official data.",CARD_BODY)],
    ]
    rt=Table(roles,colWidths=[54*mm,CONTENT_W-54*mm])
    rt.setStyle(TableStyle([
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[WHITE,MIST]),("BOX",(0,0),(-1,-1),.6,colors.HexColor("#BAC4CE")),
        ("INNERGRID",(0,0),(-1,-1),.3,colors.HexColor("#D1D7DD")),("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]))
    story += [rt, Spacer(1,7)]
    seq=["COMMON GLOSSARY","NATIONAL REPORT","SECURITY REVIEW","INTERACTIVE QUESTIONS","CORRECTED REPORT","ECOLOGY UPDATE"]
    cells=[P(x+("  →" if i<5 else ""),ParagraphStyle(f"C2Seq{i}",parent=CENTER_SMALL,fontSize=6.5,leading=7.8,textColor=WHITE)) for i,x in enumerate(seq)]
    st=Table([cells],colWidths=[CONTENT_W/6]*6)
    st.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),NAVY),("BOX",(0,0),(-1,-1),.6,GOLD),("INNERGRID",(0,0),(-1,-1),.25,colors.HexColor("#4B6279")),("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
    story += [st,Spacer(1,8),P("JAPAN’S ACCOUNTABILITY DECLARATION",SECTION)]
    japan_box=Table([[P("44.4 t",FACT_NUMBER),P("<b>Separated civilian plutonium, end-2024</b><br/>8.6 t in Japan • 35.8 t held abroad • detailed annual reporting since 1994",CARD_BODY),P("SAFEGUARDED",ParagraphStyle("C2JapanBadge",parent=CENTER_SMALL,textColor=WHITE,fontSize=7.1))]],colWidths=[27*mm,CONTENT_W-58*mm,31*mm])
    japan_box.setStyle(TableStyle([("BACKGROUND",(0,0),(0,0),PALE_RED),("BACKGROUND",(1,0),(1,0),WHITE),("BACKGROUND",(2,0),(2,0),CRIMSON),("BOX",(0,0),(-1,-1),.7,CRIMSON),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
    story += [japan_box,Spacer(1,5),P("Japan raises its own figure because the principle is universal: disclose the category, define it accurately, submit it to the applicable safeguards system and permit informed scrutiny. This is civilian material—not a warhead stockpile.<super>[11]</super>",BODY_SMALL),P("SCOPE + LEGAL SAFEGUARDS",SECTION)]
    shields=["NO estimates presented as official","NO exact storage or movements","NO command-and-control or readiness","NO design or isotopic disclosure","NO ordinary IAEA warhead inspections","NO reporting as a substitute for disarmament"]
    sc=[[P("• "+shields[i],SHIELD),P("• "+shields[i+1],SHIELD)] for i in range(0,6,2)]
    sht=Table(sc,colWidths=[CONTENT_W/2]*2)
    sht.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),NAVY),("BOX",(0,0),(-1,-1),.6,GOLD),("INNERGRID",(0,0),(-1,-1),.35,colors.HexColor("#49627B")),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    story += [sht,Spacer(1,8),thesis_box("<font color='#BC002D'>THE WORLD CANNOT REMEDIATE WHAT NUCLEAR POSSESSORS REFUSE TO REPORT.</font><br/>Disclose the category. Protect the operation. Account for the environmental lifecycle."),PageBreak()]

    # PAGE 4 — sources 1 through 6.
    story += [P("EVIDENCE LEDGER  /  PART I",KICKER),P("OFFICIAL RECORDS + NATIONAL DISCLOSURES",TITLE),P("Sources 1–6: global estimates, declared counts and current national policies",SUBTITLE)]
    sources_a=[
        source_row(1,"SIPRI Yearbook 2026 — World Nuclear Forces","12,187 total inventory; 9,745 military stockpile; approximately 4,012 deployed; transparency warning.","https://www.sipri.org/yearbook/2026/08"),
        source_row(2,"US NNSA — Stockpile Transparency","Official 3,748 active/inactive stockpile warheads as of September 2023; 12,088 dismantlements FY1994–2023.","https://www.energy.gov/sites/default/files/2024-08/U.S.%20Nuclear%20Weapons%20Stockpile%20Transparency%207_22_24.pdf"),
        source_row(3,"United Kingdom — 2026 NPT National Report","Ceiling no more than 260; operational-stockpile, deployed-warhead and deployed-missile figures withheld.","https://assets.publishing.service.gov.uk/media/69df600a53469bbcdf408e8b/UK-National-Report-11th-Treaty-on-the-Non-Proliferation-of-Nuclear-Weapons-NPT-Review-Conference.pdf"),
        source_row(4,"French Presidency — Île Longue, 2 March 2026","Official announcement of arsenal increase and end to numerical disclosure.","https://www.elysee.fr/en/emmanuel-macron/2026/03/02/visit-to-the-ile-longue-operational-base"),
        source_row(5,"China MOFA — 2025 arms-control white paper","No-first-use, self-defence and minimum-deterrence doctrine; no official aggregate warhead count.","https://www.fmprc.gov.cn/mfa_eng/xw/wjbxw/202511/t20251127_11761653.html"),
        source_row(6,"United Nations — New START expiration","Secretary-General statement, 5 February 2026: no binding limits on the two largest strategic arsenals; call for successor.","https://media.un.org/unifeed/en/asset/d353/d3532748"),
    ]
    story += [source_table(sources_a),Spacer(1,9),P("CATEGORY DISCIPLINE",SECTION)]
    cat_rows=[
        [P("MILITARY STOCKPILE",CARD_BODY),P("Deployed plus reserve/non-deployed warheads assigned for possible military use.",CARD_BODY)],
        [P("TOTAL INVENTORY",CARD_BODY),P("Military stockpile plus retired warheads awaiting dismantlement.",CARD_BODY)],
        [P("DISMANTLED",CARD_BODY),P("No longer a warhead; fissile material still requires accounting and disposition.",CARD_BODY)],
        [P("ESTIMATE",CARD_BODY),P("External assessment that must never be represented as an official national declaration.",CARD_BODY)],
    ]
    ctab=Table(cat_rows,colWidths=[45*mm,CONTENT_W-45*mm])
    ctab.setStyle(TableStyle([("ROWBACKGROUNDS",(0,0),(-1,-1),[WHITE,MIST]),("BOX",(0,0),(-1,-1),.6,colors.HexColor("#BAC4CE")),("INNERGRID",(0,0),(-1,-1),.3,colors.HexColor("#D1D7DD")),("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    story += [ctab,Spacer(1,8),thesis_box("<font color='#0B1F3A'>PRECISION RULE:</font><br/>Date every figure. Define every category. Label every estimate."),PageBreak()]

    # PAGE 5 — sources 7 through 11 and precision declarations.
    story += [P("EVIDENCE LEDGER  /  PART II",KICKER),P("ACCOUNTABILITY BASIS + JAPAN’S RECORD",TITLE),P("Sources 7–11: ecology, reporting commitments and safeguarded civilian material",SUBTITLE)]
    sources_b=[
        source_row(7,"US GAO — GAO-26-107820","DOE cleanup sites reflect weapons production and nuclear-energy research; remaining cleanup above half a trillion dollars.","https://www.gao.gov/products/gao-26-107820"),
        source_row(8,"United Nations NPT record — Action 21","Standard reporting form and appropriate intervals, voluntarily and without prejudice to national security.","https://documents.un.org/doc/undoc/gen/n24/140/15/pdf/n2414015.pdf"),
        source_row(9,"Japan MOFA — Cross-regional statement, 9 May 2025","Standardized and comparable national reports plus interactive discussion.","https://www.mofa.go.jp/mofaj/files/100845120.pdf"),
        source_row(10,"NPDI — 2026 NPT Review Conference statement","Nuclear-weapon States report at least twice per Review Cycle; dedicated interactive consideration.","https://estatements.un.org/estatements/14.0447/20260428100000000/vNCRzyobSXGC/AxTRBQDc_nyc_en.pdf"),
        source_row(11,"Japan Atomic Energy Commission — Plutonium 2024","44.4 tonnes separated civilian plutonium; 8.6 domestic, 35.8 abroad; annual reporting and safeguards conclusion.","https://www.aec.go.jp/bunya/04/plutonium/20250805_e.pdf"),
    ]
    story += [source_table(sources_b),Spacer(1,9),P("PRECISION DECLARATIONS",SECTION)]
    precision=[
        "SIPRI’s 12,187 is an estimate, not an official UN or national total.",
        "The official US 3,748 figure is a September 2023 military-stockpile category—not SIPRI’s January 2026 total inventory.",
        "No unofficial French, Chinese, Russian, Indian, Israeli or DPRK estimate is presented as an official national count.",
        "Ordinary IAEA safeguards are not assigned a universal warhead-inspection mandate.",
        "Japan’s 44.4 tonnes concern separated civilian plutonium, not nuclear weapons; all material in Japan remains under safeguards.",
        "Transparency is a basis for accountability and verification, never a substitute for disarmament.",
    ]
    for item in precision: story.append(P("• "+item,BULLET))
    story += [Spacer(1,8),thesis_box("<font color='#0B1F3A'>THE STANDARD JAPAN ASKS THE COMMITTEE TO ADOPT:</font><br/><font color='#BC002D'>Report the arsenal. Protect the operation. Account for the cleanup.</font>")]
    return story

def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = NumberedDocTemplate(str(OUTPUT))
    doc.build(build_story())
    print(OUTPUT)


if __name__ == "__main__":
    main()
