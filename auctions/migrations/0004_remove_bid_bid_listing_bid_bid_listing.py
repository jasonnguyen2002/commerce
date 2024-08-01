# Generated by Django 5.0.6 on 2024-07-30 15:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_listing_listing_setprice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='bid_listing',
        ),
        migrations.AddField(
            model_name='bid',
            name='bid_listing',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
            preserve_default=False,
        ),
    ]