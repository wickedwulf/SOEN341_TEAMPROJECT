from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from .models import TwitterTweets


@login_required(login_url="/accounts/login/")
def post_view(request):
    return render(request, 'postings/posting.html')


# @login_required(login_url="/accounts/login/")         # disabled for now since we don't need login check at the moment
def new_tweet(request):  # handle request for create new tweet
    if request.method == 'POST':                      # check that this is a valid post message from botton and not someone loading page
        postform = forms.NewTweetForm(request.POST)    # get the data from the fields on the page
        if postform.is_valid():                         # check if the form is valid i.e right kind of data
            postform.save()                             # save the post in the database
            return redirect('latest.html')              # send user to latest page to view their tweet
    else:
        postform = forms.NewTweetForm()  # create as an object for the form we want to use (look in forms.py for layout etc..)
    return render(request, 'postings/tweets.html', {'postform': postform})  # the form to the tweets.html


def tweets_latest(request):
    latest_tweets = TwitterTweets.objects.all().order_by('published')                   # pull all the data from our table and store in an object called latest_tweets
    return render(request, 'postings/latest.html', {'latest_tweets': latest_tweets})    # {} part lets us send pulled object array to html file
