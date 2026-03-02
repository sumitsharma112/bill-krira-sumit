#!/usr/bin/env python3
import sqlite3
import json
import uuid
from datetime import datetime

# New Krira Pharma Products
krira_products = [
    {
        "name": "Krisure Syrup 200ml",
        "description": "Krisure Syrup",
        "price": "175.00",
        "packing": "Syrup",
        "manufacturer": "Krira Pharma Co.",
        "stock": 0  # Stock will show after manually adding
    },
    {
        "name": "Kri-K27 Tablet",
        "description": "10 Tablets",
        "price": "175.00",
        "packing": "Tablet",
        "manufacturer": "Krira Pharma Co.",
        "stock": 0
    },
    {
        "name": "KPDEX Syrup 100ml",
        "description": "KPDEX Syrup",
        "price": "120.00",
        "packing": "Syrup",
        "manufacturer": "Krira Pharma Co.",
        "stock": 0
    },
    {
        "name": "KPD3 60K Capsule",
        "description": "4 Capsules",
        "price": "99.00",
        "packing": "Tablet",
        "manufacturer": "Krira Pharma Co.",
        "stock": 0
    },
    {
        "name": "Keftall SPASS Tablet",
        "description": "10 Tablets",
        "price": "49.00",
        "packing": "Tablet",
        "manufacturer": "Krira Pharma Co.",
        "stock": 0
    },
    {
        "name": "KPDEX-H Syrup 100ml",
        "description": "KPDEX-H Syrup",
        "price": "140.00",
        "packing": "Syrup",
        "manufacturer": "Krira Pharma Co.",
        "stock": 0
    },
    {
        "name": "UTI-LEU Capsule",
        "description": "30 Capsules",
        "price": "350.00",
        "packing": "Tablet",
        "manufacturer": "Krira Pharma Co.",
        "stock": 0
    },
    {
        "name": "Aciramol-P Tablet",
        "description": "10 Tablets",
        "price": "120.00",
        "packing": "Tablet",
        "manufacturer": "Krira Pharma Co.",
        "stock": 0
    },
    {
        "name": "Aciramol SP Tablet",
        "description": "10 Tablets",
        "price": "150.00",
        "packing": "Tablet",
        "manufacturer": "Krira Pharma Co.",
        "stock": 0
    },
    {
        "name": "KPin-NT Tablet",
        "description": "10 Tablets",
        "price": "350.00",
        "packing": "Tablet",
        "manufacturer": "Krira Pharma Co.",
        "stock": 0
    },
    {
        "name": "KP-Wash 100ml",
        "description": "KP-Wash Solution",
        "price": "250.00",
        "packing": "Others",
        "manufacturer": "Krira Pharma Co.",
        "stock": 0
    }
]

# Connect to database
conn = sqlite3.connect('billing.db')
cursor = conn.cursor()

# Delete all existing products
print("Deleting old products...")
cursor.execute("DELETE FROM products")
deleted = cursor.rowcount
print(f"✓ Deleted {deleted} old products\n")

# Add new Krira Pharma products
print("Adding new Krira Pharma Products...\n")
for product in krira_products:
    product_id = str(uuid.uuid4())
    created_at = datetime.now().isoformat()
    
    # Prepare data blob
    product['id'] = product_id
    product['createdAt'] = created_at
    # HSN and Batch will be empty initially
    product['hsnCode'] = ''
    product['batchNumber'] = ''
    product['expiryDate'] = ''
    
    try:
        cursor.execute(
            "INSERT INTO products (id, name, stock, data) VALUES (?, ?, ?, ?)",
            (product_id, product['name'], product['stock'], json.dumps(product))
        )
        print(f"✓ Added: {product['name']} - MRP ₹{product['price']}")
    except Exception as e:
        print(f"✗ Failed to add {product['name']}: {e}")

conn.commit()
conn.close()

print(f"\n✅ Successfully updated database with {len(krira_products)} Krira Pharma products!")
print("\nNote: HSN Code, Batch Number, and Stock will show after manually adding them.")
