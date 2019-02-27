# Generated by Django 2.1.5 on 2019-02-14 12:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterTweets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet_id', models.CharField(max_length=255)),
                ('content', models.TextField(max_length=280)),
                ('author_id', models.CharField(max_length=255)),
                ('reply_id', models.CharField(max_length=255)),
                ('published', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]