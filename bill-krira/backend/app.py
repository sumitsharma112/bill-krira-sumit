from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_session, User, Client, Product, Invoice, Purchase, Request, Payment
import json
import uuid

app = Flask(__name__)
CORS(app)

# Helper to get DB session
def get_db():
    return get_session()

# --- Auth ---
@app.route('/api/login', methods=['POST'])
def login():
    # Log raw request for debugging
    print(f"DEBUG: Headers: {dict(request.headers)}")
    print(f"DEBUG: Raw Data: {request.get_data(as_text=True)}")
    
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON payload", "received": request.get_data(as_text=True)}), 400
        
    session = get_db()
    # Check username, password AND empCode
    user = session.query(User).filter_by(
        username=data.get('username'), 
        password=data.get('password'),
        empCode=data.get('empCode')
    ).first()
    session.close()
    
    if user:
        return jsonify(user.to_dict())
    return jsonify({"error": "Invalid credentials or Employee Code"}), 401

@app.route('/api/users', methods=['GET'])
def get_users():
    session = get_db()
    try:
        users = [u.to_dict() for u in session.query(User).all()]
        return jsonify(users)
    finally:
        session.close()

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    session = get_db()
    try:
        new_user = User(
            id=data['id'],
            username=data['username'],
            password=data['password'],
            role=data['role'],
            name=data.get('name'),
            region=data.get('region'),
            empCode=data.get('empCode')
        )
        session.add(new_user)
        session.commit()
        return jsonify(new_user.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route('/api/users/<id>', methods=['DELETE'])
def delete_user(id):
    session = get_db()
    try:
        session.query(User).filter_by(id=id).delete()
        session.commit()
        return jsonify({"success": True})
    finally:
        session.close()

# --- Data Fetching ---
@app.route('/api/data', methods=['GET'])
def get_all_data():
    session = get_db()
    try:
        data = {
            "clients": [c.to_dict() for c in session.query(Client).all()],
            "products": [p.to_dict() for p in session.query(Product).all()],
            "invoices": [i.to_dict() for i in session.query(Invoice).all()],
            "purchases": [p.to_dict() for p in session.query(Purchase).all()],
            "requests": [r.to_dict() for r in session.query(Request).all()],
            "payments": [p.to_dict() for p in session.query(Payment).all()]
        }
        return jsonify(data)
    finally:
        session.close()

# --- Clients ---
@app.route('/api/clients', methods=['POST'])
def add_client():
    data = request.json
    session = get_db()
    try:
        new_client = Client(
            id=data['id'],
            name=data['name'],
            region=data.get('region'),
            empCode=data.get('empCode'),
            data=json.dumps(data)
        )
        session.add(new_client)
        session.commit()
        return jsonify(new_client.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route('/api/clients/<id>', methods=['PUT'])
def update_client(id):
    data = request.json
    session = get_db()
    try:
        client = session.query(Client).filter_by(id=id).first()
        if client:
            client.name = data.get('name', client.name)
            client.region = data.get('region', client.region)
            client.empCode = data.get('empCode', client.empCode)
            client.data = json.dumps(data)
            session.commit()
            return jsonify(client.to_dict())
        return jsonify({"error": "Not found"}), 404
    finally:
        session.close()

@app.route('/api/clients/<id>', methods=['DELETE'])
def delete_client(id):
    session = get_db()
    try:
        session.query(Client).filter_by(id=id).delete()
        session.commit()
        return jsonify({"success": True})
    finally:
        session.close()

# --- Products ---
@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    session = get_db()
    try:
        new_product = Product(
            id=data['id'],
            name=data['name'],
            stock=int(data.get('stock', 0)),
            data=json.dumps(data)
        )
        session.add(new_product)
        session.commit()
        return jsonify(new_product.to_dict())
    finally:
        session.close()

@app.route('/api/products/<id>', methods=['PUT'])
def update_product(id):
    data = request.json
    session = get_db()
    try:
        product = session.query(Product).filter_by(id=id).first()
        if product:
            product.name = data.get('name', product.name)
            product.stock = int(data.get('stock', product.stock))
            product.data = json.dumps(data)
            session.commit()
            return jsonify(product.to_dict())
        return jsonify({"error": "Not found"}), 404
    finally:
        session.close()

@app.route('/api/products/<id>', methods=['DELETE'])
def delete_product(id):
    session = get_db()
    try:
        session.query(Product).filter_by(id=id).delete()
        session.commit()
        return jsonify({"success": True})
    finally:
        session.close()

# --- Invoices ---
@app.route('/api/invoices', methods=['POST'])
def add_invoice():
    data = request.json
    session = get_db()
    try:
        new_invoice = Invoice(
            id=data['id'],
            clientId=data.get('clientId'),
            total=float(data.get('total', 0)),
            createdAt=data.get('createdAt'),
            data=json.dumps(data)
        )
        session.add(new_invoice)
        
        # Update stock
        for item in data.get('items', []):
            product = session.query(Product).filter_by(id=item['productId']).first()
            if product:
                product.stock -= int(item['quantity'])
                # Update product data blob too to keep in sync
                p_data = json.loads(product.data)
                p_data['stock'] = product.stock
                product.data = json.dumps(p_data)
        
        session.commit()
        
        # --- Email Notification Trigger ---
        try:
            # 1. Get Client Name
            client = session.query(Client).filter_by(id=data.get('clientId')).first()
            client_name = client.name if client else "Unknown Client"
            
            # 2. Generate PDF
            from pdf_generator import generate_invoice_pdf
            pdf_buffer = generate_invoice_pdf(new_invoice.to_dict(), client_name)
            
            # 3. Send Email
            from email_service import send_invoice_email
            send_invoice_email(client_name, new_invoice.id, pdf_buffer)
            
        except Exception as e:
            print(f"⚠️ Email Notification Failed: {e}")
        # ----------------------------------

        return jsonify(new_invoice.to_dict())
    finally:
        session.close()

@app.route('/api/invoices/<id>', methods=['PUT'])
def update_invoice(id):
    data = request.json
    session = get_db()
    try:
        invoice = session.query(Invoice).filter_by(id=id).first()
        if invoice:
            invoice.total = float(data.get('total', invoice.total))
            invoice.data = json.dumps(data)
            session.commit()
            return jsonify(invoice.to_dict())
        return jsonify({"error": "Not found"}), 404
    finally:
        session.close()

@app.route('/api/invoices/<id>', methods=['DELETE'])
def delete_invoice(id):
    session = get_db()
    try:
        session.query(Invoice).filter_by(id=id).delete()
        session.commit()
        return jsonify({"success": True})
    finally:
        session.close()

# --- Purchases ---
@app.route('/api/purchases', methods=['POST'])
def add_purchase():
    data = request.json
    session = get_db()
    try:
        new_purchase = Purchase(
            id=data['id'],
            productId=data.get('productId'),
            quantity=int(data.get('quantity', 0)),
            data=json.dumps(data)
        )
        session.add(new_purchase)
        
        # Update stock
        product = session.query(Product).filter_by(id=data['productId']).first()
        if product:
            product.stock += int(data['quantity'])
            p_data = json.loads(product.data)
            p_data['stock'] = product.stock
            product.data = json.dumps(p_data)
            
        session.commit()
        return jsonify(new_purchase.to_dict())
    finally:
        session.close()

# --- Requests ---
@app.route('/api/requests', methods=['POST'])
def add_request():
    data = request.json
    session = get_db()
    try:
        new_req = Request(
            id=data['id'],
            clientId=data.get('clientId'),
            status=data.get('status', 'Pending'),
            data=json.dumps(data)
        )
        session.add(new_req)
        session.commit()
        return jsonify(new_req.to_dict())
    finally:
        session.close()

@app.route('/api/requests/<id>', methods=['PUT'])
def update_request(id):
    data = request.json
    session = get_db()
    try:
        req = session.query(Request).filter_by(id=id).first()
        if req:
            req.status = data.get('status', req.status)
            req.data = json.dumps(data)
            session.commit()
            return jsonify(req.to_dict())
        return jsonify({"error": "Not found"}), 404
    finally:
        session.close()

@app.route('/api/requests/<id>', methods=['DELETE'])
def delete_request(id):
    session = get_db()
    try:
        session.query(Request).filter_by(id=id).delete()
        session.commit()
        return jsonify({"success": True})
    finally:
        session.close()

# --- Payments ---
@app.route('/api/payments', methods=['POST'])
def add_payment():
    data = request.json
    session = get_db()
    try:
        new_payment = Payment(
            id=data['id'],
            clientId=data.get('clientId'),
            amount=float(data.get('amount', 0)),
            date=data.get('date'),
            data=json.dumps(data)
        )
        session.add(new_payment)
        session.commit()
        return jsonify(new_payment.to_dict())
    finally:
        session.close()

# --- Reports ---
@app.route('/api/reports/daily', methods=['POST'])
def send_daily_report():
    try:
        # 1. Get Data
        from report_service import get_daily_report_data
        report_data = get_daily_report_data()
        
        # 2. Generate PDF
        from pdf_generator import generate_daily_report_pdf
        pdf_buffer = generate_daily_report_pdf(report_data)
        
        # 3. Send Email
        from email_service import send_daily_report_email
        success = send_daily_report_email(pdf_buffer, report_data['date'])
        
        if success:
            return jsonify({"success": True, "message": "Daily report sent successfully"})
        else:
            return jsonify({"success": False, "message": "Failed to send email"}), 500
            
    except Exception as e:
        print(f"❌ Report Generation Failed: {e}")
        return jsonify({"error": str(e)}), 500

# --- Init ---
def init_db():
    session = get_db()
    if session.query(User).count() == 0:
        print("Seeding default users...")
        admin = User(id='admin-1', username='krira-sumit', password='Ankit-Sumit', role='admin', name='Admin User', region='all', empCode='ADMIN01')
        viewer = User(id='viewer-1', username='viewer', password='password123', role='viewer', name='View Only User', region='all', empCode='VIEW01')
        session.add(admin)
        session.add(viewer)
        session.commit()
    session.close()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
