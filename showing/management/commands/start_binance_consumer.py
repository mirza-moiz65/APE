import asyncio
from django.core.management.base import BaseCommand
from showing.consumers import BinanceConsumer

class Command(BaseCommand):
    help = 'Start the Binance WebSocket consumer to update coin prices'

    def handle(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        consumer = BinanceConsumer()
        loop.run_until_complete(consumer.connect())
