from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.utils import timezone


class user_profile(models.Model):
    user_name = models.CharField(max_length=255)
    user_profile_name = models.CharField(max_length=255)
    user_password = models.CharField(max_length=255, default='**********')
    user_first_name = models.CharField(max_length=255)
    user_last_name = models.CharField(max_length=255)
    user_email = models.CharField(max_length=255)
    user_phone = models.CharField(max_length=255)
    user_country = models.CharField(max_length=255)
    user_city = models.CharField(max_length=255)
    user_website = models.CharField(max_length=500)
    tweet_count = models.IntegerField(default=0)
    follower_count = models.IntegerField(default=0)
    liked_tweet_count = models.IntegerField(default=0)
    created_on = models.DateTimeField(default=timezone.now)
    user_profile_picture: ImageFieldFile = models.ImageField(upload_to='profile_image', blank=True, default="profile_image/default_user.png")
    about_user = models.TextField(max_length=255)
