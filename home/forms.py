from django import forms
from . import models
from emoji import Emoji


class NewTweetForm(forms.ModelForm):
    class Meta:
        model = models.Twitter_Tweet
        fields = ['content', 'author_id', 'media_attachment', 'tweet_id', 'encrypted_content', 'content_key', 'replies', 'favourites', 'encrypt_content', 'show_encrypted']
        widgets = {'author_id': forms.HiddenInput(), 'tweet_id': forms.HiddenInput(), 'encrypted_content': forms.HiddenInput(),
                   'replies': forms.HiddenInput(), 'favourites': forms.HiddenInput(),
                   'content': forms.Textarea(attrs={'onkeypress': Emoji.names()}), 'show_encrypted': forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        super(NewTweetForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = "Message:"
        self.fields['content_key'].label = "Encryption Key:"

class Private_Message_Form(forms.ModelForm):
    class Meta:
        model = models.Private_Message
        fields = ['target_user_id', 'content', 'media_attachment', 'private_message_id']
        widgets = {'private_message_id': forms.HiddenInput(), 'content': forms.Textarea(attrs={'onkeypress': Emoji.names()})}

    def __init__(self, *args, **kwargs):
        super(Private_Message_Form, self).__init__(*args, **kwargs)
        self.fields['target_user_id'].label = "To:"

class Reply_To_Tweet_Form(forms.ModelForm):
    class Meta:
        model = models.Replies_To_Tweet
        fields = ['tweet_id', 'author_id', 'reply_id', 'content', 'media_attachment']
        widgets = {'tweet_id': forms.HiddenInput(), 'author_id': forms.HiddenInput(), 'reply_id': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(Reply_To_Tweet_Form, self).__init__(*args, **kwargs)
        self.fields['content'].label = "Message:"


class Edit_Post_Form(forms.ModelForm):
    class Meta:
        model = models.Twitter_Tweet
        fields = ['content', 'author_id', 'media_attachment', 'tweet_id', 'encrypted_content', 'content_key', 'replies', 'favourites', 'encrypt_content', 'show_encrypted']
        widgets = {'author_id': forms.HiddenInput(), 'tweet_id': forms.HiddenInput(), 'encrypted_content': forms.HiddenInput(),
                   'replies': forms.HiddenInput(), 'favourites': forms.HiddenInput(),
                   'content': forms.Textarea(attrs={'onkeypress': Emoji.names()}), 'show_encrypted': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(Edit_Post_Form, self).__init__(*args, **kwargs)
        self.fields['content'].label = "Message:"
        self.fields['content_key'].label = "Encryption Key:"
