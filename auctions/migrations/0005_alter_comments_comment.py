# Generated by Django 5.0.6 on 2024-07-31 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_remove_bid_bid_listing_bid_bid_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
