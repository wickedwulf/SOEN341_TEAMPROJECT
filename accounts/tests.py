from django.test import TestCase
from django.urls import reverse, resolve
from accounts.views import login_view, user_profile_view , signup_view , user_search_view, logout_view
# Create your tests here.


class TestUrls(TestCase):

    def test_login_is_resolved(self):
        url = reverse('accounts:login')
        self.assertEquals(resolve(url).func,login_view)

    def test_signup_is_resolved(self):
        url = reverse('accounts:signup')
        self.assertEquals(resolve(url).func,signup_view)

    def test_user_profile_is_resolved(self):
        url = reverse('accounts:user_profile_view')
        self.assertEquals(resolve(url).func, user_profile_view)

    def test_user_logout_view_is_resolved(self):
        url = reverse('accounts:logout')
        self.assertEquals(resolve(url).func, logout_view)

    def test_user_search_view_is_resolved(self):
        url = reverse('accounts:user_search_view')
        self.assertEquals(resolve(url).func, user_search_view)


