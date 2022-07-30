# Generated by Django 4.0.4 on 2022-06-04 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_remove_auctionlisting_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='auctionlisting',
            name='user',
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='creator',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='all_creators_listing', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='current_bid',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='watchers',
            field=models.ManyToManyField(blank=True, related_name='watched_listing', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bids',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='createdDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='description',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='start_bid',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='bids',
            name='bid',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='similar_listing', to='auctions.category'),
        ),
    ]