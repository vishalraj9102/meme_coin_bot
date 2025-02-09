from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class MemeCoin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_address = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    liquidity = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TradeHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_address = db.Column(db.String(100), nullable=False)
    trade_type = db.Column(db.String(10), nullable=False)  # BUY / SELL
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="PENDING")  # SUCCESS, FAILED
    tx_hash = db.Column(db.String(100), nullable=True)  # Blockchain Transaction ID
    error_message = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)