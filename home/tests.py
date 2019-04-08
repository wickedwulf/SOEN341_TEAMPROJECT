from django.test import TestCase
from django.urls import reverse, resolve
from home.views import homeactions


class TestUrls(TestCase):

    def test_homeactions_is_resolved(self):
        url = reverse('home:home_actions')
        self.assertEquals(resolve(url).func, homeactions)
