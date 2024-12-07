from flask import Flask, render_template, redirect, url_for, request, session, flash, send_file, jsonify
from app.utils import (
    init_db, validate_user, get_dashboard_data, add_customer_to_db,
    add_product_to_db, save_quotation, get_quotation, generate_pdf,
    get_customers, get_products, Product
)
from num2words import num2words
import os
import sqlite3
from app.database import fetch_products_from_db


app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'app/static/images'
PDF_FOLDER = 'app/static/pdfs'

# Ensure the PDFs folder exists
if not os.path.exists(PDF_FOLDER):
    os.makedirs(PDF_FOLDER)

# Initialize the database
init_db()

@app.route('/')
def login():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']
    if validate_user(username, password):
        session['logged_in'] = True
        flash("Login successful!", "success")
        return redirect(url_for('dashboard'))
    else:
        flash("Invalid credentials. Please try again.", "danger")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    # Get data for dashboard
    product_data, recent_quotations = get_dashboard_data()
    return render_template('dashboard.html', product_data=product_data, recent_quotations=recent_quotations)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        add_customer_to_db(request.form)
        flash("Customer added successfully!", "success")
        return redirect(url_for('dashboard'))
    return render_template('add_customer.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Retrieve form data for the product
        name = request.form['name']
        size = request.form['size']
        surface = request.form['surface']
        rate_sq_ft = request.form['rate_sq_ft']
        rate_per_box = request.form['rate_per_box']
        
        # Image URL instead of storing the image on disk
        image_url = request.form['image_url']  # Expecting an image URL instead of file upload
        link_360 = request.form['link_360']
        website_link = request.form['website_link']
        additional_details = request.form['additional_details']

        # Add product to the database (no local image saving)
        add_product_to_db(name, size, surface, rate_sq_ft, rate_per_box, image_url, link_360, website_link, additional_details)

        flash("Product added successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('add_product.html')

@app.route('/view_quotation/<int:quotation_id>')
def view_quotation(quotation_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    quotation_data = get_quotation(quotation_id)
    if not quotation_data:
        flash("Quotation not found.", "danger")
        return redirect(url_for('dashboard'))

    return render_template('view_quotation.html', quotation=quotation_data)

@app.route('/create_quotation', methods=['GET', 'POST'])
def create_quotation():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        items = []
        grand_total = 0

        for i, product_id in enumerate(request.form.getlist('product_id[]')):
            size = request.form.getlist('size[]')[i]
            surface = request.form.getlist('surface[]')[i]
            rate_sq_ft = request.form.getlist('rate_sq_ft[]')[i]
            rate_per_box = float(request.form.getlist('rate_per_box[]')[i])
            quantity = int(request.form.getlist('quantity[]')[i])
            total_price = rate_per_box * quantity
            grand_total += total_price
            items.append({
                'product_id': product_id,
                'size': size,
                'surface': surface,
                'rate_sq_ft': rate_sq_ft,
                'rate_per_box': rate_per_box,
                'quantity': quantity,
                'total_price': total_price
            })

        # Convert the total to words
        amount_in_words = num2words(grand_total, to='currency', lang='en')
        save_quotation(customer_id, items, grand_total, amount_in_words)

        flash("Quotation created successfully!", "success")
        return redirect(url_for('dashboard'))

    # Fetch customers and products for the form
    customers = get_customers()
    products = get_products()
    return render_template('create_quotation.html', customers=customers, products=products)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/search_products', methods=['GET'])
def search_products():
    query = request.args.get('q', '').lower()  # Get search query
    products = query_db("SELECT * FROM products WHERE LOWER(name) LIKE ?", (f"%{query}%",))
    return jsonify(products)  # Return products in JSON format

@app.route('/create_quotation', methods=['GET'])
def create_quotation():
    products = fetch_products_from_db()  # Fetch products from the database
    return render_template('create_quotation.html', products=products)


