#!/usr/bin/env python3
"""Build the handwritten-ready PDF for Japan's third substantive chit."""

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
OUTPUT = ROOT / "substantive_chits" / "SUBSTANTIVE_CHIT_3.pdf"

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
    footer = "SUBSTANTIVE CHIT 03  |  SHIELD STANDARD • HANDWRITTEN"
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
            title="Substantive Chit 03 — The Narrow Shield",
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
    story=[]

    def source_table(rows):
        t=Table(rows,colWidths=[13*mm,70*mm,CONTENT_W-83*mm])
        t.setStyle(TableStyle([
            ("VALIGN",(0,0),(-1,-1),"TOP"),("ROWBACKGROUNDS",(0,0),(-1,-1),[WHITE,MIST]),
            ("BOX",(0,0),(-1,-1),.6,colors.HexColor("#B9C4CF")),("INNERGRID",(0,0),(-1,-1),.3,colors.HexColor("#D1D7DD")),
            ("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ])); return t

    def metadata():
        t=Table([
            [P("DELEGATION",META_HEADER),P("COMMITTEE",META_HEADER),P("MODERATED-CAUCUS FOCUS",META_HEADER)],
            [P("JAPAN",ParagraphStyle("C3M1",parent=FACT_LABEL,fontSize=9.2)),P("UN GENERAL ASSEMBLY",ParagraphStyle("C3M2",parent=FACT_LABEL,fontSize=9.2)),P("NATIONAL SECURITY + ENVIRONMENTAL PROTECTION",ParagraphStyle("C3M3",parent=FACT_LABEL,fontSize=7.7))],
        ],colWidths=[CONTENT_W*.22,CONTENT_W*.28,CONTENT_W*.50])
        t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("BACKGROUND",(0,1),(-1,1),WHITE),("BOX",(0,0),(-1,-1),.6,NAVY),("INNERGRID",(0,0),(-1,-1),.35,colors.HexColor("#C8D0D8")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
        return t

    # PAGE 1 — exact handwritten submission, part I.
    story += [
        P("SUBSTANTIVE CHIT 03  /  HANDWRITTEN SUBMISSION  /  COPY PART I",KICKER),
        P("THE NARROW SHIELD",TITLE),
        P("A Security–Ecology Proportionality Standard for Nuclear Policy",SUBTITLE),
        metadata(),Spacer(1,7),
        thesis_box("<font color='#BC002D'>COPY PAGES 1–2 AS THE SUBMISSION.</font><br/>National security may protect an operation; it must not erase accountability for ecological consequences."),
        Spacer(1,8),
        P("EXACT HANDWRITTEN TEXT  |  PART I",SECTION),
        P("National security can justify protecting an operation; it cannot justify hiding every ecological consequence of that operation. Japan therefore proposes a <b>Narrow Security Exception for Nuclear Environmental Accountability</b>, expressed through the <b>SHIELD Standard</b>."),
        P("The legal balance already exists in principle. In its 1996 Nuclear Weapons Advisory Opinion, the International Court of Justice held that environmental obligations were not intended to deprive a State of self-defence, but that environmental considerations must still inform what is necessary and proportionate in pursuit of legitimate military objectives.<super>[1]</super> The General Assembly later took note of the International Law Commission’s principles on protecting the environment before, during and after armed conflict, including prevention, mitigation and remediation.<super>[2]</super>"),
        P("Japan’s SHIELD Standard asks six questions whenever a State invokes national security to withhold nuclear-environmental information:",BODY),
    ]
    shield_rows=[
        ("S","SPECIFIC SECURITY HARM","Has the State identified the category of security harm that disclosure would create, without being required to reveal the secret itself?"),
        ("H","HARM BEYOND BORDERS","Has it assessed plausible effects on neighbouring States, shared waters, food chains and future generations?"),
        ("I","INFORMATION MINIMIZED, NOT ERASED","Could aggregate, delayed, redacted or protected-channel disclosure address the risk?"),
        ("E","EMERGENCY WARNING PRESERVED","Are monitoring, regulator communication and rapid notification guaranteed when significant radiological consequences may cross borders?"),
        ("L","LIFECYCLE LIABILITIES REPORTED","Are waste, contaminated sites, decommissioning and remediation obligations visible even when operational details remain classified?"),
        ("D","DECISION INDEPENDENTLY REVIEWED","Is the secrecy claim examined by an independent national authority or agreed technical process and reconsidered periodically?"),
    ]
    cells=[]
    for letter,label,question in shield_rows:
        cells.append([P(letter,ParagraphStyle(f"ShieldLetter{letter}",parent=FACT_NUMBER,textColor=WHITE,fontSize=13,leading=14)),P(f"<b>{label}</b><br/>{question}",CARD_BODY)])
    shield_table=Table(cells,colWidths=[12*mm,CONTENT_W-12*mm])
    shield_table.setStyle(TableStyle([("BACKGROUND",(0,0),(0,-1),CRIMSON),("ROWBACKGROUNDS",(1,0),(1,-1),[WHITE,MIST]),("BOX",(0,0),(-1,-1),.65,colors.HexColor("#C5AAB1")),("INNERGRID",(0,0),(-1,-1),.3,colors.HexColor("#D1D7DD")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    story += [shield_table,Spacer(1,7),P("CONTINUE DIRECTLY TO PAGE 2  →",ParagraphStyle("Continue",parent=KICKER,alignment=TA_CENTER,fontSize=8.2)),PageBreak()]

    # PAGE 2 — exact handwritten submission, part II.
    story += [
        P("SUBSTANTIVE CHIT 03  /  HANDWRITTEN SUBMISSION  /  COPY PART II",KICKER),
        P("THE NARROW SHIELD  /  CONTINUED",TITLE),
        P("Exact handwritten text • continue without adding a second heading",SUBTITLE),
        P("EXACT HANDWRITTEN TEXT  |  PART II",SECTION),
        P("The standard is practical. The IAEA’s Seven Indispensable Pillars and Five Concrete Principles show that armed conflict does not suspend nuclear safety: physical integrity, power, monitoring, staff capacity, logistics and regulator communication remain essential.<super>[3]</super> The Early Notification Convention separately demonstrates that rapid information exchange can protect other States when a covered nuclear accident may cause a significant transboundary release.<super>[4]</super> Japan does not claim that this Convention automatically governs every military activity; it adopts the underlying design principle that warning must not wait for political attribution."),
        P("Technical protection is also possible. The UK–Norway Initiative tested managed access and information barriers designed to verify nuclear-warhead dismantlement without revealing national-security or proliferation-sensitive information.<super>[5]</super> Security and accountability are therefore not binary choices."),
        P("Japan recommends that this committee:",BODY),
    ]
    recs=[
        "<b>endorses</b> the SHIELD Standard as a voluntary test for nuclear-security exceptions;",
        "<b>encourages</b> dual environmental assessments: a protected technical assessment and a public aggregate summary;",
        "<b>calls for</b> independent review, regional warning channels and periodic reporting across the nuclear-policy lifecycle—before deployment decisions, during operation and after retirement or decommissioning.",
    ]
    for i,x in enumerate(recs,1): story += [numbered_recommendation(i,x),Spacer(1,6)]
    story += [
        Spacer(1,6),
        thesis_box("<font color='#BC002D'>THE GOVERNING RULE IS NARROW AND DEFENSIBLE:</font><br/><font color='#0B1F3A'>Classify the operation, not the consequence; protect the secret, not the pollution.</font>"),
        Spacer(1,10),
        P("HANDWRITING CHECKLIST",SECTION),
    ]
    checklist=[
        "Write the inline source numbers [1]–[5].",
        "Do not add country accusations unless responding to the live debate.",
        "Keep the bold final line as the final sentence.",
        "If space is short, remove the ILC sentence—not the SHIELD test or recommendations.",
    ]
    check_table=Table([[P("• "+x,CARD_BODY)] for x in checklist],colWidths=[CONTENT_W])
    check_table.setStyle(TableStyle([("ROWBACKGROUNDS",(0,0),(-1,-1),[WHITE,MIST]),("BOX",(0,0),(-1,-1),.5,colors.HexColor("#BBC5CF")),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),8)]))
    story += [check_table,Spacer(1,8),P("END OF TEXT TO HANDWRITE",ParagraphStyle("EndCopy",parent=KICKER,alignment=TA_CENTER,fontSize=8.3)),PageBreak()]

    # PAGE 3 — supporting architecture, not mandatory to copy.
    story += [
        P("RESEARCH SUPPORT  /  DO NOT COPY UNLESS SPACE PERMITS",KICKER),
        P("THE POLICY LIFECYCLE",TITLE),
        P("The SHIELD Standard applied before, during and after a security-sensitive nuclear policy",SUBTITLE),
        layer_card("01","BEFORE — ANTICIPATE",[
            "Conduct a security-screened environmental risk assessment.",
            "Identify plausible transboundary pathways and emergency contacts.",
            "Separate public aggregate findings from a protected technical annex.",
            "Establish responsibility for later decommissioning and remediation.",
        ],NAVY),
        layer_card("02","DURING — MONITOR + WARN",[
            "Maintain independent regulatory communication and environmental monitoring.",
            "Preserve facility staffing, power, cooling, logistics and emergency preparedness.",
            "Notify potentially affected States when significant cross-border harm is plausible.",
            "Use protected technical channels before withholding information entirely.",
        ],CRIMSON),
        layer_card("03","AFTER — ACCOUNT + REMEDIATE",[
            "Report aggregate waste, contaminated sites, decommissioning progress and liabilities.",
            "Review whether continued secrecy remains necessary.",
            "Include affected communities in remediation indicators and outcome review.",
            "Preserve records needed for long-term health and environmental assessment.",
        ],colors.HexColor("#485F75")),
        P("DRAFT-READY LANGUAGE",SECTION),
        numbered_recommendation(1,"<b>Recommends</b> the voluntary SHIELD Standard—specificity, transboundary-harm assessment, least-restrictive disclosure, preserved warning, lifecycle reporting and independent review—for evaluating national-security exceptions;"),
        Spacer(1,5),
        numbered_recommendation(2,"<b>Encourages</b> a protected technical environmental assessment and a public aggregate summary for security-sensitive nuclear policies and facilities;"),
        Spacer(1,5),
        numbered_recommendation(3,"<b>Calls upon</b> States to maintain independent regulation, regional warning, record preservation and periodic environmental reporting across the full nuclear-policy lifecycle."),
        Spacer(1,8),
        P("LIVE CUSTOMIZATION",SECTION),
        thesis_box("Add one opening sentence only if it reflects the room:<br/><font color='#BC002D'>“The debate has treated national security as [a blanket exemption / an illegitimate concern]; Japan submits that neither extreme is technically or legally defensible.”</font>"),
        Spacer(1,7),
        P("SCOPE SAFEGUARDS",SECTION),
    ]
    scope=["NO compelled classified disclosure","NO weakening of self-defence rights","NO judgment on deterrence legality","NO new inspection authority","NO weapon design or location disclosure","NO automatic extension of civilian conventions"]
    sc=[[P("• "+scope[i],SHIELD),P("• "+scope[i+1],SHIELD)] for i in range(0,6,2)]
    st=Table(sc,colWidths=[CONTENT_W/2]*2)
    st.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),NAVY),("BOX",(0,0),(-1,-1),.6,GOLD),("INNERGRID",(0,0),(-1,-1),.35,colors.HexColor("#49627B")),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
    story += [st,PageBreak()]

    # PAGE 4 — sources and precision.
    story += [
        P("EVIDENCE LEDGER",KICKER),
        P("SOURCES + PRECISION DECLARATIONS",TITLE),
        P("Six official or high-quality records supporting the handwritten submission",SUBTITLE),
    ]
    sources=[
        source_row(1,"International Court of Justice — Advisory Opinion, 8 July 1996","Environment, self-defence, necessity and proportionality in the Nuclear Weapons Advisory Opinion.","https://www.icj-cij.org/index.php/node/103787"),
        source_row(2,"UN General Assembly / International Law Commission — Resolution 77/104","Principles addressing protection before, during and after conflict, including prevention, mitigation and remediation.","https://legal.un.org/ilc/texts/instruments/english/draft_articles/8_7_2022.pdf"),
        source_row(3,"International Atomic Energy Agency — Seven Pillars + Five Principles","Nuclear safety and security during armed conflict; physical integrity, systems, staff, power, logistics, monitoring and communication.","https://www.iaea.org/publications/reports/annual-report/2023/in-focus/nuclear-safety-security-and-safeguards-in-ukraine"),
        source_row(4,"IAEA — Convention on Early Notification of a Nuclear Accident","Notification where a covered accident may produce an internationally significant transboundary radiological release.","https://www.iaea.org/topics/nuclear-safety-conventions/convention-early-notification-nuclear-accident"),
        source_row(5,"United Kingdom–Norway Initiative — NPT working paper","Managed access and information barriers protecting national-security and proliferation-sensitive information during verification research.","https://assets.publishing.service.gov.uk/media/5a79015fed915d04220670ca/npt_revcon_2010_jwp.pdf"),
        source_row(6,"UN General Assembly — Resolution 47/37","Compliance with environmental law applicable in armed conflict and incorporation into military manuals.","https://digitallibrary.un.org/record/158808?ln=en"),
    ]
    story += [source_table(sources),Spacer(1,9),P("PRECISION DECLARATIONS",SECTION)]
    precision=[
        "The ICJ did not hold that environmental law abolishes self-defence; the submission states the Court’s balance.",
        "Resolution 77/104 took note of ILC draft principles; it did not transform every principle into a universally binding treaty rule.",
        "The IAEA pillars and principles are policy evidence, not a universal enforcement mandate.",
        "The Early Notification Convention is used as a design precedent; automatic extension to every military activity is expressly rejected.",
        "The UK–Norway Initiative concerned research and exercises, not a binding universal inspection regime.",
    ]
    for x in precision: story.append(P("• "+x,BULLET))
    story += [Spacer(1,9),thesis_box("<font color='#0B1F3A'>JAPAN’S BALANCE:</font><br/><font color='#BC002D'>Specific secrecy. Minimum necessary withholding. Non-negotiable environmental warning.</font>")]
    return story

def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = NumberedDocTemplate(str(OUTPUT))
    doc.build(build_story())
    print(OUTPUT)


if __name__ == "__main__":
    main()
