#!/usr/bin/env python3
import os, sys, math
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register fonts
font_dir = '/usr/share/fonts/truetype/dejavu'
pdfmetrics.registerFont(TTFont('DejaVuSans', os.path.join(font_dir, 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', os.path.join(font_dir, 'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSerif', os.path.join(font_dir, 'DejaVuSerif.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSerif-Bold', os.path.join(font_dir, 'DejaVuSerif-Bold.ttf')))

# Color palette matching Sample.pdf & UN aesthetic
NAVY_PRIMARY = colors.HexColor('#0B2E4F')      # #0B2E4F / #12395C
NAVY_SECONDARY = colors.HexColor('#1B5480')    # #1B5480 for section titles
GOLD_ACCENT = colors.HexColor('#C9A227')       # Gold trim
BORDER_RULE = colors.HexColor('#C8D4DE')       # Light slate divider rule
TEXT_DARK = colors.HexColor('#1A1A1A')         # Main body text
TEXT_MUTED = colors.HexColor('#444444')        # Subtitle text
TEXT_LIGHT = colors.HexColor('#666666')        # Metadata text
BG_BOX = colors.HexColor('#F4F7FA')            # Light blue-gray box fill
BG_SIGNATORY = colors.HexColor('#FBF8F0')      # Light warm tint

W, H = A4 # 595.27 x 841.89

def draw_canvas_decorations(canvas, doc):
    canvas.saveState()
    pn = canvas.getPageNumber()
    
    # Outer navy border & inner gold border on all pages
    canvas.setStrokeColor(NAVY_PRIMARY)
    canvas.setLineWidth(1.8)
    canvas.rect(26, 26, W - 52, H - 52, stroke=1, fill=0)
    
    canvas.setStrokeColor(GOLD_ACCENT)
    canvas.setLineWidth(0.75)
    canvas.rect(31, 31, W - 62, H - 62, stroke=1, fill=0)
    
    if pn > 1:
        # Body page top header
        canvas.setFont('DejaVuSans-Bold', 13.5)
        canvas.setFillColor(NAVY_PRIMARY)
        canvas.drawString(46, H - 56, "Draft Resolution 1.1")
        
        # Header double rules matching Sample.pdf
        canvas.setStrokeColor(NAVY_PRIMARY)
        canvas.setLineWidth(1.15)
        canvas.line(46, H - 64, W - 46, H - 64)
        
        canvas.setStrokeColor(BORDER_RULE)
        canvas.setLineWidth(0.6)
        canvas.line(46, H - 68, W - 46, H - 68)
        
        # Footer rule & text
        canvas.setStrokeColor(BORDER_RULE)
        canvas.setLineWidth(0.6)
        canvas.line(46, 50, W - 46, 50)
        
        canvas.setFont('DejaVuSans', 8.0)
        canvas.setFillColor(TEXT_LIGHT)
        body_page = pn - 1
        canvas.drawString(46, 38, f"{body_page} of 3")
        canvas.drawRightString(W - 46, 38, "Draft Resolution 1.1 — UNGA, CCA MUN 2026")
        
    canvas.restoreState()

def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=46,
        rightMargin=46,
        topMargin=76,
        bottomMargin=58,
        title="Draft Resolution 1.1 — VANGUARD",
        author="Delegation of Japan on behalf of VANGUARD Bloc"
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        fontName='DejaVuSans-Bold',
        fontSize=18.5,
        leading=22,
        textColor=NAVY_PRIMARY,
        alignment=TA_CENTER
    )
    
    sub_style = ParagraphStyle(
        'CoverSub',
        fontName='DejaVuSans',
        fontSize=9.8,
        leading=13.5,
        textColor=TEXT_MUTED,
        alignment=TA_CENTER
    )
    
    conf_style = ParagraphStyle(
        'CoverConf',
        fontName='DejaVuSans',
        fontSize=8.6,
        leading=11.5,
        textColor=TEXT_LIGHT,
        alignment=TA_CENTER
    )
    
    sec_header_style = ParagraphStyle(
        'CoverSecHead',
        fontName='DejaVuSans-Bold',
        fontSize=8.2,
        leading=10.5,
        textColor=NAVY_PRIMARY,
        alignment=TA_LEFT
    )
    
    names_style = ParagraphStyle(
        'CoverNames',
        fontName='DejaVuSerif',
        fontSize=7.8,
        leading=11.2,
        textColor=TEXT_DARK,
        alignment=TA_LEFT
    )
    
    stats_style = ParagraphStyle(
        'CoverStats',
        fontName='DejaVuSans',
        fontSize=7.6,
        leading=10,
        textColor=TEXT_LIGHT,
        alignment=TA_CENTER
    )
    
    ga_heading_style = ParagraphStyle(
        'GAHeading',
        fontName='DejaVuSans-Bold',
        fontSize=10.4,
        leading=13.5,
        textColor=NAVY_SECONDARY,
        spaceBefore=4,
        spaceAfter=6
    )
    
    pp_style = ParagraphStyle(
        'PPStyle',
        fontName='DejaVuSerif',
        fontSize=8.1,
        leading=11.4,
        textColor=TEXT_DARK,
        alignment=TA_JUSTIFY,
        spaceBefore=2.5,
        spaceAfter=2.5,
        leftIndent=0,
        firstLineIndent=0
    )
    
    op_sec_style = ParagraphStyle(
        'OPSecStyle',
        fontName='DejaVuSans-Bold',
        fontSize=8.8,
        leading=12,
        textColor=NAVY_PRIMARY,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )
    
    op_style = ParagraphStyle(
        'OPStyle',
        fontName='DejaVuSerif',
        fontSize=8.1,
        leading=11.4,
        textColor=TEXT_DARK,
        alignment=TA_JUSTIFY,
        spaceBefore=3.5,
        spaceAfter=3.5,
        leftIndent=14,
        firstLineIndent=-14
    )
    
    closing_title_style = ParagraphStyle(
        'ClosingTitle',
        fontName='DejaVuSans-Bold',
        fontSize=8.5,
        leading=11,
        textColor=NAVY_PRIMARY,
        alignment=TA_CENTER
    )
    
    closing_text_style = ParagraphStyle(
        'ClosingText',
        fontName='DejaVuSans',
        fontSize=7.5,
        leading=10.5,
        textColor=TEXT_MUTED,
        alignment=TA_CENTER
    )

    story = []

    # ==================== PAGE 1: COVER PAGE ====================
    story.append(Spacer(1, 10))
    
    # Center Logo Emblem
    logo_path = '/home/user/CCA-Mun/assets/vanguard_logo_final.png'
    if os.path.exists(logo_path):
        logo_img = Image(logo_path, width=105, height=105)
        logo_img.hAlign = 'CENTER'
        story.append(logo_img)
        story.append(Spacer(1, 10))
    else:
        story.append(Spacer(1, 25))
        
    story.append(Paragraph("Draft Resolution 1.1", title_style))
    story.append(Spacer(1, 7))
    story.append(Paragraph("United Nations General Assembly", sub_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Assessing the Ecological Threats of Nuclear Proliferation on Global Boundaries", sub_style))
    story.append(Spacer(1, 7))
    story.append(Paragraph("CCA MUN 2026  •  21–22 August 2026", conf_style))
    story.append(Spacer(1, 14))

    # Sponsors Box Table (10 confirmed bloc members)
    sponsors_content = [
        [Paragraph("SPONSORS (10)", sec_header_style)],
        [Paragraph("<b>Japan</b>  ·  <b>Mexico</b>  ·  <b>Canada</b>  ·  <b>India</b>  ·  <b>Iran</b>  ·  <b>Switzerland</b>  ·  <b>Egypt</b>  ·  <b>Philippines</b>  ·  <b>Barbados</b>  ·  <b>South Africa</b>", names_style)]
    ]
    sponsors_table = Table(sponsors_content, colWidths=[W - 92])
    sponsors_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_BOX),
        ('BOX', (0,0), (-1,-1), 1.0, GOLD_ACCENT),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(sponsors_table)
    story.append(Spacer(1, 9))

    # Signatories Box Table (5 target members)
    signatories_content = [
        [Paragraph("SIGNATORIES (5)", sec_header_style)],
        [Paragraph("<b>Norway</b>  ·  <b>Germany</b>  ·  <b>Republic of Korea</b>  ·  <b>Singapore</b>  ·  <b>New Zealand</b>", names_style)]
    ]
    signatories_table = Table(signatories_content, colWidths=[W - 92])
    signatories_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_SIGNATORY),
        ('BOX', (0,0), (-1,-1), 0.75, BORDER_RULE),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(signatories_table)
    story.append(Spacer(1, 14))

    # Stats Summary Line
    story.append(Paragraph("15 delegations across six global regions  |  17 operative clauses  |  VANGUARD Framework", stats_style))
    story.append(PageBreak())

    # ==================== PAGE 2: PREAMBLE ====================
    story.append(Paragraph("THE GENERAL ASSEMBLY,", ga_heading_style))
    story.append(Spacer(1, 2))

    preambles = [
        ("PP1", "<i>Guided by</i> the purposes and principles of the Charter of the United Nations, including the promotion of international cooperation in solving international problems of an economic, social, cultural and humanitarian character,"),
        ("PP2", "<i>Recalling</i> that the global environment respects no political boundaries, and that radiological contamination, once introduced into the atmosphere, oceans, soil, or groundwater, constitutes a shared and enduring hazard to all humankind,"),
        ("PP3", "<i>Recalling</i> its resolutions 78/240 of 22 December 2023, 79/60 of 2 December 2024, and 80/56 of 2 December 2025 on addressing the legacy of nuclear weapons: providing victim assistance and environmental remediation to Member States affected by the use or testing of nuclear weapons, and <i>welcoming</i> the convening of the first International Meeting on Victim Assistance and Environmental Remediation on 1 September 2026,"),
        ("PP4", "<i>Noting</i> the thirtieth anniversary of the opening for signature of the Comprehensive Nuclear-Test-Ban Treaty on 24 September 2026, and <i>recognizing</i> the indispensable contribution of the International Monitoring System to environmental radiation detection, verification and global boundary security,"),
        ("PP5", "<i>Reaffirming</i> the central statutory role of the International Atomic Energy Agency (IAEA) in establishing global nuclear safety and radiation-protection standards, and <i>recalling</i> the Convention on Early Notification of a Nuclear Accident (1986) and the Convention on Assistance in the Case of a Nuclear Accident or Radiological Emergency (1986),"),
        ("PP6", "<i>Taking note with appreciation</i> of the establishment of the independent 21-member United Nations Scientific Panel on the Effects of Nuclear War pursuant to General Assembly resolution 79/238, and <i>anticipating</i> its comprehensive 2027 report examining the physical, climatic, ecological and agricultural consequences of nuclear detonations,"),
        ("PP7", "<i>Recalling</i> existing international legal instruments relevant to nuclear weapons — including the Treaty on the Non-Proliferation of Nuclear Weapons and the Treaty on the Prohibition of Nuclear Weapons — <b>for their respective States parties</b>, without prejudice to the sovereign national security policies or legal positions of any State,"),
        ("PP8", "<i>Emphasizing</i> that the present resolution addresses transboundary ecological threats arising from the development, testing, production, proliferation and legacy of nuclear weapons and their associated facilities, while <i>noting</i> that civilian operational releases conducted in full compliance with established IAEA safety standards and independent verification remain under their respective regulatory frameworks,"),
        ("PP9", "<i>Mindful</i> of the profound humanitarian and ecological legacies of Hiroshima and Nagasaki on their eighty-first anniversaries, of Semipalatinsk, the Marshall Islands, Moruroa, Fangataufa, Lop Nor, Maralinga, Novaya Zemlya, and all global testing grounds, and of affected indigenous, downwind and coastal communities whose testimony anchors this framework,"),
        ("PP10", "<i>Recognizing</i> the heightened ecological vulnerability of coastal, archipelagic, small island developing States (SIDS), and landlocked legacy-affected developing States, and their acute need for early warning, real-time data access, and international capacity-building,"),
        ("PP11", "<i>Recognizing also</i> the value of drawing upon the world's only decade-long, large-scale post-accident environmental remediation experience, which demonstrates that scientifically guided, multi-tiered ecological recovery and transparent monitoring are achievable,"),
        ("PP12", "<i>Reaffirming</i> the enduring commitment of Member States to multilateral diplomacy, nuclear non-proliferation, arms control, and the shared global vision of a world free from nuclear weapons,"),
        ("PP13", "<i>Recalling</i> the resolutions of the General Conference of the International Atomic Energy Agency, including GC(XXIX)/RES/444 of 1985 and GC(XXXIV)/RES/533 of 1990, affirming that any armed attack on and threat against nuclear facilities devoted to peaceful purposes constitutes a violation of the principles of the Charter of the United Nations, international law and the Statute of the Agency,"),
        ("PP14", "<i>Recognizing</i> the vital role of international scientific cooperation, including through the IAEA and regional technical centres, in strengthening the capacity of all States to detect, assess and mitigate transboundary radiological risks, and its contribution to transparency and mutual confidence among nations,")
    ]

    for label, pp_text in preambles:
        story.append(Paragraph(pp_text, pp_style))

    story.append(PageBreak())

    # ==================== PAGES 3 & 4: OPERATIVE CLAUSES ====================
    story.append(Paragraph("OPERATIVE CLAUSES", ga_heading_style))
    story.append(Spacer(1, 2))

    sections = [
        ("I. Definition and Framework", [
            ("1.", "<i>Decides to establish</i> the <b>Global Framework for Nuclear-Ecological Monitoring, Response and Remediation</b> (\"the Framework\"), operating in close partnership with existing international mechanisms — including the International Atomic Energy Agency, the United Nations Environment Programme (UNEP), the Preparatory Commission for the Comprehensive Nuclear-Test-Ban Treaty Organization (CTBTO), and relevant regional bodies — without creating duplicative administrative organs, and <i>requests</i> the Secretary-General to transmit a progress report on its initial implementation to the General Assembly at its eighty-second session;"),
            ("2.", "<i>Calls upon</i> Member States to collaborate toward the harmonization of international standards for environmental radiation monitoring and reporting across air, marine, terrestrial, and agricultural vectors, and <i>invites</i> the IAEA to serve as the international technical reference point and benchmark for data quality, verification and comparability;")
        ]),
        ("II. Environmental Radiation Monitoring and Early Warning", [
            ("3.", "<i>Encourages</i> Member States, in cooperation with the IAEA, the CTBTO and relevant regional organizations, to establish and strengthen interoperable regional environmental-radiation monitoring networks for continuous detection of transboundary radiological contamination across marine, atmospheric and terrestrial ecosystems, with data-sharing protocols that fully respect national sovereignty and applicable international obligations;"),
            ("4.", "<i>Encourages</i> Member States to designate national emergency contact points and strengthen rapid-notification mechanisms for nuclear or radiological incidents with potential transboundary ecological consequences, building upon and operationalizing the Convention on Early Notification of a Nuclear Accident (1986);"),
            ("7A.", "<i>Encourages</i> enhanced cooperation with the International Atomic Energy Agency to strengthen environmental radiation monitoring, rapid detection capabilities, and nuclear waste verification mechanisms, building upon the Agency's established technical cooperation programmes and safety standards;")
        ]),
        ("III. Capacity Building and Technical Cooperation", [
            ("5.", "<i>Calls upon</i> technologically and financially capable Member States, relevant United Nations entities, and international financial institutions to provide voluntary technical assistance, capacity-building, equipment, and technology transfer to developing, archipelagic, and small island developing States for radiation detection, environmental baseline assessment, emergency preparedness, and ecosystem remediation, including through voluntary South–South and triangular cooperation programmes;"),
            ("15.", "<i>Encourages</i> Member States pursuing or operating civilian nuclear programmes, in particular newcomer States, to establish and strengthen independent national radiation-monitoring institutions, robust regulatory frameworks, and rapid emergency-response capacities, and <i>invites</i> experienced States and international organizations to support such efforts through bilateral and regional partnerships;")
        ]),
        ("IV. Transboundary Environmental Impact Assessments", [
            ("6.", "<i>Encourages</i> Member States to conduct comprehensive, transparent environmental impact assessments (EIAs) prior to undertaking nuclear-related activities with demonstrable potential for transboundary ecological consequences, and to consult in good faith with potentially affected neighbouring and coastal States to mitigate cross-border radiological hazards;")
        ]),
        ("V. Radioactive Waste Management", [
            ("7.", "<i>Calls upon</i> Member States to establish comprehensive, responsible life-cycle radioactive waste management strategies, prioritizing deep geological disposal, transparent and consent-based community siting frameworks, and dedicated owner-funded financing mechanisms to ensure long-term containment and environmental safety;")
        ]),
        ("VI. Verification and Independent Assessment", [
            ("8.", "<i>Encourages</i> the establishment, under relevant United Nations bodies and the IAEA, of a voluntary multilateral facility for independent assessment, scientific verification, and public reporting of significant transboundary ecological risks arising from legacy nuclear activities, while providing appropriate safeguards for legitimate national security and proprietary data;"),
            ("9A.", "<i>Encourages</i> voluntary cooperation with the IAEA for environmental radiation monitoring along international boundaries and at historical legacy test sites, conducted strictly with the prior consent of the States concerned;")
        ]),
        ("VII. Ecological Remediation and Assistance", [
            ("9.", "<i>Encourages</i> the establishment, through UNEP and the IAEA, of a voluntary International Radiological Damage and Ecological Remediation Fund to support affected States in long-term environmental remediation, ecosystem recovery, soil and water decontamination, and health monitoring, with voluntary contributions from States in a position to do so, including States whose past nuclear activities have contributed to transboundary contamination;"),
            ("11.", "<i>Encourages</i> Member States, international organizations, and civil society to implement voluntary cooperative programmes for the long-term ecological restoration of ecosystems affected by radioactive contamination, including joint scientific assessments, marine and agricultural monitoring, and targeted assistance for affected indigenous peoples, downwind populations, and vulnerable island communities;"),
            ("12.", "<i>Welcomes</i> the convening of the International Meeting on Victim Assistance and Environmental Remediation on 1 September 2026 pursuant to General Assembly resolution 80/56, <i>calls upon</i> Member States to participate constructively, and <i>invites</i> voluntary contributions to support international remediation cooperation and victim assistance frameworks;"),
            ("14.", "<i>Calls upon</i> Member States to expand international technical cooperation for the remediation of contaminated land, river basins, and maritime zones, facilitating the exchange of proven decontamination technologies and environmental management best practices;")
        ]),
        ("VIII. Facility Protection and Security in Armed Conflict", [
            ("13.", "<i>Reaffirms</i> that any armed attack on and threat against nuclear facilities devoted to peaceful purposes constitutes a violation of the principles of the Charter of the United Nations, international law and the Statute of the International Atomic Energy Agency, and that armed attacks on nuclear facilities could result in radioactive releases with grave consequences within and beyond the boundaries of the State which has been attacked, <i>calls upon</i> all States to refrain from such attacks and threats and to respect applicable international law, and <i>invites</i> the IAEA Director General to continue providing factual reporting on the nuclear safety, security and safeguards situation at safeguarded sites affected by military activities, including any radiological or environmental implications;"),
            ("13A.", "<i>Calls upon</i> all States to cooperate fully with the International Atomic Energy Agency in the exercise of its statutory safeguards functions, <i>encourages</i> the restoration and strengthening of Agency access to nuclear material and facilities subject to safeguards in accordance with applicable safeguards agreements, and <i>invites</i> regular Agency reporting to its Board of Governors and the General Conference;")
        ]),
        ("IX. Regional Security and Peaceful Uses", [
            ("9B.", "<i>Recalls</i> the historic contribution of nuclear-weapon-free zones, including the pioneering Treaty of Tlatelolco, to regional environmental protection, nuclear non-proliferation, and global security, and <i>encourages</i> States parties to existing NWFZ treaties to continue sharing environmental monitoring and verification best practices;"),
            ("16.", "<i>Reaffirms</i> the inalienable right of all States parties to the Treaty on the Non-Proliferation of Nuclear Weapons to develop research, production and use of nuclear energy for peaceful purposes without discrimination and in conformity with Articles I, II, and III of the Treaty, and <i>encourages</i> international scientific cooperation under IAEA safeguards;")
        ]),
        ("X. Review and Follow-Through", [
            ("17.", "<i>Decides</i> to remain seized of the matter, and <i>requests</i> the Secretary-General to submit to the General Assembly at its eighty-third session a consolidated report on the implementation of the present resolution, prepared in consultation with the IAEA, UNEP, and relevant regional partner organizations.")
        ])
    ]

    for sec_title, clauses in sections:
        story.append(Paragraph(sec_title, op_sec_style))
        for num, text in clauses:
            p_text = f"<b>{num}</b> {text}"
            story.append(Paragraph(p_text, op_style))

    # Closing Submission Box on Page 4
    story.append(Spacer(1, 14))
    closing_content = [
        [Paragraph("— END OF DRAFT RESOLUTION 1.1 —", closing_title_style)],
        [Paragraph("Submitted by the Delegation of <b>Japan</b> on behalf of the <b>VANGUARD Bloc</b><br/><b>Co-Sponsors (10):</b> Japan · Mexico · Canada · India · Iran · Switzerland · Egypt · Philippines · Barbados · South Africa<br/><b>Target Signatories (5):</b> Norway · Germany · Republic of Korea · Singapore · New Zealand<br/><i>United Nations General Assembly  •  CCA MUN 2026</i>", closing_text_style)]
    ]
    closing_table = Table(closing_content, colWidths=[W - 92])
    closing_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_BOX),
        ('BOX', (0,0), (-1,-1), 1.0, GOLD_ACCENT),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(closing_table)

    doc.build(story, onFirstPage=draw_canvas_decorations, onLaterPages=draw_canvas_decorations)
    print(f"Generated {output_path} successfully ({os.path.getsize(output_path)} bytes)")

if __name__ == '__main__':
    out1 = '/home/user/CCA-Mun/drafts/VANGUARD_DR1.1.pdf'
    out2 = '/home/user/CCA-Mun/drafts/Working_Paper_1.1.pdf'
    build_pdf(out1)
    build_pdf(out2)
