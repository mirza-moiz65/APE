from django.db import models


class Coin(models.Model):
    symbol = models.CharField(max_length=30)
    price = models.CharField(max_length=30)
    market_cap = models.CharField(max_length=30)
    volume = models.CharField(max_length=30)
    price_change_percentage = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.symbol}"

class Post(models.Model):
    crypto = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='posts')
    item_number = models.IntegerField(default=0)
    url = models.URLField(unique=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField()
    sentiment = models.IntegerField(default=0)  # 0 for neutral, 1 for positive, -1 for negative
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source = models.CharField(max_length=100, null=True, blank=True)
