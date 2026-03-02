import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

# --- CONFIGURATION ---
# To send real emails, you must provide your Gmail App Password.
# 1. Go to Google Account > Security > 2-Step Verification > App Passwords
# 2. Generate a password and paste it below.
SMTP_EMAIL = "sumitsharmaje0786@gmail.com"  # Your real email to authenticate
SMTP_PASSWORD = ""                          # PASTE YOUR APP PASSWORD HERE
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# The "Dummy" Sender Name you requested
SENDER_DISPLAY_NAME = "Krira Billing <bill@krira.com>"
RECIPIENT_EMAIL = "sumitsharmaje0786@gmail.com"

def send_invoice_email(client_name, invoice_id, pdf_buffer):
    msg = MIMEMultipart()
    # We set the 'From' header to your requested dummy address
    # Note: Gmail may still show the authenticated email (SMTP_EMAIL) as the actual sender
    msg['From'] = SENDER_DISPLAY_NAME
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = f"Invoice: {client_name} - {invoice_id}"

    body = f"""
    Hello,

    Please find attached the invoice for {client_name}.
    
    Invoice Number: {invoice_id}
    
    Regards,
    Krira Billing Team
    """
    msg.attach(MIMEText(body, 'plain'))

    # Attach PDF with requested format: ClientName-InvoiceID.pdf
    # Sanitize filename to remove spaces or special chars
    safe_client_name = "".join(c for c in client_name if c.isalnum() or c in ('-', '_')).strip()
    safe_invoice_id = "".join(c for c in invoice_id if c.isalnum() or c in ('-', '_')).strip()
    filename = f"{safe_client_name}-{safe_invoice_id}.pdf"
    
    pdf_attachment = MIMEApplication(pdf_buffer.read(), _subtype="pdf")
    pdf_attachment.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(pdf_attachment)

    try:
        if not SMTP_PASSWORD:
            print("⚠️ SMTP_PASSWORD is not set. Email will NOT be sent (Mock Mode).")
            print(f"📧 [MOCK EMAIL] To: {RECIPIENT_EMAIL} | From: {SENDER_DISPLAY_NAME}")
            return True

        print(f"Connecting to {SMTP_SERVER}...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ [REAL EMAIL SENT] To: {RECIPIENT_EMAIL}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def send_daily_report_email(pdf_buffer, date_str):
    msg = MIMEMultipart()
    msg['From'] = SENDER_DISPLAY_NAME
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = f"Daily Business Report: {date_str}"

    body = f"""
    Hello,

    Please find attached the Daily Business Report for {date_str}.
    
    Includes:
    - Today's Invoices
    - Financial Summary
    - Stock Alerts
    - New Clients
    
    Regards,
    Krira Billing Team
    """
    msg.attach(MIMEText(body, 'plain'))

    # Attach PDF
    filename = f"DailyReport-{date_str}.pdf"
    pdf_attachment = MIMEApplication(pdf_buffer.read(), _subtype="pdf")
    pdf_attachment.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(pdf_attachment)

    try:
        if not SMTP_PASSWORD:
            print("⚠️ SMTP_PASSWORD is not set. Report will NOT be sent (Mock Mode).")
            print(f"📧 [MOCK REPORT] To: {RECIPIENT_EMAIL}")
            return True

        print(f"Connecting to {SMTP_SERVER}...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ [REPORT SENT] To: {RECIPIENT_EMAIL}")
        return True
    except Exception as e:
        print(f"❌ Failed to send report: {e}")
        return False
