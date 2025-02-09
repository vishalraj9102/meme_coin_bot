from solana.rpc.api import Client
import os

# Load RPC URL from environment variables
SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")

# Initialize Solana Client
solana_client = Client(SOLANA_RPC_URL)

def get_balance(wallet_address):
    """Fetch Solana (SOL) balance of a wallet."""
    response = solana_client.get_balance(wallet_address)
    return response["result"]["value"] / 10**9  # Convert lamports to SOL
