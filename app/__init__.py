from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'your_fallback_secret_key')  # Use environment variable
    app.config['UPLOAD_FOLDER'] = 'app/static/images'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app/database/quotation_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app
