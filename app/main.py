# app/main.py
from flask import Flask, render_template, redirect, url_for, request, session, flash
from app.utils import init_db, validate_user, get_dashboard_data, add_customer_to_db, add_product_to_db
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'app/static/images'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']
    if validate_user(username, password):
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid credentials. Try again.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    product_data, recent_quotations = get_dashboard_data()
    return render_template('dashboard.html', product_data=product_data, recent_quotations=recent_quotations)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        add_customer_to_db(request.form)
        return redirect(url_for('dashboard'))
    return render_template('add_customer.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        add_product_to_db(request.form, request.files)
        return redirect(url_for('dashboard'))
    return render_template('add_product.html')

if __name__ == '__main__':
    app.run(debug=True)
