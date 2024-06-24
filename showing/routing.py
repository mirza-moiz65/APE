# myapp/routing.py
from django.urls import re_path,path
from showing.consumers import RTSPConsumer

websocket_urlpatterns = [
    path('ws/coins/', RTSPConsumer.as_asgi()),
]