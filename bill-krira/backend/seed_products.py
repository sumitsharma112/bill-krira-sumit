#!/usr/bin/env python3
import sqlite3
import json
import uuid
from datetime import datetime

# Sample Krira Pharma Products
pharmaceutical_products = [
    {
        "name": "Paracetamol 500mg Tablet",
        "description": "Pain reliever and fever reducer",
        "price": "50.00",
        "expiryDate": "2026-12-31",
        "hsnCode": "3004",
        "packing": "Tablet",
        "manufacturer": "Krira Pharma Co.",
        "batchNumber": "KRP-PAR-001",
        "stock": 500
    },
    {
        "name": "Amoxicillin 250mg Capsule",
        "description": "Antibiotic for bacterial infections",
        "price": "120.00",
        "expiryDate": "2026-08-31",
        "hsnCode": "3004",
        "packing": "Tablet",
        "manufacturer": "Krira Pharma Co.",
        "batchNumber": "KRP-AMX-002",
        "stock": 300
    },
    {
        "name": "Cetirizine 10mg Tablet",
        "description": "Antihistamine for allergies",
        "price": "60.00",
        "expiryDate": "2027-03-31",
        "hsnCode": "3004",
        "packing": "Tablet",
        "manufacturer": "Krira Pharma Co.",
        "batchNumber": "KRP-CET-003",
        "stock": 450
    },
    {
        "name": "Cough Syrup 100ml",
        "description": "Relief from cough and cold",
        "price": "85.00",
        "expiryDate": "2026-06-30",
        "hsnCode": "3004",
        "packing": "Syrup",
        "manufacturer": "Krira Pharma Co.",
        "batchNumber": "KRP-CGH-004",
        "stock": 200
    },
    {
        "name": "Vitamin D3 60000 IU Capsule",
        "description": "Vitamin D supplement",
        "price": "150.00",
        "expiryDate": "2027-12-31",
        "hsnCode": "3004",
        "packing": "Tablet",
        "manufacturer": "Krira Pharma Co.",
        "batchNumber": "KRP-VD3-005",
        "stock": 250
    }
]

# Connect to database
conn = sqlite3.connect('billing.db')
cursor = conn.cursor()

# Add products
print("Adding Krira Pharma Products to database...\n")
for product in pharmaceutical_products:
    product_id = str(uuid.uuid4())
    created_at = datetime.now().isoformat()
    
    # Prepare data blob
    product['id'] = product_id
    product['createdAt'] = created_at
    
    try:
        cursor.execute(
            "INSERT INTO products (id, name, stock, data) VALUES (?, ?, ?, ?)",
            (product_id, product['name'], product['stock'], json.dumps(product))
        )
        print(f"✓ Added: {product['name']} (Stock: {product['stock']})")
    except Exception as e:
        print(f"✗ Failed to add {product['name']}: {e}")

conn.commit()
conn.close()

print(f"\n✅ Successfully added {len(pharmaceutical_products)} Krira Pharma products to the database!")
print("\nRefresh your browser to see the new products.")
