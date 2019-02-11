from django.db import models
from django.utils import timezone


# Create your models here.

class TwitterTweets(models.Model):
    tweet_id = models.CharField(max_length=255)
    content = models.TextField(max_length=280)
    author_id = models.CharField(max_length=255)
    reply_id = models.CharField(max_length=255)
    replies = models.BigIntegerField
    favourites = models.IntegerField
    published = models.DateTimeField(default=timezone.now)
