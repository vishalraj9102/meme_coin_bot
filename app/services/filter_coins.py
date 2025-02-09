def filter_profitable_coins(coins, min_growth=5, min_liquidity=10000):
    profitable = []
    for coin in coins:
        name = coin.get("name", "Unknown")
        price_change = float(coin.get("priceChange", {}).get("h24", 0))

        # 🔹 Debugging: Print full coin data
        print(f"DEBUG: Coin Data: {coin}")

        # 🔹 Fix: Ensure liquidity is a number, not a dict
        liquidity_data = coin.get("liquidity", 0)
        if isinstance(liquidity_data, dict):
            liquidity = float(liquidity_data.get("usd", 0))  # Extract 'usd' value if liquidity is a dict
        else:
            liquidity = float(liquidity_data)  # Convert if it's already a number

        print(f"Checking Coin: {name}, Growth: {price_change}%, Liquidity: {liquidity}")

        if price_change > min_growth and liquidity >= min_liquidity:
            profitable.append(coin)

    print(f"Filtered Coins: {profitable}")
    return profitable
