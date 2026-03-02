"""
PDF generation utilities for creating travel itinerary PDFs
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
from config import WEATHER_ICONS


# =========================
# WEATHER ICONS
# =========================
def create_weather_icon(weather_type):
    """Return weather emoji based on type"""
    return WEATHER_ICONS.get(weather_type, "🌤️")


# =========================
# PDF GENERATION
# =========================
def generate_itinerary_pdf(city, country, weather, season, itinerary_text, city_row, user_input, language="English"):
    """
    Generate PDF from itinerary data using ReportLab
    """

    try:
        # Create PDF buffer
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)

        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2d5aa6'),
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        )

        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            leading=14
        )

        info_style = ParagraphStyle(
            'InfoText',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#555555'),
            spaceAfter=6
        )

        # Build PDF content
        content = []

        # Title
        title = Paragraph(f"🌍 {city}, {country}", title_style)
        content.append(title)
        content.append(Spacer(1, 0.2*inch))

        # Destination info section
        weather_icon = create_weather_icon(weather)
        info_data = [
            ["📊 Destination Information", ""],
            ["Location:", f"{city}, {country}"],
            ["Weather:", f"{weather_icon} {weather}"],
            ["Season:", f"🗓️ {season}"],
            ["Rating:", f"⭐ {city_row['avg_rating']}/5.0"],
            ["Match Score:", f"🎯 {city_row['final_score']:.2f}"],
            ["Ideal Duration:", f"📅 {city_row['ideal_duration_days']} days"],
            ["Budget Level:", f"💰 {user_input['budget']}"],
        ]

        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#e8f0f8')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.HexColor('#1f4788')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ]))
        content.append(info_table)
        content.append(Spacer(1, 0.3*inch))

        # Daily itinerary section
        content.append(Paragraph("📋 Your Personalized Itinerary", heading_style))
        content.append(Spacer(1, 0.1*inch))

        # Parse and format itinerary line-by-line
        itinerary_lines = itinerary_text.split('\n')
        current_section = []

        for i, line in enumerate(itinerary_lines):
            stripped_line = line.strip()

            if not stripped_line:
                # Empty line - add spacing
                if current_section:
                    for item in current_section:
                        content.append(item)
                    current_section = []
                content.append(Spacer(1, 0.08*inch))

            elif stripped_line.startswith('**Day'):
                # Day header - flush previous section and add new header
                if current_section:
                    for item in current_section:
                        content.append(item)
                    current_section = []

                content.append(Paragraph(stripped_line.replace('**', ''), heading_style))
                content.append(Spacer(1, 0.05*inch))

            elif stripped_line.startswith('- '):
                # Bullet point
                clean_text = stripped_line[2:]
                para = Paragraph(f"• {clean_text}", normal_style)
                current_section.append(para)

            elif stripped_line and not stripped_line.startswith('-'):
                # Regular text line
                para = Paragraph(stripped_line, normal_style)
                current_section.append(para)

        # Flush any remaining content
        if current_section:
            for item in current_section:
                content.append(item)

        # Footer
        content.append(Spacer(1, 0.3*inch))
        footer_text = f"Generated on {__import__('datetime').datetime.now().strftime('%B %d, %Y')}"
        content.append(Paragraph(footer_text, info_style))

        # Build PDF
        doc.build(content)
        pdf_buffer.seek(0)

        return pdf_buffer

    except Exception as e:
        raise Exception(f"PDF generation error: {str(e)}")


# =========================
# PDF HELPER FUNCTIONS
# =========================
def create_pdf_filename(city, country):
    """Generate a filename for the PDF"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{city}_{country}_{timestamp}.pdf"
