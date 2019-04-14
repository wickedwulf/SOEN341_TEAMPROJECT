from django.test import TestCase
from home.forms import NewTweetForm, PrivateMessageForm


class TestForms(TestCase):

    def test_valid_tweet_form(self):
        """ Used to test the new tweet form """
        form = NewTweetForm(data={'content': 'test tweet', 'encrypt_content': False, 'content_key': 'test', 'tweet_id': '23', 'author_id': '@admin', 'replies': 0, 'favourites': 0})
        self.assertTrue(form.is_valid())

    def test_invalid_tweet_form(self):
        """ used to make sure an empty form fails """
        form = NewTweetForm(data={})
        self.assertFalse(form.is_valid())

    def test_valid_pmsg_form(self):
        """ used to test the private message form"""
        form = PrivateMessageForm(data={'content': 'test tweet', 'target_user_id': '@admin'})
        self.assertTrue(form.is_valid())

    def test_invalid_pmsg_form(self):
        """ used to make sure an empty form fails """
        form = PrivateMessageForm(data={})
        self.assertFalse(form.is_valid())
