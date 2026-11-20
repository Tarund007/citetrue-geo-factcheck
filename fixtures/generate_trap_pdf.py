"""
Generates the fixtures/trap_document.pdf using ReportLab.
Contains a balanced distribution of:
- 3 Verified facts
- 3 Inaccurate / Outdated facts
- 2 Blatantly False / Fabricated facts
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def build_pdf():
    fixtures_dir = os.path.join(os.path.dirname(__file__))
    pdf_path = os.path.join(fixtures_dir, "trap_document.pdf")
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#111111'),
        spaceAfter=12
    )
    
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#666666'),
        spaceAfter=18
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=16,
        textColor=colors.HexColor('#222222'),
        spaceAfter=12
    )
    
    story = []
    
    # Header
    story.append(Paragraph("Enterprise Market Analysis & Technology Audit (2025/2026)", title_style))
    story.append(Paragraph("Published by Global Insights Research Group | Assessment Test Artifact", meta_style))
    story.append(Spacer(1, 10))
    
    # Paragraph 1
    story.append(Paragraph("<b>Section 1: AI & Tech Ecosystem Growth</b>", styles['Heading3']))
    story.append(Paragraph(
        "OpenAI was founded in December 2015 as a non-profit artificial intelligence research laboratory in San Francisco, California. "
        "Over the subsequent decade, generative AI became central to mobile hardware and enterprise search. "
        "For instance, Apple released the iPhone 16 series in September 2024 powered by the A18 and A18 Pro Bionic chips.",
        body_style
    ))
    
    # Paragraph 2
    story.append(Paragraph("<b>Section 2: Indian Tech & Quick-Commerce Capital Markets</b>", styles['Heading3']))
    story.append(Paragraph(
        "India's consumer tech sector experienced massive consolidation. "
        "In 2022, Zomato acquired quick-commerce platform Blinkit for $1.8 billion in an all-stock deal. "
        "Meanwhile, competitor Swiggy is currently planning its initial public offering (IPO) scheduled for late 2026.",
        body_style
    ))
    
    # Paragraph 3
    story.append(Paragraph("<b>Section 3: Regional Corporate Infrastructure & Fintech</b>", styles['Heading3']))
    story.append(Paragraph(
        "DLF Cyber City is an integrated commercial technology business district located in Gurugram, Haryana. "
        "Fintech infrastructure also scaled rapidly across the country; for example, Cashfree Payments was founded in 2021 by Akash Gehani and Reeju Datta in Bengaluru.",
        body_style
    ))
    
    # Paragraph 4
    story.append(Paragraph("<b>Section 4: Healthcare & Global Conglomerates</b>", styles['Heading3']))
    story.append(Paragraph(
        "Apollo Hospitals operates over 120,000 hospital beds across 45 countries worldwide as of 2024, setting a historic benchmark for private medical delivery. "
        "In international consumer FMCG, Satya Nadella has served as the Chairman and Chief Executive Officer of PepsiCo since 2018.",
        body_style
    ))
    
    doc.build(story)
    print(f"Trap PDF successfully generated at: {pdf_path}")

if __name__ == "__main__":
    build_pdf()
