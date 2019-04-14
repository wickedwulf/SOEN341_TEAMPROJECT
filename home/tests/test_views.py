from django.test import TestCase
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from home.views import homeactions
from mixer.backend.django import mixer
from home.models import TwitterTweet
from accounts.models import UserProfile


class TestViews(TestCase):

    def test_home_action_invalid_user(self):
        """ Used to test redirecting an invalid user to the root page """
        path = reverse('home:home_actions')
        request = RequestFactory().get(path, data=None)
        request.user = AnonymousUser()
        response = homeactions(request)
        assert '/index.html' in response.url

    def test_home_action_invalid_delete_tweet_id(self):
        """ Used to test deleting a tweet that does not exist """
        path = reverse('home:home_actions')
        mixer.blend(UserProfile, user_name='admin', user_profile_name='@admin')
        request = RequestFactory().post(path + '?delete=123456')
        request.user = 'admin'
        homeactions(request)
        self.assertRaises(TwitterTweet.DoesNotExist)

    def test_home_action_delete_tweet_id(self):
        """ Used to create a dummy test tweet then pass it's ID and delete it using the view """
        mixer.blend(TwitterTweet, content='test', tweet_id='test_id_tweet_1', author_id='@admin')
        mixer.blend(UserProfile, user_name='admin', user_profile_name='@admin')
        path = reverse('home:home_actions')
        request = RequestFactory().post(path + '?delete=test_id_tweet')
        request.user = 'admin'
        response = homeactions(request)
        assert response.status_code == 302
        self.assertRaises(TwitterTweet.DoesNotExist)
