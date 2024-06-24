import requests

def get_binance_data():
    # Endpoint for all tickers
    url = "https://api.binance.com/api/v3/ticker/24hr"
    
    response = requests.get(url)
    data = response.json()

    crypto_details = []

    for coin in data:
        symbol = coin.get('symbol')
        price = coin.get('lastPrice')
        volume = coin.get('quoteVolume')
        
        # To get the name and market cap, you would typically need another endpoint
        # However, Binance does not directly provide name and market cap in the public API
        # For the sake of this example, we'll mock this data as it requires additional steps
        name = "Name for " + symbol  # Placeholder for actual name
        market_cap = float(price) * float(volume)  # Simplified calculation for market cap
        
        crypto_details.append({
            "name": name,
            "symbol": symbol,
            "current_price": price,
            "total_volume": volume,
            "market_cap": market_cap
        })

    return crypto_details[:100]

if __name__ == "__main__":
    data = get_binance_data()
    for coin in data:
        print(coin)
