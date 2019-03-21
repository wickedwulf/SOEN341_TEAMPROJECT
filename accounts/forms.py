from django import forms
from . import models
from accounts.models import user_profile


class EditUserProfile(forms.ModelForm):
    class Meta:
        model = models.user_profile
        fields = ['user_first_name', 'user_last_name', 'user_email', 'user_phone', 'user_country', 'user_city',
                  'user_website', 'about_user', 'user_profile_picture']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EditUserProfile, self).__init__(*args, **kwargs)
        self.initial['user_first_name'] = user_profile.objects.get(user_name=self.user).user_first_name
        self.initial['user_last_name'] = user_profile.objects.get(user_name=self.user).user_last_name
        self.initial['user_email'] = user_profile.objects.get(user_name=self.user).user_email
        self.initial['user_phone'] = user_profile.objects.get(user_name=self.user).user_phone
        self.initial['user_country'] = user_profile.objects.get(user_name=self.user).user_country
        self.initial['user_city'] = user_profile.objects.get(user_name=self.user).user_city
        self.initial['user_website'] = user_profile.objects.get(user_name=self.user).user_website
        self.initial['about_user'] = user_profile.objects.get(user_name=self.user).about_user


class User_Encryption_Form(forms.ModelForm):
    class Meta:
        model = models.user_encryption_key_list
        fields = ['user_profile_name', 'encryption_key', 'enc_keys_notes']
        widgets = {'enc_keys_notes': forms.Textarea()}

    def __init__(self, *args, **kwargs):
        super(User_Encryption_Form, self).__init__(*args, **kwargs)
        self.fields['user_profile_name'].label = "Persons @name:"
        self.fields['encryption_key'].label = "Key value:"
        self.fields['enc_keys_notes'].label = "Notes about key:"
