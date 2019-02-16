from django import forms
from . import models


class NewTweetForm(forms.ModelForm):
    class Meta:
        model = models.TwitterTweets
        fields = ['content', 'author_id']
        widgets = {'author_id': forms.HiddenInput()}

    def new_author_id(self, value):
        data = self.data.copy()
        data['author_id'] = value
        self.data = data
