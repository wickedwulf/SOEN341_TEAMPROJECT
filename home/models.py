from django.db import models
from django.utils import timezone


class Twitter_Tweet(models.Model):
    tweet_id = models.CharField(max_length=255,  blank=True)
    content = models.TextField(max_length=280, default=None)
    author_id = models.CharField(max_length=255,  blank=True)
    reply_id = models.CharField(max_length=255,  blank=True)
    replies = models.BigIntegerField(default=0)
    favourites = models.IntegerField(default=0)
    published = models.DateTimeField(default=timezone.now)
    media_attachment = models.ImageField(upload_to='site_media', default='default.png', blank=True)


class Liked_Tweets(models.Model):
    author_id = models.CharField(max_length=255, blank=True)
    tweet_id = models.CharField(max_length=255,  blank=True)
    liked_by_user = models.CharField(max_length=255,  blank=True)


class Following_Users(models.Model):
    followed_user = models.CharField(max_length=255, blank=True)
    liked_by_user = models.CharField(max_length=255,  blank=True)


class Replied_To_Tweet(models.Model):
    tweet_id = models.CharField(max_length=255,  blank=True)
