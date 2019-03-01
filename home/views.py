from django.shortcuts import render, redirect
from . import forms
from .models import Twitter_Tweet
from accounts.models import user_profile
from django.http import HttpResponse
import hashlib


def homeactions(request):
    userprofile = user_profile.objects.get(user_name=request.user)
    query = request.GET.get('action')
    if "{}".format(query) == "tweet": # used for sending parameters from buttons on the same page.. might be a better way *shrug*
        if request.method == 'POST':  # check that this is a valid post message from botton and not someone loading page
            postform = forms.NewTweetForm(request.POST, request.FILES)  # get the data from the fields on the page
            if postform.is_valid():  # check if the form is valid i.e right kind of data
                new_form = postform.save(commit=False)  # save the post in the database
                user_profile_name = user_profile.objects.get(user_name=request.user) # use username to get profile
                userprofile.tweet_count = userprofile.tweet_count+1  # increase post count by 1
                userprofile.save()   # save updated count
                new_form.author_id = user_profile_name.user_profile_name # set the author id
                new_form.tweet_id = hashlib.sha1(new_form.content.encode('utf-8') + new_form.author_id.encode('utf-8')).hexdigest()

                new_form.save() # save updated tweet to db
                return redirect('home:home_actions')  # send user to latest page to view their tweet
        return HttpResponse('somethings wrong - check homeactions code in home/views.py file')
    else:
        latest_tweets = Twitter_Tweet.objects.all().order_by(
            'published')  # pull all the data from our table and store in an object called latest_tweets
        postform = forms.NewTweetForm()
        return render(request, 'home/home.html', {'userprofile': userprofile, 'postform': postform, 'latest_tweets': latest_tweets})
        # need to send all that above data to the page so we can access it for the modal boxes and stuff
