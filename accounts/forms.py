from django import forms
from . import models
from accounts.models import user_profile


class EditUserProfile(forms.ModelForm):
    class Meta:
        model = models.user_profile
        fields = ['user_first_name', 'user_last_name', 'user_email', 'user_phone', 'user_country', 'user_city',
                  'user_website', 'about_user', 'user_profile_picture']
