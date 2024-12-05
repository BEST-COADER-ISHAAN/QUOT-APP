# app/utils.py
import sqlite3
import os

DATABASE = 'app/database/quotation_app.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )""")
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
        conn.commit()

def validate_user(username, password):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return cursor.fetchone()

def get_dashboard_data():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, COUNT(*) FROM products GROUP BY name")
        product_data = cursor.fetchall()
        cursor.execute("SELECT * FROM customers LIMIT 5")
        recent_quotations = cursor.fetchall()
    return product_data, recent_quotations

def add_customer_to_db(form_data):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO customers (name, address, phone, email) VALUES (?, ?, ?, ?)
        """, (form_data['name'], form_data['address'], form_data['phone'], form_data['email']))
        conn.commit()

def add_product_to_db(form_data, file):
    image_path = None
    if file and file.get('image'):
        image = file['image']
        image_path = os.path.join('app/static/images', image.filename)
        image.save(image_path)
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO products (name, size, surface, rate_sq_ft, rate_per_box, image, link_360, website_link, additional_details)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (form_data['name'], form_data['size'], form_data['surface'], form_data['rate_sq_ft'], form_data['rate_per_box'],
              image_path, form_data['link_360'], form_data['website_link'], form_data['additional_details']))
        conn.commit()
