from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from solana.rpc.api import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Load database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "postgresql://postgres:root@localhost:5432/meme_coin_db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database with Flask app
    db.init_app(app)

    # Initialize Flask-Migrate
    Migrate(app, db)

    # Solana RPC Client
    SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL")
    solana_client = Client(SOLANA_RPC_URL)

    # DEX Screener API Configuration
    DEX_API_URL = "https://api.dexscreener.com/latest/dex/search?q=solana"

    # Import and register blueprints (routes)
    from app.routes.scan import scan_bp
    from app.routes.trade import trade_bp

    app.register_blueprint(scan_bp, url_prefix="/scan")
    app.register_blueprint(trade_bp, url_prefix="/trade")

    return app
