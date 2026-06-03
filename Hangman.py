from flask import Flask
from dotenv import load_dotenv
import os
from models import Db
from routes import bp as routes_bp

# Load environment variables from the .env file
load_dotenv()

App = Flask(__name__)

# Secure secret key loaded from env
App.secret_key = os.environ.get("FLASK_SECRET_KEY", "giki_coding_fallback_secret_key_18273")

# Database Configuration
DbUrl = os.environ.get('DATABASE_URL', 'postgresql+pg8000://postgres:pgadmin4@localhost:5432/Hangman')
if DbUrl.startswith("postgres://"):
    DbUrl = DbUrl.replace("postgres://", "postgresql+pg8000://", 1)

App.config['SQLALCHEMY_DATABASE_URI'] = DbUrl
App.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
Db.init_app(App)

# Register routes blueprint
App.register_blueprint(routes_bp)

with App.app_context():
    Db.create_all()

if __name__ == '__main__':
    App.run(debug=True)