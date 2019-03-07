from django import forms
from . import models
from emoji import Emoji


class NewTweetForm(forms.ModelForm):
    class Meta:
        model = models.Twitter_Tweet
        fields = ['content', 'author_id', 'media_attachment', 'tweet_id', 'reply_id', 'replies', 'favourites']
        widgets = {'author_id': forms.HiddenInput(), 'tweet_id': forms.HiddenInput(), 'reply_id': forms.HiddenInput(),
                   'replies': forms.HiddenInput(), 'favourites': forms.HiddenInput(), 'content': forms.Textarea(attrs={'onkeypress': Emoji.names()})}

