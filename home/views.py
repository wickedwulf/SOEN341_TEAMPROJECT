from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from .models import Twitter_Tweet, Following_Users, Liked_Tweets
from accounts.models import user_profile
import hashlib


def homeactions(request):
    userprofile = user_profile.objects.get(user_name=request.user)
    query = request.GET

    # used for doing new tweets
    if 'action' in query.keys():  # used for sending parameters from buttons on the same page.. might be a better way *shrug*
        if "{}".format(query.get('action')) == "tweet":
            if request.method == 'POST':  # check that this is a valid post message from botton and not someone loading page
                postform = forms.NewTweetForm(request.POST, request.FILES)  # get the data from the fields on the page
                if postform.is_valid():  # check if the form is valid i.e right kind of data
                    new_form = postform.save(commit=False)  # save the post in the database
                    user_profile_name = user_profile.objects.get(user_name=request.user)  # use username to get profile
                    userprofile.tweet_count = userprofile.tweet_count + 1  # increase post count by 1
                    userprofile.save()  # save updated count
                    new_form.author_id = user_profile_name.user_profile_name  # set the author id
                    new_form.tweet_id = hashlib.sha1(
                        new_form.content.encode('utf-8') + new_form.author_id.encode('utf-8')).hexdigest()

                    new_form.save()  # save updated tweet to db
                    return redirect('home:home_actions')  # send user to latest page to view their tweet
                return HttpResponse('somethings wrong - check homeactions code in home/views.py file')
    # This handles looking for the tweet ID from the passed variables and liking it
    elif 'liked' in query.keys():
        if request.method == 'POST':
            postform = forms.NewTweetForm()
            like_tweet = Twitter_Tweet.objects.get(tweet_id="{}".format(query.get('liked')))
            if Liked_Tweets.objects.all().count() > 0:
                try:
                    Liked_Tweets.objects.get(tweet_id="{}".format(query.get('liked')), liked_by_user=userprofile.user_profile_name).delete()
                    print("deleted like from tweet")
                    userprofile.liked_tweet_count = userprofile.liked_tweet_count - 1
                    userprofile.save()
                    like_tweet.favourites = like_tweet.favourites - 1
                    like_tweet.save()
                    following = Following_Users.objects.all()
                    latest_tweets = Twitter_Tweet.objects.all().order_by('published')
                    return render(request, 'home/home.html', {'userprofile': userprofile, 'postform': postform, 'latest_tweets': latest_tweets, 'following': following})
                except Liked_Tweets.DoesNotExist:
                    print("Ignoring does not exist error")

            print("Add like to tweet")
            like_add = Liked_Tweets()
            like_tweet.favourites = like_tweet.favourites + 1
            userprofile.liked_tweet_count = userprofile.liked_tweet_count + 1
            like_add.author_id = like_tweet.author_id
            like_add.tweet_id = like_tweet.tweet_id
            like_add.liked_by_user = userprofile.user_profile_name
            like_add.save()
            userprofile.save()
            like_tweet.save()
        following = Following_Users.objects.all()
        latest_tweets = Twitter_Tweet.objects.all().order_by(
            'published')  # pull all the data from our table and store in an object called latest_tweets
        return render(request, 'home/home.html', {'userprofile': userprofile, 'postform': postform, 'latest_tweets': latest_tweets, 'following': following})

    elif 'delete' in query.keys():
        if request.method == 'POST':
            try:
                Twitter_Tweet.objects.get(tweet_id="{}".format(query.get('delete'))).delete()
            except Twitter_Tweet.DoesNotExist:
                print("Ignoring does not exist error delete")
        following = Following_Users.objects.all()
        postform = forms.NewTweetForm()
        latest_tweets = Twitter_Tweet.objects.all().order_by('published')  # pull all the data from our table and store in an object called latest_tweets
        return render(request, 'home/home.html',
                      {'userprofile': userprofile, 'postform': postform, 'latest_tweets': latest_tweets, 'following': following})


    elif 'follow' in query.keys():
        if request.method == 'POST':
            try:
                Following_Users.objects.get(followed_user="{}".format(query.get('follow')), liked_by_user=userprofile.user_profile_name).delete()
                follow_profile = user_profile.objects.get(user_profile_name="{}".format(query.get('follow')))
                follow_profile.follower_count = follow_profile.follower_count + 1
                follow_profile.save()
                print("deleted like from tweet")
                following = Following_Users.objects.all()
                postform = forms.NewTweetForm()
                latest_tweets = Twitter_Tweet.objects.all().order_by('published')
                return render(request, 'home/home.html', {'userprofile': userprofile, 'postform': postform, 'latest_tweets': latest_tweets, 'following': following})

            except Following_Users.DoesNotExist:
                print("Ignoring does not exist error delete")

        follow_add = Following_Users()
        follow_add.liked_by_user = userprofile.user_profile_name
        follow_add.followed_user = "{}".format(query.get('follow'))
        follow_add.save()
        follow_profile = user_profile.objects.get(user_profile_name="{}".format(query.get('follow')))
        follow_profile.follower_count = follow_profile.follower_count + 1
        follow_profile.save()
        latest_tweets = Twitter_Tweet.objects.all().order_by('published')  # pull all the data from our table and store in an object called latest_tweets
        postform = forms.NewTweetForm()
        following = Following_Users.objects.all()
        return render(request, 'home/home.html', {'userprofile': userprofile, 'postform': postform, 'latest_tweets': latest_tweets, 'following': following})

    # need to send all that above data to the page so we can access it for the modal boxes and stuff
    else:
        following = Following_Users.objects.all()
        latest_tweets = Twitter_Tweet.objects.all().order_by('published')  # pull all the data from our table and store in an object called latest_tweets
        postform = forms.NewTweetForm()
        return render(request, 'home/home.html',
                      {'userprofile': userprofile, 'postform': postform, 'latest_tweets': latest_tweets, 'following': following})
    # need to send all that above data to the page so we can access it for the modal boxes and stuff
