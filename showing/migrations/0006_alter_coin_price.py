# Generated by Django 5.0.6 on 2024-06-29 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showing', '0005_alter_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='price',
            field=models.DecimalField(decimal_places=10, max_digits=25),
        ),
    ]
