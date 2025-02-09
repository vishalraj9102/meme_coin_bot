from flask import Blueprint, request, jsonify
from app.services.trade_executor import execute_trade

trade_bp = Blueprint("trade", __name__)

@trade_bp.route("/", methods=["POST"])
def trade():
    data = request.json
    token_address = data.get("token_address")
    amount = data.get("amount")
    trade_type = data.get("trade_type", "BUY")  # Default to BUY

    if not token_address or not amount:
        return jsonify({"error": "Missing token address or amount"}), 400

    result = execute_trade(token_address, amount, trade_type)
    return jsonify(result)
