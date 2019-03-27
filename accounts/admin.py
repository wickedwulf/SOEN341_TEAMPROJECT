"""" Admin panel setup """
from django.contrib import admin
from .models import UserProfile, UserEncryptionKeyList


admin.site.register(UserProfile)
admin.site.register(UserEncryptionKeyList)
