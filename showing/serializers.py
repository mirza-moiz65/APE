from rest_framework import serializers
from .models import Coin, Post
from django.utils import timezone
from datetime import timedelta

class CoinSerializer(serializers.ModelSerializer):
    posts_last_24_hours = serializers.SerializerMethodField()

    class Meta:
        model = Coin
        fields = ['symbol', 'price', 'volume', 'market_cap', 'price_change_percentage', 'posts_last_24_hours']

    def get_posts_last_24_hours(self, obj):
        now = timezone.now()
        last_24_hours = now - timedelta(hours=24)
        return Post.objects.filter(crypto=obj, created_at__gte=last_24_hours).count()
