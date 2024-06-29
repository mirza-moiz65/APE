import asyncio
import json
import websockets
from django.db import connections
from asgiref.sync import sync_to_async

class BinanceConsumer:
    async def connect(self):
        print("Connecting to Binance WebSocket...")
        await self.fetch_prices()

    async def fetch_prices(self):
        url = "wss://stream.binance.com:9443/ws/!ticker@arr"
        async with websockets.connect(url, ping_interval=180, ping_timeout=600) as websocket:
            while True:
                try:
                    message = await websocket.recv()
                    await self.update_prices(message)
                except websockets.ConnectionClosed:
                    print("Connection closed, reconnecting...")
                    await asyncio.sleep(5)
                    await self.fetch_prices()
                except Exception as e:
                    print(f"Error: {e}")
                    await asyncio.sleep(5)

    async def update_prices(self, message):
        data = json.loads(message)
        for ticker in data:
            symbol = ticker['s']
            if symbol.endswith('USDT'):
                price = ticker['c']
                volume = ticker['v']
                market_cap = ticker['q']
                price_change_percentage = ticker['P']

                await self.update_coin_data(symbol, price, volume, market_cap, price_change_percentage)

    @sync_to_async
    def update_coin_data(self, symbol, price, volume, market_cap, price_change_percentage):
        from .models import Coin
        print(f"Updating {symbol} price to {price}")

        try:
            coin = Coin.objects.get(symbol=symbol)
            coin.price = price
            coin.volume = volume
            coin.market_cap = market_cap
            coin.price_change_percentage = price_change_percentage
            coin.save()
        except Coin.DoesNotExist:
            Coin.objects.create(
                symbol=symbol, price=price, volume=volume, market_cap=market_cap, price_change_percentage=price_change_percentage
            )
