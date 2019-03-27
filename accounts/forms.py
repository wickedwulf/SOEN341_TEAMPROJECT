"""" Forms file that provides inputs and such to the html aspect based on the main classes """
from django import forms
from accounts.models import UserProfile
from . import models


class EditUserProfile(forms.ModelForm):
    """" This form is used for editing the basic user profile """

    class Meta:
        model = models.UserProfile
        fields = ['user_first_name', 'user_last_name', 'user_email', 'user_phone', 'user_country', 'user_city',
                  'user_website', 'about_user', 'user_profile_picture']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EditUserProfile, self).__init__(*args, **kwargs)
        self.initial['user_first_name'] = UserProfile.objects.get(user_name=self.user).user_first_name
        self.initial['user_last_name'] = UserProfile.objects.get(user_name=self.user).user_last_name
        self.initial['user_email'] = UserProfile.objects.get(user_name=self.user).user_email
        self.initial['user_phone'] = UserProfile.objects.get(user_name=self.user).user_phone
        self.initial['user_country'] = UserProfile.objects.get(user_name=self.user).user_country
        self.initial['user_city'] = UserProfile.objects.get(user_name=self.user).user_city
        self.initial['user_website'] = UserProfile.objects.get(user_name=self.user).user_website
        self.initial['about_user'] = UserProfile.objects.get(user_name=self.user).about_user


class UserEncryptionForm(forms.ModelForm):
    """" This form allows a user to input new encryption keys to decode emoji encrypted messages """

    class Meta:
        model = models.UserEncryptionKeyList
        fields = ['user_profile_name', 'encryption_key', 'enc_keys_notes']
        widgets = {'enc_keys_notes': forms.Textarea()}

    def __init__(self, *args, **kwargs):
        super(UserEncryptionForm, self).__init__(*args, **kwargs)
        self.fields['user_profile_name'].label = "Persons @name:"
        self.fields['encryption_key'].label = "Key value:"
        self.fields['enc_keys_notes'].label = "Notes about key:"
