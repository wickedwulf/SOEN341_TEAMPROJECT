# Generated by Django 2.1.7 on 2019-03-21 00:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_twitter_tweet_show_encrypted'),
    ]

    operations = [
        migrations.AddField(
            model_name='blocked_users',
            name='block_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='blocked_users',
            name='block_id',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]