from django.conf.urls import url
from . import views

app_name = 'home'

urlpatterns = [
    url(r'^home.html', views.homeactions, name='home_actions'),
    url(r'^$', views.homeactions),
]
