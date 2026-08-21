#!/usr/bin/env python3
"""Build the decorated PDF for Japan's first substantive chit."""

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
OUTPUT = ROOT / "substantive_chits" / "SUBSTANTIVE_CHIT_1.pdf"

# Embed a Unicode-capable font so bullets, dashes and typographic punctuation
# remain visible in every PDF viewer.
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
    footer = "SUBSTANTIVE CHIT 01  |  MONITOR • RESPOND • REMEDIATE"
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
            title="Substantive Chit 01 — From Fallout Records to Remediation",
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

    # PAGE 1
    story += [
        P("SUBSTANTIVE CHIT 01  /  ONLINE FLAGSHIP SUBMISSION", KICKER),
        P("FROM FALLOUT RECORDS<br/>TO REMEDIATION", TITLE),
        P("A voluntary, consent-based Nuclear Legacy Evidence and Response Mechanism", SUBTITLE),
    ]

    meta = Table(
        [
            [P("DELEGATION", CENTER_SMALL), P("COMMITTEE", CENTER_SMALL), P("MODERATED-CAUCUS FOCUS", CENTER_SMALL)],
            [P("JAPAN", ParagraphStyle("MetaBig", parent=FACT_LABEL, fontSize=9.2)), P("UN GENERAL ASSEMBLY", ParagraphStyle("MetaBig2", parent=FACT_LABEL, fontSize=9.2)), P("PAST TESTING + PRODUCTION LEGACIES", ParagraphStyle("MetaBig3", parent=FACT_LABEL, fontSize=8.4))],
        ],
        colWidths=[CONTENT_W * 0.22, CONTENT_W * 0.28, CONTENT_W * 0.50],
    )
    meta.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
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
            "The debate has named the harm; it has not yet named the evidentiary process required to prove, monitor and remediate it. Japan proposes three linked functions: <font color='#BC002D'>MONITOR</font>, <font color='#BC002D'>RESPOND</font> and <font color='#BC002D'>REMEDIATE</font>."
        ),
        Spacer(1, 8),
        fact_strip(),
        Spacer(1, 8),
        P("I  |  THE VERIFIED RECORD", SECTION),
        P(
            "The General Assembly has expressly recognized that the consequences of nuclear-weapons use and testing have <b>transcended national borders</b>, contaminated environments and continued to harm health, food security and development.<super>[1]</super>"
        ),
        P(
            "The United States conducted <b>67 nuclear tests in the Marshall Islands</b>.<super>[2]</super> On 1 March 1954, <i>Lucky Dragon No. 5</i> was operating <b>well outside the declared United States danger area</b> when Castle Bravo fallout reached it; all <b>23 crew members</b> were exposed.<super>[3]</super> A line drawn around a test area did not contain the radioactive material."
        ),
        P(
            "At the former Soviet test site in Kazakhstan, <b>456 tests</b> were conducted, including <b>116 above ground</b>, across approximately <b>19,000 square kilometres</b>.<super>[4]</super> IAEA-linked dose-reconstruction records document fallout plumes beyond the test-site boundary.<super>[5]</super> Japan does not claim every part of the site is equally contaminated; the record instead proves the need for site-specific monitoring and risk classification."
        ),
        P(
            "Production legacies are equally material. US auditors report that Department of Energy sites remain contaminated from decades of nuclear-weapons production and nuclear-energy research. In May 2025, the Department estimated that remaining cleanup would cost <b>more than half a trillion dollars</b>.<super>[6]</super> A retired warhead does not retire its waste, contaminated facilities, soil or groundwater."
        ),
        P("II  |  THE INSTITUTIONAL GAP", SECTION),
        P(
            "Existing institutions are necessary but not interchangeable. The CTBTO system detects nuclear explosions; it is not a universal remediation authority.<super>[7]</super> IAEA safeguards verify peaceful-use commitments; they do not create an automatic right to inspect every former military site. UNSCEAR evaluates radiation science; it does not administer national cleanup programmes. Records remain fragmented across national archives, while affected States may lack the laboratories or source data needed to challenge a source State’s assessment."
        ),
        P(
            "The General Assembly can recommend common reporting, request a Secretary-General repository, convene technical cooperation and encourage assistance. It cannot manufacture compulsory access to classified military sites. Japan’s mechanism is designed accordingly."
        ),
        PageBreak(),
    ]

    # PAGE 2
    story += [
        P("THE PROPOSED MECHANISM", KICKER),
        P("III  |  MONITOR • RESPOND • REMEDIATE", TITLE),
        P("One evidence chain—from historical record to measurable cleanup", SUBTITLE),
    ]

    story.append(
        layer_card(
            "01",
            "MONITOR — VOLUNTARY NUCLEAR LEGACY ENVIRONMENTAL REPORTS",
            [
                "Test dates, broad locations and atmospheric or underground classification.",
                "Declassified meteorological, plume and dose-reconstruction records.",
                "Known or suspected contaminated soil, groundwater, sediment and marine pathways.",
                "Former production facilities, waste categories, cleanup spending and timelines.",
                "Measured data, modelled estimates and unresolved uncertainty labelled separately.",
                "Designs, exact vulnerabilities, operational locations and proliferation-sensitive data protected.",
            ],
            NAVY,
        )
    )
    story.append(
        layer_card(
            "02",
            "RESPOND — AFFECTED-STATE TECHNICAL REVIEW + NOTIFICATION",
            [
                "Affected territorial State may request review voluntarily; no site visit without host consent.",
                "Secretary-General roster draws—within existing mandates—on IAEA, UNSCEAR, CTBTO expertise, regional bodies and qualified laboratories.",
                "Source State invited to provide original records, methods and uncertainty ranges.",
                "Plausible cross-border pathway triggers prompt notification and shared sampling methods.",
                "Notification does not predetermine liability or political attribution.",
            ],
            CRIMSON,
        )
    )
    story.append(
        layer_card(
            "03",
            "REMEDIATE — VOLUNTARY ASSISTANCE + MEASURABLE OUTCOMES",
            [
                "Priority to affected States lacking laboratories and remediation capacity.",
                "Community participation in selecting monitoring and completion indicators.",
                "Risk-based remediation; no assumption that every part of a site is equally dangerous.",
                "Published progress: access restrictions, material secured, environmental trends, health-support coverage and timeline performance.",
                "Assistance never requires an affected State to surrender its legal position.",
            ],
            colors.HexColor("#485F75"),
        )
    )

    story += [P("EVIDENCE-TO-ACTION CONTROL LOGIC", SECTION)]
    control_header = [
        P("FAILURE MODE", ParagraphStyle("CtrlH1", parent=CENTER_SMALL, textColor=WHITE)),
        P("WHAT GOES WRONG", ParagraphStyle("CtrlH2", parent=CENTER_SMALL, textColor=WHITE)),
        P("JAPAN’S CONTROL", ParagraphStyle("CtrlH3", parent=CENTER_SMALL, textColor=WHITE)),
    ]
    control_rows = [
        control_header,
        [P("FRAGMENTED RECORDS", CARD_BODY), P("Incompatible baselines and hidden uncertainty", CARD_BODY), P("MONITOR: common categories + uncertainty labels", CARD_BODY)],
        [P("CONTESTED PATHWAYS", CARD_BODY), P("Warnings delayed by political attribution disputes", CARD_BODY), P("RESPOND: consent-based review + notification", CARD_BODY)],
        [P("UNMEASURED CLEANUP", CARD_BODY), P("Money announced without proof of environmental results", CARD_BODY), P("REMEDIATE: public indicators + community review", CARD_BODY)],
    ]
    control_table = Table(control_rows, colWidths=[CONTENT_W * 0.25, CONTENT_W * 0.36, CONTENT_W * 0.39])
    control_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, MIST]),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#B9C4CF")),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D1D7DD")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story += [
        control_table,
        Spacer(1, 7),
        thesis_box("<font color='#0B1F3A'>NO LAYER SUBSTITUTES FOR ANOTHER.</font><br/>Evidence without response does not protect neighbours; remediation without measurement cannot prove success."),
    ]

    # PAGE 3 — operative translation and implementation map.
    story += [
        PageBreak(),
        P("FROM MECHANISM TO TEXT", KICKER),
        P("IV  |  DRAFT-READY<br/>COMMITTEE RECOMMENDATIONS", TITLE),
        P("Three recommendations the General Assembly can actually adopt", SUBTITLE),
        numbered_recommendation(
            1,
            "<b>Requests</b> the Secretary-General, in consultation with relevant organizations acting within their mandates, to develop a non-binding Nuclear Legacy Environmental Reporting Template and public repository;",
        ),
        Spacer(1, 6),
        numbered_recommendation(
            2,
            "<b>Invites</b> affected States, by consent, to request independent technical review and encourages source States to provide declassified test, plume, dose and production records relevant to environmental assessment;",
        ),
        Spacer(1, 6),
        numbered_recommendation(
            3,
            "<b>Encourages</b> voluntary technical and financial assistance for monitoring, victim support and remediation, with community participation, transparent expenditure and periodic outcome reporting.",
        ),
        Spacer(1, 9),
        P("V  |  IMPLEMENTATION + RESPONSIBILITY MAP", SECTION),
    ]

    role_rows = [
        [P("SECRETARY-GENERAL / UNODA", ParagraphStyle("RoleHead1", parent=CARD_BODY, fontName="DejaVuSans-Bold", textColor=NAVY)), P("Consult on the template; maintain the repository; compile a technical roster; summarize participation without grading political positions.", CARD_BODY)],
        [P("AFFECTED TERRITORIAL STATE", ParagraphStyle("RoleHead2", parent=CARD_BODY, fontName="DejaVuSans-Bold", textColor=NAVY)), P("Controls consent for site access; requests review; nominates community representatives; approves publication of review findings.", CARD_BODY)],
        [P("SOURCE STATE", ParagraphStyle("RoleHead3", parent=CARD_BODY, fontName="DejaVuSans-Bold", textColor=NAVY)), P("Supplies declassified records, methodology, uncertainty ranges and relevant technical experts.", CARD_BODY)],
        [P("TECHNICAL INSTITUTIONS", ParagraphStyle("RoleHead4", parent=CARD_BODY, fontName="DejaVuSans-Bold", textColor=NAVY)), P("Contribute only within existing mandates; distinguish measurement, modelling and unresolved uncertainty.", CARD_BODY)],
        [P("DONORS + COMMUNITIES", ParagraphStyle("RoleHead5", parent=CARD_BODY, fontName="DejaVuSans-Bold", textColor=NAVY)), P("Provide voluntary finance, laboratories, training and local knowledge without controlling scientific conclusions.", CARD_BODY)],
    ]
    role_table = Table(role_rows, colWidths=[50 * mm, CONTENT_W - 50 * mm])
    role_table.setStyle(
        TableStyle(
            [
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, MIST]),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#BAC4CE")),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D1D7DD")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story += [role_table, Spacer(1, 8)]

    sequence = ["COMMON TEMPLATE", "VOLUNTARY REPORT", "STATE REQUEST", "TECHNICAL REVIEW", "REMEDIATION PLAN", "PUBLIC OUTCOMES"]
    seq_cells = []
    for idx, label in enumerate(sequence):
        arrow = "  →" if idx < len(sequence) - 1 else ""
        seq_cells.append(P(label + arrow, ParagraphStyle(f"Seq{idx}", parent=CENTER_SMALL, fontSize=6.7, leading=8.1, textColor=WHITE)))
    seq_table = Table([seq_cells], colWidths=[CONTENT_W / 6] * 6)
    seq_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("BOX", (0, 0), (-1, -1), 0.6, GOLD),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#4B6279")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story += [seq_table, Spacer(1, 9), P("SCOPE + LEGAL SAFEGUARDS", SECTION)]

    shields = [
        "NO compulsory inspections",
        "NO liability determination",
        "NO weapon-design disclosure",
        "NO claim that every test crossed a border",
        "NO claim that every site is uniformly dangerous",
        "NO conflation with accidents or routine civilian operations",
    ]
    shield_cells = [[P(f"• {shields[i]}", SHIELD), P(f"• {shields[i+1]}", SHIELD)] for i in range(0, 6, 2)]
    shield_table = Table(shield_cells, colWidths=[CONTENT_W / 2] * 2)
    shield_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, -1), WHITE),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#49627B")),
                ("BOX", (0, 0), (-1, -1), 0.6, GOLD),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story += [
        shield_table,
        Spacer(1, 8),
        thesis_box(
            "<font color='#BC002D'>RADIATION MUST NOT INHERIT THE SECRECY THAT CREATED IT.</font><br/>Japan asks this committee to establish a common method for documenting inherited contamination, warning affected States and measuring whether remediation actually succeeds."
        ),
        Spacer(1, 5),
        P("Submission doctrine: voluntary • consent-based • source-neutral • evidence-led • community-informed", CENTER_SMALL),
        PageBreak(),
    ]

    # PAGE 4
    story += [
        P("EVIDENCE LEDGER", KICKER),
        P("SOURCES + PRECISION DECLARATIONS", TITLE),
        P("Every load-bearing factual claim is traceable to an official or high-quality record", SUBTITLE),
    ]

    sources = [
        source_row(
            1,
            "United Nations General Assembly — Resolution 79/60",
            "Official recognition that nuclear-use and testing consequences have transcended national borders; victim-assistance and environmental-remediation mandate.",
            "https://documents.un.org/doc/undoc/gen/n24/391/05/pdf/n2439105.pdf",
        ),
        source_row(
            2,
            "US Government Accountability Office — GAO-24-104082",
            "Official US record for 67 Marshall Islands tests and continuing nuclear-waste management questions.",
            "https://www.gao.gov/assets/gao-24-104082.pdf",
        ),
        source_row(
            3,
            "Hiroshima Peace Memorial Museum — Lucky Dragon exhibit",
            "Official Japanese museum record: vessel well outside the danger area; all 23 crew members exposed.",
            "https://hpmmuseum.jp/virtual/VirtualMuseum_e/exhibit_e/exh0307_e/exh03078_e.html",
        ),
        source_row(
            4,
            "International Atomic Energy Agency — Publication 1063",
            "Radiological conditions at the Kazakhstan test site; 456 tests, 116 above ground and site characteristics.",
            "https://www-pub.iaea.org/MTCD/Publications/PDF/Pub1063_web.pdf",
        ),
        source_row(
            5,
            "IAEA International Nuclear Information System",
            "Population-dose reconstruction and record of fallout plumes extending beyond the Kazakhstan test-site boundary.",
            "https://inis.iaea.org/records/ejdbm-x3087",
        ),
        source_row(
            6,
            "US Government Accountability Office — GAO-26-107820",
            "DOE sites contaminated by weapons production and nuclear-energy research; remaining cleanup estimated above half a trillion dollars.",
            "https://www.gao.gov/products/gao-26-107820",
        ),
        source_row(
            7,
            "Comprehensive Nuclear-Test-Ban Treaty Organization",
            "Soviet nuclear-testing history and the International Monitoring System’s test-detection role.",
            "https://www.ctbto.org/nuclear-testing/the-effects-of-nuclear-testing/the-soviet-unions-nuclear-testing-programme/",
        ),
    ]
    source_table = Table(sources, colWidths=[10 * mm, 73 * mm, CONTENT_W - 83 * mm], repeatRows=0)
    source_table.setStyle(
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
    story += [source_table, Spacer(1, 8), P("PRECISION DECLARATIONS", SECTION)]

    precision = [
        "The half-trillion-dollar figure is DOE’s estimate reported by GAO for remaining Environmental Management cleanup; it is not attributed exclusively to current warheads.",
        "‘Beyond the test-site boundary’ is not presented as proof that every Kazakhstan plume crossed an international border.",
        "Lucky Dragon is evidence that fallout exceeded the declared danger area—not a claim about every nuclear test.",
        "All technical participation, information release and site access remain subject to existing mandates, host-State consent and legitimate security protections.",
        "The mechanism distinguishes testing and weapons-production legacies from reactor accidents, routine safeguarded civilian operations and current regulated releases.",
    ]
    for item in precision:
        story.append(P(f"• {item}", BULLET))

    story += [
        Spacer(1, 8),
        thesis_box(
            "<font color='#0B1F3A'>THE STANDARD JAPAN ASKS THE COMMITTEE TO ADOPT:</font><br/><font color='#BC002D'>Disclose the record. Share the warning. Measure the cleanup.</font>"
        ),
    ]
    return story


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = NumberedDocTemplate(str(OUTPUT))
    doc.build(build_story())
    print(OUTPUT)


if __name__ == "__main__":
    main()
