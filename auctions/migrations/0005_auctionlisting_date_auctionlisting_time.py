# Generated by Django 4.0.4 on 2022-06-03 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='time',
            field=models.TimeField(blank=True, default=None, null=True),
        ),
    ]
