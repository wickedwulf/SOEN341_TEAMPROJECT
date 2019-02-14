from django.db import models
from django.utils import timezone


class user_profile(models.Model):
    user_name = models.CharField(max_length=255, default=' ')
    user_profile_name = models.CharField(max_length=255, default=' ')
    user_password = models.CharField(max_length=255, default='**********')
    user_first_name = models.CharField(max_length=255, default=' ')
    user_last_name = models.CharField(max_length=255, default=' ')
    tweet_count = models.IntegerField(default=0)
    follower_count = models.IntegerField(default=0)
    liked_tweet_count = models.IntegerField(default=0)
    created_on = models.DateTimeField(default=timezone.now)
