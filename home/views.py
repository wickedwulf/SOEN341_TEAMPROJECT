from django.shortcuts import render, redirect
from . import forms
from .models import TwitterTweets
from accounts.models import user_profile



def homeactions(request):
    userprofile = user_profile.objects.get(user_name=request.user)
    query = request.GET.get('action')
    if "{}".format(query) == "tweet":
        if request.method == 'POST':  # check that this is a valid post message from botton and not someone loading page
            postform = forms.NewTweetForm(request.POST)  # get the data from the fields on the page
            userprofilename = user_profile.objects.get(user_name=request.user) # use username to get profile
            userprofile.tweet_count = userprofile.tweet_count+1  # increase post count by 1
            userprofile.save()   # save updated count
            postform.new_author_id(userprofilename.user_profile_name)
            if postform.is_valid():  # check if the form is valid i.e right kind of data
                postform.save()  # save the post in the database
                return redirect('home:home_actions')  # send user to latest page to view their tweet
    else:
        latest_tweets = TwitterTweets.objects.all().order_by(
            'published')  # pull all the data from our table and store in an object called latest_tweets
        postform = forms.NewTweetForm()
        return render(request, 'home/home.html', {'userprofile': userprofile, 'postform': postform, 'latest_tweets': latest_tweets})
           # need to send all that above data to the page so we can access it for the modal boxes and stuff