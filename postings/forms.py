from django import forms
from . import models

class NewPostsForm(forms.ModelForm):
    class Meta:
        model = models.TwitterTweets
        fields = ['content']

