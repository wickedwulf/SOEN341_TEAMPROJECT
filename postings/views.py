from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from .models import TwitterTweets


@login_required(login_url="/accounts/login/")
def post_view(request):
    return render(request, 'postings/posting.html')


@login_required(login_url="/accounts/login/")
def new_tweet(request):
    form = forms.NewPostsForm()
    return render(request, 'postings/tweets.html', {'form': form})


def tweets_latest(request):
    latest_tweets = TwitterTweets.objects.all().order_by('published')                   # pull all the data from our table and store in an object called latest_tweets
    return render(request, 'postings/latest.html', {'latest_tweets': latest_tweets})    # {} part lets us send pulled object array to html file
