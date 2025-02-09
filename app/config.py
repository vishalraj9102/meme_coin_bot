import os

class Config:
    SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
    DEX_API_URL = "https://api.dexscreener.com/latest/dex/pairs/solana"

config = Config()
