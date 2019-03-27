""" Main forms file for the home app """
from django import forms
from emoji import Emoji
from . import models


class NewTweetForm(forms.ModelForm):
    """ This form is used to setup the tweet form used for creating new tweets """

    class Meta:
        model = models.TwitterTweet
        fields = ['content', 'author_id', 'media_attachment', 'tweet_id', 'encrypted_content', 'content_key', 'replies', 'favourites', 'encrypt_content', 'show_encrypted']
        widgets = {'author_id': forms.HiddenInput(), 'tweet_id': forms.HiddenInput(), 'encrypted_content': forms.HiddenInput(),
                   'replies': forms.HiddenInput(), 'favourites': forms.HiddenInput(),
                   'content': forms.Textarea(attrs={'onkeypress': Emoji.names()}), 'show_encrypted': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(NewTweetForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = "Message:"
        self.fields['content_key'].label = "Encryption Key:"


class PrivateMessageForm(forms.ModelForm):
    """ This form is used for the private message form for creating new messages """

    class Meta:
        model = models.PrivateMessage
        fields = ['target_user_id', 'content', 'media_attachment', 'private_message_id']
        widgets = {'private_message_id': forms.HiddenInput(), 'content': forms.Textarea(attrs={'onkeypress': Emoji.names()})}

    def __init__(self, *args, **kwargs):
        super(PrivateMessageForm, self).__init__(*args, **kwargs)
        self.fields['target_user_id'].label = "To:"


class ReplyToTweetForm(forms.ModelForm):
    """ This form is used for replying to tweets """

    class Meta:
        model = models.RepliesToTweet
        fields = ['tweet_id', 'author_id', 'reply_id', 'content', 'media_attachment']
        widgets = {'tweet_id': forms.HiddenInput(), 'author_id': forms.HiddenInput(), 'reply_id': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(ReplyToTweetForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = "Message:"


class EditPostForm(forms.ModelForm):
    """ This form is used for editing an existing tweet by providing the input types that match the model """

    class Meta:
        model = models.TwitterTweet
        fields = ['content', 'author_id', 'media_attachment', 'tweet_id', 'encrypted_content', 'content_key', 'replies', 'favourites', 'encrypt_content', 'show_encrypted']
        widgets = {'author_id': forms.HiddenInput(), 'tweet_id': forms.HiddenInput(), 'encrypted_content': forms.HiddenInput(),
                   'replies': forms.HiddenInput(), 'favourites': forms.HiddenInput(),
                   'content': forms.Textarea(attrs={'onkeypress': Emoji.names()}), 'show_encrypted': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(EditPostForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = "Message:"
        self.fields['content_key'].label = "Encryption Key:"
