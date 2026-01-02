from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
from decimal import Decimal
from typing import List
from app.schemas.quotation import QuotationItemResponse
from app.schemas.user import UserResponse
import io


def generate_quotation_pdf(
    quotation_number: str,
    user: UserResponse,
    items: List[QuotationItemResponse],
    total_amount: Decimal,
    output_buffer: io.BytesIO
) -> io.BytesIO:
    """Generate a PDF quotation document"""
    
    doc = SimpleDocTemplate(output_buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#666666')
    )
    
    # Title
    story.append(Paragraph("AureumPOS", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Quotation Number
    story.append(Paragraph(f"Cotización #{quotation_number}", heading_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Date
    date_str = datetime.now().strftime("%d de %B de %Y")
    story.append(Paragraph(f"Fecha: {date_str}", normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Client Information
    story.append(Paragraph("Información del Cliente", heading_style))
    client_data = [
        ["Nombre:", f"{user.first_name} {user.last_name}"],
        ["Email:", user.email],
    ]
    if user.address:
        client_data.append(["Dirección:", user.address])
    if user.phone:
        client_data.append(["Teléfono:", user.phone])
    
    client_table = Table(client_data, colWidths=[2*inch, 4*inch])
    client_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#333333')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#666666')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(client_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Products Table
    story.append(Paragraph("Detalle de Productos", heading_style))
    
    # Table headers
    table_data = [["Producto", "Cantidad", "Precio Unitario", "Subtotal"]]
    
    # Table rows
    for item in items:
        table_data.append([
            item.product_name,
            str(item.quantity),
            f"${item.unit_price:,.2f}",
            f"${item.subtotal:,.2f}"
        ])
    
    # Create table
    products_table = Table(table_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
    products_table.setStyle(TableStyle([
        # Header style
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        # Data style
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#333333')),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e0e0e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    story.append(products_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Total
    total_style = ParagraphStyle(
        'TotalStyle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#1a1a1a'),
        alignment=TA_RIGHT,
        fontName='Helvetica-Bold'
    )
    story.append(Paragraph(f"Total: ${total_amount:,.2f}", total_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#999999'),
        alignment=TA_CENTER
    )
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Gracias por su preferencia", footer_style))
    story.append(Paragraph("AureumPOS - Sistema de Punto de Venta", footer_style))
    
    # Build PDF
    doc.build(story)
    output_buffer.seek(0)
    return output_buffer

