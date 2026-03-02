from database import get_session, Invoice, Client, Product, Payment, Purchase
from datetime import datetime
import json

def get_daily_report_data():
    session = get_session()
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    report_data = {
        "date": today_str,
        "invoices": [],
        "payments": [],
        "new_clients": [],
        "stock_alert": [],
        "financials": {
            "total_billed": 0.0,
            "total_received": 0.0
        }
    }

    try:
        # 1. Today's Invoices
        # Assuming createdAt is stored as YYYY-MM-DD
        invoices = session.query(Invoice).filter(Invoice.createdAt.like(f"{today_str}%")).all()
        for inv in invoices:
            client = session.query(Client).filter_by(id=inv.clientId).first()
            client_name = client.name if client else "Unknown"
            report_data["invoices"].append({
                "id": inv.id,
                "client": client_name,
                "total": inv.total
            })
            report_data["financials"]["total_billed"] += inv.total

        # 2. Today's Payments
        payments = session.query(Payment).filter(Payment.date == today_str).all()
        for pay in payments:
            client = session.query(Client).filter_by(id=pay.clientId).first()
            client_name = client.name if client else "Unknown"
            report_data["payments"].append({
                "id": pay.id,
                "client": client_name,
                "amount": pay.amount
            })
            report_data["financials"]["total_received"] += pay.amount

        # 3. New Clients (Best Effort)
        # Since Client table doesn't have createdAt, we'll check the JSON data
        # If not present, we can't reliably report this without schema change.
        # For now, we'll list ALL clients and let the user see (or filter if we add a date field later)
        # actually, let's try to parse ID if it's timestamp based, or just skip for now to avoid noise.
        # We will skip "New Clients" for now if we can't filter, or just show count.
        # Let's check if 'createdAt' is in the json blob.
        all_clients = session.query(Client).all()
        for c in all_clients:
            c_data = json.loads(c.data) if c.data else {}
            # If createdAt exists in JSON and matches today
            if c_data.get('createdAt', '').startswith(today_str):
                report_data["new_clients"].append({
                    "name": c.name,
                    "region": c.region
                })

        # 4. Stock Report (Low Stock & Expiry)
        products = session.query(Product).all()
        for p in products:
            p_data = json.loads(p.data) if p.data else {}
            
            # Low Stock Alert (e.g., < 10)
            if p.stock < 10:
                report_data["stock_alert"].append({
                    "name": p.name,
                    "stock": p.stock,
                    "issue": "Low Stock"
                })
            
            # Expiry Check (if 'expiryDate' exists in JSON)
            expiry = p_data.get('expiryDate')
            if expiry:
                # Simple string comparison or parsing if needed
                # Assuming YYYY-MM-DD
                if expiry <= today_str:
                     report_data["stock_alert"].append({
                        "name": p.name,
                        "stock": p.stock,
                        "issue": f"Expired ({expiry})"
                    })

    finally:
        session.close()

    return report_data
