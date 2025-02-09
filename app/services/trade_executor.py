from flask import json
from solana.rpc.api import Client
from solders.transaction import Transaction
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from spl.token.instructions import transfer, TransferParams
import os
import base64
from app import db
from app.models.trade_model import TradeHistory

# Load Solana RPC URL & Private Key
SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
PRIVATE_KEY = os.getenv("SOLANA_PRIVATE_KEY")  # ⚠️ Must be securely stored

solana_client = Client(SOLANA_RPC_URL)

def load_keypair():
    """Load a valid 64-byte private key from Base64 or JSON format."""
    try:
        # Try Base64 Decoding
        private_key_bytes = base64.b64decode(PRIVATE_KEY)
        if len(private_key_bytes) == 64:
            return Keypair.from_bytes(private_key_bytes)
    except Exception:
        pass  # If Base64 fails, try JSON format

    try:
        # Try JSON Decoding (if using keypair.json format)
        private_key_json = json.loads(PRIVATE_KEY)
        private_key_bytes = bytes(private_key_json[:32])  # Extract first 32 bytes (secret key)
        return Keypair.from_bytes(private_key_bytes)
    except Exception:
        raise ValueError("Invalid Solana private key format. Expected 64-byte Base64 or JSON key.")

def execute_trade(token_address, amount, trade_type="BUY"):
    """
    Executes a trade on Solana blockchain (BUY or SELL).
    """
    try:
        # Load wallet keypair
        keypair = load_keypair()

        # Create transaction
        transaction = Transaction()

        # Example: Add a token transfer instruction (Modify this for Raydium Swap)
        instruction = transfer(
            TransferParams(
                program_id=Pubkey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),  # Token program ID
                source=keypair.pubkey(),  # Your wallet address
                dest=Pubkey(token_address),  # Destination (DEX pool address)
                owner=keypair.pubkey(),
                amount=int(amount * 10**6)  # Adjust for token decimals
            )
        )

        transaction.add(instruction)

        # Sign and send transaction
        signature = solana_client.send_transaction(transaction, keypair)
        print(f"Transaction Signature: {signature}")

        # Save trade to database
        trade = TradeHistory(token_address=token_address, trade_type=trade_type, amount=amount, status="SUCCESS", tx_hash=signature)
        db.session.add(trade)
        db.session.commit()

        return {"status": "success", "tx_hash": signature}

    except Exception as e:
        print(f"Trade failed: {str(e)}")

        # Log failed trade
        trade = TradeHistory(token_address=token_address, trade_type=trade_type, amount=amount, status="FAILED", error_message=str(e))
        db.session.add(trade)
        db.session.commit()

        return {"status": "failed", "error": str(e)}
