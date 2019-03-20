from django.contrib import admin
from .models import user_profile, user_encryption_key_list


admin.site.register(user_profile)
admin.site.register(user_encryption_key_list)
