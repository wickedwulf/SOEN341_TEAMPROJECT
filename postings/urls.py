from django.conf.urls import url
from . import views

app_name = 'postings'

urlpatterns = [
    url(r'^$', views.post_view),
    url(r'^latest.html$', views.tweets_latest, name='latest_tweets'),
    url(r'^tweets.html$', views.new_tweet, name='new_tweet'),
]
