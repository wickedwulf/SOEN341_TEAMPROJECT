from django.conf.urls import url
from . import views

app_name = 'postings'

urlpatterns = [
    url(r'^$', views.post_view)
    #url(r'^postings/$', views.)
]
