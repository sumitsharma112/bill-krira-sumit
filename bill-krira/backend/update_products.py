#!/usr/bin/env python3
import sqlite3
import json

# Connect to database
conn = sqlite3.connect('billing.db')
cursor = conn.cursor()

# Find all products with "Web Development" in the name
cursor.execute("SELECT id, name, data FROM products WHERE name LIKE '%Web Development%'")
products = cursor.fetchall()

if products:
    print(f"Found {len(products)} product(s) with 'Web Development' in the name:")
    for product in products:
        print(f"  - ID: {product[0]}, Name: {product[1]}")
        
        # Update the product name
        data = json.loads(product[2]) if product[2] else {}
        data['name'] = 'Paracetamol 500mg Tablet'
        
        cursor.execute(
            "UPDATE products SET name = ?, data = ? WHERE id = ?",
            ('Paracetamol 500mg Tablet', json.dumps(data), product[0])
        )
        print(f"  ✓ Updated to: Paracetamol 500mg Tablet")
    
    conn.commit()
    print("\n✅ Database updated successfully!")
else:
    print("No products found with 'Web Development' in the name.")
    
    # Show all products
    cursor.execute("SELECT id, name FROM products")
    all_products = cursor.fetchall()
    if all_products:
        print(f"\nCurrent products in database ({len(all_products)}):")
        for p in all_products:
            print(f"  - {p[1]} (ID: {p[0]})")
    else:
        print("\nDatabase is empty - no products found.")

conn.close()
