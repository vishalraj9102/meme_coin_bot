import requests
import os

def fetch_meme_coins():
    # ✅ Define DEX_API_URL here to ensure it is available
    DEX_API_URL = os.getenv("DEX_API_URL", "https://api.dexscreener.com/latest/dex/search?q=solana")

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Accept": "application/json"}
    response = requests.get(DEX_API_URL, headers=headers)

    print(f"Status Code: {response.status_code}")  # Debugging
    print(f"Raw Response: {response.text[:500]}")  # Print first 500 chars

    if response.status_code == 200:
        try:
            data = response.json()
            return data.get("pairs", [])
        except requests.exceptions.JSONDecodeError:
            print("Error: Failed to decode JSON response")
            return []
    
    print(f"Error: Received status code {response.status_code}")
    return []
