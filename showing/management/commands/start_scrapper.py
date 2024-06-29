import asyncio
import aiohttp
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from asgiref.sync import sync_to_async
from datetime import datetime, timedelta, timezone as dt_timezone
from showing.models import Coin, Post

API_URL = "https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json?filter=top&limit=100&max={max_cursor}"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RATE_LIMIT_DELAY = 1.5  # Delay in seconds between requests

class Command(BaseCommand):
    help = 'Fetch latest posts for all cryptocurrencies'

    def sanitize_string(self, s):
        """Remove null characters from a string."""
        if s:
            return s.replace('\x00', '')
        return s

    async def fetch_posts(self, session, coin, max_cursor):
        page = 1
        while True:
            url = API_URL.format(symbol=coin.symbol.replace('USDT', ''), max_cursor=max_cursor)
            headers = {
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
            }

            print(f"SYMBOL: {coin.symbol}, Page: {page}")
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    posts = data.get('messages', [])
                    print(f"Fetching posts for {coin.symbol}...")
                    print(f"URL: {url}")
                    print(f"Posts: {len(posts)}")
                    print()
                    if not posts:
                        break

                    for item in posts:
                        post_id = str(item['id'])
                        post_exists = await sync_to_async(Post.objects.filter(url=post_id).exists)()

                        post_created_at = datetime.strptime(item['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                        post_created_at = post_created_at.replace(tzinfo=dt_timezone.utc)

                        if post_exists or post_created_at < timezone.now() - timedelta(days=1):
                            return

                        sanitized_content = self.sanitize_string(item['body'])

                        post, created = await sync_to_async(Post.objects.update_or_create)(
                            url=str(item['id']),
                            defaults={
                                'crypto': coin,
                                'item_number': post_id,
                                'content': sanitized_content,
                                'sentiment': 0,  # Assuming sentiment analysis is done later
                                'created_at': post_created_at,
                                'updated_at': timezone.now(),
                                'source': 'stocktwits'
                            }
                        )
                        if created:
                            logger.info(f'Successfully added post: {coin.symbol}')
                    max_cursor = data['cursor']['max']
                else:
                    logger.error(f"Failed to fetch posts for {coin.symbol}: {response.status}")
                    break
            page += 1
            await asyncio.sleep(RATE_LIMIT_DELAY)  # Add delay to prevent hitting rate limits

    async def main(self):
        coins = await sync_to_async(list)(Coin.objects.all())
        async with aiohttp.ClientSession() as session:
            tasks = []
            for coin in coins:
                max_cursor = ''  # Initial cursor value
                tasks.append(self.fetch_posts(session, coin, max_cursor))
                if len(tasks) >= 100:  # Adjust batch size as necessary
                    await asyncio.gather(*tasks)
                    tasks = []
            if tasks:
                await asyncio.gather(*tasks)

    def handle(self, *args, **kwargs):
        asyncio.run(self.main())
