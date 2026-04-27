import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

DB_NAME = "database/business.db"

def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create Tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        city TEXT,
        signup_date DATE
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT,
        price REAL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product_id INTEGER,
        amount REAL,
        order_date DATE,
        FOREIGN KEY(customer_id) REFERENCES customers(id),
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Database tables created.")

def seed_db():
    conn = sqlite3.connect(DB_NAME)
    
    # Seed Customers
    customers = [
        ("Alice", "New York", "2023-01-15"),
        ("Bob", "Los Angeles", "2023-02-20"),
        ("Charlie", "Chicago", "2023-03-10"),
        ("David", "New York", "2023-04-05"),
        ("Eve", "San Francisco", "2023-05-12"),
        ("Frank", "Delhi", "2023-06-01"),
        ("Grace", "Mumbai", "2023-06-15"),
        ("Hank", "Delhi", "2023-07-01")
    ]
    
    for i, (name, city, date) in enumerate(customers, 1):
        conn.execute("INSERT OR IGNORE INTO customers (id, name, city, signup_date) VALUES (?, ?, ?, ?)", (i, name, city, date))
        
    # Seed Products
    products = [
        ("Laptop", "Electronics", 1200.00),
        ("Smartphone", "Electronics", 800.00),
        ("Headphones", "Electronics", 150.00),
        ("Chair", "Furniture", 200.00),
        ("Table", "Furniture", 300.00),
        ("Coffee Maker", "Home", 100.00),
        ("Blender", "Home", 80.00)
    ]
    
    for i, (name, category, price) in enumerate(products, 1):
        conn.execute("INSERT OR IGNORE INTO products (id, name, category, price) VALUES (?, ?, ?, ?)", (i, name, category, price))
        
    # Seed Orders
    orders = []
    start_date = datetime(2023, 1, 1)
    
    for i in range(1, 101): # 100 orders
        cust_id = random.randint(1, len(customers))
        prod_id = random.randint(1, len(products))
        # Get product price (simplified)
        price = products[prod_id-1][2]
        quantity = random.randint(1, 3)
        amount = price * quantity
        
        date = start_date + timedelta(days=random.randint(0, 365))
        order_date = date.strftime("%Y-%m-%d")
        
        orders.append((i, cust_id, prod_id, amount, order_date))
        
    for order in orders:
        conn.execute("INSERT OR IGNORE INTO orders (id, customer_id, product_id, amount, order_date) VALUES (?, ?, ?, ?, ?)", order)
        
    conn.commit()
    conn.close()
    print("Database seeded with sample data.")

if __name__ == "__main__":
    import os
    if not os.path.exists("database"):
        os.makedirs("database")
    create_db()
    seed_db()
