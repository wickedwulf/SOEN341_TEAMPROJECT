from django import forms
from . import models
from django.utils import timezone



class NewTweetForm(forms.ModelForm):
    class Meta:
        model = models.TwitterTweets
        fields = ['content', 'author_id']
