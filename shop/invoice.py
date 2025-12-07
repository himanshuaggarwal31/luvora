"""
Invoice generation utilities for orders
"""
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from django.conf import settings
import os


def generate_invoice_pdf(order):
    """
    Generate PDF invoice for an order
    Returns BytesIO buffer containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#8B4513'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#8B4513'),
        spaceAfter=12,
    )
    
    right_align_style = ParagraphStyle(
        'RightAlign',
        parent=styles['Normal'],
        alignment=TA_RIGHT,
    )
    
    # Add logo (if exists)
    # logo_path = os.path.join(settings.STATIC_ROOT, 'images', 'logo.png')
    # if os.path.exists(logo_path):
    #     logo = Image(logo_path, width=2*inch, height=1*inch)
    #     story.append(logo)
    #     story.append(Spacer(1, 0.3*inch))
    
    # Title
    story.append(Paragraph("LUVORA", title_style))
    story.append(Paragraph("Tax Invoice", styles['Heading2']))
    story.append(Spacer(1, 0.3*inch))
    
    # Invoice details
    invoice_data = [
        ['Invoice Number:', order.order_id, 'Date:', order.created_at.strftime('%d %b %Y')],
        ['Payment Status:', order.get_status_display(), 'Payment ID:', order.razorpay_payment_id or 'N/A'],
    ]
    
    invoice_table = Table(invoice_data, colWidths=[1.5*inch, 2.5*inch, 1*inch, 1.5*inch])
    invoice_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(invoice_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Customer details
    story.append(Paragraph("Bill To:", heading_style))
    customer_info = f"""
    <b>{order.customer_name}</b><br/>
    {order.customer_email}<br/>
    {order.customer_phone}<br/>
    <br/>
    <b>Shipping Address:</b><br/>
    {order.shipping_address_line1}<br/>
    {order.shipping_address_line2 + '<br/>' if order.shipping_address_line2 else ''}
    {order.shipping_city}, {order.shipping_state} - {order.shipping_pincode}<br/>
    {order.shipping_country}
    """
    story.append(Paragraph(customer_info, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Order items table
    story.append(Paragraph("Order Items:", heading_style))
    
    # Table header
    items_data = [['Item', 'SKU', 'Quantity', 'Price', 'Total']]
    
    # Table rows
    for item in order.items.all():
        items_data.append([
            item.product_name,
            item.product_sku,
            str(item.quantity),
            f'₹{item.product_price:.2f}',
            f'₹{item.get_total_price():.2f}'
        ])
    
    # Totals
    items_data.append(['', '', '', 'Subtotal:', f'₹{order.subtotal:.2f}'])
    
    if order.discount_amount > 0:
        items_data.append(['', '', '', 'Discount:', f'-₹{order.discount_amount:.2f}'])
        if order.coupon_code:
            items_data.append(['', '', '', f'Coupon ({order.coupon_code}):', ''])
    
    if order.shipping_cost > 0:
        items_data.append(['', '', '', 'Shipping:', f'₹{order.shipping_cost:.2f}'])
    
    if order.tax_amount > 0:
        items_data.append(['', '', '', 'Tax:', f'₹{order.tax_amount:.2f}'])
    
    items_data.append(['', '', '', 'Total:', f'₹{order.total:.2f}'])
    
    # Create table
    items_table = Table(items_data, colWidths=[3*inch, 1.2*inch, 0.8*inch, 1*inch, 1*inch])
    items_table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B4513')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Data rows
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (2, 1), (2, -1), 'CENTER'),
        ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        
        # Subtotal and totals
        ('FONTNAME', (3, -5), (-1, -1), 'Helvetica-Bold'),
        ('LINEABOVE', (3, -5), (-1, -5), 1, colors.black),
        ('LINEABOVE', (3, -1), (-1, -1), 2, colors.black),
        ('BACKGROUND', (3, -1), (-1, -1), colors.HexColor('#f0f0f0')),
    ]))
    
    story.append(items_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_text = """
    <b>Thank you for your purchase!</b><br/>
    <br/>
    For any queries, please contact us at:<br/>
    Email: info@luvora.com<br/>
    Phone: +91 XXXXXXXXXX<br/>
    Website: www.luvora.com<br/>
    <br/>
    <i>This is a computer-generated invoice and does not require a signature.</i>
    """
    story.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
