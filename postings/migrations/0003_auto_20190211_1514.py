# Generated by Django 2.1.5 on 2019-02-11 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postings', '0002_auto_20190211_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twittertweets',
            name='content',
            field=models.TextField(max_length=280),
        ),
    ]
