from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO

def generate_invoice_pdf(invoice_data, client_name):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=20
    )
    elements.append(Paragraph("INVOICE", title_style))
    elements.append(Spacer(1, 12))

    # Header Info
    header_data = [
        [f"Invoice #: {invoice_data['id'][:8]}", f"Date: {invoice_data.get('date', 'N/A')}"],
        [f"Client: {client_name}", f"Status: {invoice_data.get('status', 'Draft')}"]
    ]
    header_table = Table(header_data, colWidths=[300, 200])
    header_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 20))

    # Items Table
    items = invoice_data.get('items', [])
    table_data = [['Item', 'Qty', 'Price', 'Total']]
    
    for item in items:
        total = float(item.get('quantity', 0)) * float(item.get('price', 0))
        table_data.append([
            item.get('description', 'Item'),
            str(item.get('quantity', 0)),
            f"Rs. {item.get('price', 0)}",
            f"Rs. {total:.2f}"
        ])

    # Total Row
    table_data.append(['', '', 'Grand Total:', f"Rs. {invoice_data.get('total', 0):.2f}"])

    item_table = Table(table_data, colWidths=[250, 50, 100, 100])
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f8fafc')),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.black),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -2), 1, colors.black),
    ]))
    elements.append(item_table)

    # Footer
    elements.append(Spacer(1, 40))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.gray
    )
    elements.append(Paragraph("Thank you for your business!", footer_style))
    elements.append(Paragraph("Krira Pharma Billing System", footer_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer

def generate_daily_report_pdf(report_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=20,
        alignment=1 # Center
    )
    elements.append(Paragraph(f"Daily Business Report: {report_data['date']}", title_style))
    elements.append(Spacer(1, 12))

    # 1. Financial Summary
    elements.append(Paragraph("Financial Summary", styles['Heading2']))
    fin_data = [
        ['Total Billed', f"Rs. {report_data['financials']['total_billed']:.2f}"],
        ['Total Received', f"Rs. {report_data['financials']['total_received']:.2f}"]
    ]
    fin_table = Table(fin_data, colWidths=[200, 200])
    fin_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ]))
    elements.append(fin_table)
    elements.append(Spacer(1, 20))

    # 2. Today's Invoices
    if report_data['invoices']:
        elements.append(Paragraph(f"Invoices Generated ({len(report_data['invoices'])})", styles['Heading2']))
        inv_data = [['Invoice ID', 'Client', 'Amount']]
        for inv in report_data['invoices']:
            inv_data.append([inv['id'], inv['client'], f"Rs. {inv['total']:.2f}"])
        
        inv_table = Table(inv_data, colWidths=[150, 200, 100])
        inv_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e2e8f0')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(inv_table)
        elements.append(Spacer(1, 20))

    # 3. New Clients
    if report_data['new_clients']:
        elements.append(Paragraph(f"New Clients ({len(report_data['new_clients'])})", styles['Heading2']))
        client_data = [['Name', 'Region']]
        for c in report_data['new_clients']:
            client_data.append([c['name'], c['region']])
        
        client_table = Table(client_data, colWidths=[250, 150])
        client_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(client_table)
        elements.append(Spacer(1, 20))

    # 4. Stock Alerts
    if report_data['stock_alert']:
        elements.append(Paragraph("Stock Alerts (Low/Expired)", styles['Heading2']))
        stock_data = [['Product', 'Stock', 'Issue']]
        for item in report_data['stock_alert']:
            stock_data.append([item['name'], str(item['stock']), item['issue']])
        
        stock_table = Table(stock_data, colWidths=[200, 100, 150])
        stock_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#fee2e2')), # Light red header
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.red),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(stock_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer
