# Generated by Django 5.0.6 on 2024-06-29 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showing', '0004_coin_price_change_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]