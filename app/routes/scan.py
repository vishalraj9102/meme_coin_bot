from flask import Blueprint, jsonify
from app.services.fetch_coins import fetch_meme_coins
from app.services.filter_coins import filter_profitable_coins

scan_bp = Blueprint("scan", __name__)

@scan_bp.route("/", methods=["GET"])
def scan_meme_coins():
    coins = fetch_meme_coins()
    filtered_coins = filter_profitable_coins(coins)
    return jsonify({"filtered_coins": filtered_coins})