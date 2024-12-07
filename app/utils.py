import sqlite3
import os
from fpdf import FPDF
from werkzeug.security import generate_password_hash, check_password_hash

# Define the path to the SQLite database
DATABASE = 'app/database/quotation_app.db'

# Function to initialize the database
def init_db():
    """Initializes the database with necessary tables."""
    if not os.path.exists(os.path.dirname(DATABASE)):
        os.makedirs(os.path.dirname(DATABASE))
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # Create Customers table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT,
            phone TEXT,
            email TEXT
        )""")
        # Create Products table
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
        # Create Quotations table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount REAL,
            amount_in_words TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )""")
        # Create Quotation Details table
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
        # Create Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )""")
        # Insert default admin user if not exists
        cursor.execute("""
        INSERT OR IGNORE INTO users (username, password)
        VALUES (?, ?)
        """, ("admin", generate_password_hash("admin123")))
        conn.commit()

# Function to validate user login
def validate_user(username, password):
    """Validates the user's credentials."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result and check_password_hash(result[0], password):
            return True
    return False

# Function to fetch dashboard data
def get_dashboard_data():
    """Fetches product data and recent quotations for the dashboard."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # Product data
        cursor.execute("SELECT name, COUNT(*) FROM products GROUP BY name")
        product_data = cursor.fetchall()
        # Recent quotations (replace with real quotation data if needed)
        cursor.execute("SELECT id, customer_id, total_amount FROM quotations ORDER BY date DESC LIMIT 5")
        recent_quotations = cursor.fetchall()
    return product_data, recent_quotations

# Function to fetch all customers
def get_customers():
    """Fetches all customers."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM customers")
        return cursor.fetchall()

# Function to fetch all products
def get_products():
    """Fetches all products."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, name, size, surface, rate_sq_ft, rate_per_box
        FROM products
        """)
        return [
            {
                "id": row[0],
                "name": row[1],
                "size": row[2],
                "surface": row[3],
                "rate_sq_ft": row[4],
                "rate_per_box": row[5]
            }
            for row in cursor.fetchall()
        ]

# Function to add a customer to the database
def add_customer_to_db(form_data):
    """Adds a new customer to the database."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO customers (name, address, phone, email)
        VALUES (?, ?, ?, ?)
        """, (form_data['name'], form_data['address'], form_data['phone'], form_data['email']))
        conn.commit()

# Function to add a product to the database
def add_product_to_db(name, size, surface, rate_sq_ft, rate_per_box, image_url, link_360, website_link, additional_details):
    """Adds a new product to the database with an image URL instead of storing the image locally."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO products (name, size, surface, rate_sq_ft, rate_per_box, image, link_360, website_link, additional_details)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, size, surface, rate_sq_ft, rate_per_box, image_url, link_360, website_link, additional_details))
        conn.commit()

# Function to save a quotation
def save_quotation(customer_id, items, total_amount, amount_in_words):
    """Saves a quotation and its details in the database."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # Insert into Quotations table
        cursor.execute("""
        INSERT INTO quotations (customer_id, total_amount, amount_in_words)
        VALUES (?, ?, ?)
        """, (customer_id, total_amount, amount_in_words))
        quotation_id = cursor.lastrowid
        # Insert into Quotation Details table
        for item in items:
            cursor.execute("""
            INSERT INTO quotation_details (quotation_id, product_id, quantity, rate_per_box, total_price)
            VALUES (?, ?, ?, ?, ?)
            """, (quotation_id, item['product_id'], item['quantity'], item['rate_per_box'], item['total_price']))
        conn.commit()
        return quotation_id

# Function to fetch quotation details
def get_quotation(quotation_id):
    """Retrieves quotation metadata and details."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT q.id, c.name, c.address, c.phone, c.email, q.date, q.total_amount, q.amount_in_words
        FROM quotations q
        JOIN customers c ON q.customer_id = c.id
        WHERE q.id = ?
        """, (quotation_id,))
        quotation = cursor.fetchone()
        cursor.execute("""
        SELECT p.name, p.size, p.surface, qd.quantity, qd.rate_per_box, qd.total_price
        FROM quotation_details qd
        JOIN products p ON qd.product_id = p.id
        WHERE qd.quotation_id = ?
        """, (quotation_id,))
        items = cursor.fetchall()
        return {'quotation': quotation, 'items': items}

# Function to generate PDF
def generate_pdf(quotation_data, output_path):
    """Generates a PDF for a quotation."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Quotation", ln=True, align='C')
    pdf.output(output_path)

def get_customers():
    """Fetches all customers."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM customers")
        return cursor.fetchall()
    

def fetch_products_from_db():
    connection = sqlite3.connect("your_database.db")
    cursor = connection.cursor()
    query = "SELECT id, name, size, surface, rate_sq_ft, rate_per_box FROM products"
    cursor.execute(query)
    products = cursor.fetchall()
    connection.close()
    return [{"id": p[0], "name": p[1], "size": p[2], "surface": p[3], "rate_sq_ft": p[4], "rate_per_box": p[5]} for p in products]