import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket

# Configuration
GMAIL_MX_SERVER = "gmail-smtp-in.l.google.com"
SMTP_PORT = 25
SENDER_EMAIL = "bill@krira.com"
RECIPIENT_EMAIL = "sumitsharmaje0786@gmail.com"

def debug_send():
    print(f"--- Debugging Email Delivery to {RECIPIENT_EMAIL} ---")
    msg = MIMEMultipart()
    msg['From'] = f"Krira Debug <{SENDER_EMAIL}>"
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = "Debug Test: Direct Send"
    msg.attach(MIMEText("This is a debug test to check SMTP response.", 'plain'))

    try:
        server = smtplib.SMTP(GMAIL_MX_SERVER, SMTP_PORT)
        server.set_debuglevel(1) # Enable verbose output
        server.ehlo(socket.gethostname())
        
        print(f"Attempting to send from {SENDER_EMAIL}...")
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print("\n✅ SMTP Server accepted the message.")
    except Exception as e:
        print(f"\n❌ SMTP Error: {e}")

if __name__ == "__main__":
    debug_send()
