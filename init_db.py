import sqlite3
import os

DATABASE = 'app/database/quotation_app.db'

def init_db():
    if not os.path.exists(os.path.dirname(DATABASE)):
        os.makedirs(os.path.dirname(DATABASE))
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        
        # Existing tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT,
            phone TEXT,
            email TEXT
        )""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            size TEXT,
            surface TEXT,
            rate_sq_ft REAL,
            rate_per_box REAL,
            image TEXT,
            link_360 TEXT,
            website_link TEXT,
            additional_details TEXT
        )""")
        
        # New tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount REAL,
            amount_in_words TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotation_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quotation_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER,
            rate_per_box REAL,
            total_price REAL,
            FOREIGN KEY (quotation_id) REFERENCES quotations(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )""")
        
        conn.commit()
        print("Database initialized with quotations and details tables.")

if __name__ == '__main__':
    init_db()
