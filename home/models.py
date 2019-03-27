""" This file models and structure for the basic site """
from django.db import models
from django.utils import timezone


class TwitterTweet(models.Model):
    """ this model handles the tweets and their encryption """
    tweet_id = models.CharField(max_length=255, blank=True)
    content = models.TextField(max_length=140, default=None)
    encrypted_content = models.TextField(max_length=280, blank=True)
    content_key = models.CharField(max_length=255, blank=True)
    encrypt_content = models.BooleanField(default=False)
    author_id = models.CharField(max_length=255, blank=True)
    replies = models.BigIntegerField(default=0)
    favourites = models.IntegerField(default=0)
    published = models.DateTimeField(default=timezone.now, blank=True)
    media_attachment = models.ImageField(upload_to='site_media', default='default.png', blank=True)
    show_post = models.BooleanField(default=True)
    show_encrypted = models.BooleanField(default=False)


class LikedTweets(models.Model):
    """ This class/table layout is used for the like function """
    author_id = models.CharField(max_length=255, blank=True)
    tweet_id = models.CharField(max_length=255, blank=True)
    liked_by_user = models.CharField(max_length=255, blank=True)


class FollowingUsers(models.Model):
    """ This table is used for our liking function """
    followed_user = models.CharField(max_length=255, blank=True)
    liked_by_user = models.CharField(max_length=255, blank=True)


class PinnedPosts(models.Model):
    """ This class is used for pinning a post """
    pinned_by_user = models.CharField(max_length=255, blank=True)
    tweet_id = models.CharField(max_length=255, blank=True)


class RepliesToTweet(models.Model):
    """ this class is the structure for the replies to tweets """
    tweet_id = models.CharField(max_length=255, blank=True)
    author_id = models.CharField(max_length=255, blank=True)
    reply_id = models.CharField(max_length=255, blank=True)
    content = models.CharField(max_length=280, default=None)
    media_attachment = models.ImageField(upload_to='site_media', default='default.png', blank=True)
    reply_date = models.DateTimeField(default=timezone.now)


class PrivateMessage(models.Model):
    """ This is the class that defines the structure to our private messages """
    private_message_id = models.CharField(max_length=255, blank=True)
    source_author_id = models.CharField(max_length=255, blank=True)
    target_user_id = models.CharField(max_length=255, blank=True)
    content = models.TextField(max_length=280, default=None)
    sent_date = models.DateTimeField(default=timezone.now)
    media_attachment = models.ImageField(upload_to='private_message_images', default='default.png', blank=True)
    seen = models.BooleanField(default=False)
    show_message = models.BooleanField(default=True)


class BlockedUsers(models.Model):
    """ the blocked user structure """
    blocked_user_id = models.CharField(max_length=255, blank=True)
    blocked_by = models.CharField(max_length=255, blank=True)
    block_id = models.CharField(max_length=255, blank=True)
    block_date = models.DateTimeField(default=timezone.now)
