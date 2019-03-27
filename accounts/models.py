"""" Class / database structure for the user profile and encryption list """
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.utils import timezone


class UserProfile(models.Model):
    """" Class for handling the user profile information """
    user_name = models.CharField(max_length=255)
    user_profile_name = models.CharField(max_length=255)
    user_password = models.CharField(max_length=255, default='**********')
    user_first_name = models.CharField(max_length=255, default=' ', blank=True)
    user_last_name = models.CharField(max_length=255, default=' ', blank=True)
    user_email = models.CharField(max_length=255, default=' ', blank=True)
    user_phone = models.CharField(max_length=255, default=' ', blank=True)
    user_country = models.CharField(max_length=255, default=' ', blank=True)
    user_city = models.CharField(max_length=255, default=' ', blank=True)
    user_website = models.CharField(max_length=500, default=' ', blank=True)
    tweet_count = models.IntegerField(default=0)
    follower_count = models.IntegerField(default=0)
    user_mails = models.IntegerField(default=0)
    liked_tweet_count = models.IntegerField(default=0)
    created_on = models.DateTimeField(default=timezone.now)
    user_profile_picture: ImageFieldFile = models.ImageField(upload_to='profile_image', blank=True, default="default_user.png")
    about_user = models.TextField(max_length=255, default=' ', blank=True)


class UserEncryptionKeyList(models.Model):
    """" Class for handling the user encryption key list for the encoded messages """
    user_profile_name = models.CharField(max_length=255, blank=True)
    encryption_key = models.CharField(max_length=255, blank=True)
    enc_keys_notes = models.TextField(max_length=255, blank=True)
    encrypt_list_owner = models.TextField(max_length=255, blank=True)
    key_id = models.TextField(max_length=255)
