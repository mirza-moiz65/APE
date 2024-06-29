# myapp/routing.py
from django.urls import re_path,path
from showing.consumers import BinanceConsumer

websocket_urlpatterns = [
    path('ws/binance/', BinanceConsumer.as_asgi()),
]