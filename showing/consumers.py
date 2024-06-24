
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coins.settings')
django.setup()
import json
from channels.generic.websocket import WebsocketConsumer
import requests
import csv 
from showing.views import upload_csv


class RTSPConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        self.fetch_coins_data()

    def disconnect(self, close_code):
       pass

    def receive(self, text_data=None, bytes_data=None):
        pass
    
    def fetch_coins_data(self):
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",  # Specify the currency you want the price in
            "order": "market_cap_desc",  # Order by market capitalization
            "per_page": 250,  # Number of results per page (maximum is 250)
            "page": 1,  # Starting page number
        }
        
        all_coins_data = []
        total_pages = 40  # To fetch 10,000 coins (250 coins per page * 40 pages)
        
        for page in range(1, total_pages + 1):
            params["page"] = page
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                all_coins_data.extend(data)
            else:
                print(f"Failed to fetch data for page {page}")
                break
        
        filename = "coins_data.csv"
        header = ["name", "symbol", "current_price", "total_volume", "market_cap"]

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            for coin in all_coins_data:
                writer.writerow({
                    "name": coin["name"],
                    "symbol": coin["symbol"],
                    "current_price": coin["current_price"],
                    "total_volume": coin["total_volume"],
                    "market_cap": coin["market_cap"],
                })
        
        response = upload_csv(filename)
        if(response.status_code == 200):
            self.send(text_data="200")

    

   

    