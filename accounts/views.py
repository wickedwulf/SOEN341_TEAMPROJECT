from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import user_profile
from home.forms import NewTweetForm
from home.models import TwitterTweets

import datetime


def signup_view(request):  # create capture for html request from signup page
    if request.method == 'POST':  # check if it's a post message from form
        form = UserCreationForm(request.POST)  # create a djangos user creation form and fill it with submitted data
        if form.is_valid():  # is form valid? i.e user does not exist and requirements are met pass 8 char etc
            user = form.save()  # save the form to the data base form.save  also store the user token in user variable
            login(request, user)  # use djangos login function to login the valid user

            # create a user profile for holding users account data (independent of their login profile)
            userprofile = user_profile()
            userprofile.user_name = user
            random_number = User.objects.make_random_password(length=4, allowed_chars='123456789') # random number to add to name so they are unique
            userprofile.user_profile_name = '@' + "{}".format(user) + random_number # set up profile user name for people to use in @ tells
            userprofile.tweet_count = 0
            userprofile.follower_count = 0
            userprofile.liked_tweet_count = 0
            userprofile.user_password = '**********'
            userprofile.user_first_name = ' '
            userprofile.user_last_name = ' '
            userprofile.save()
            # end create user profile

            return redirect('/home/')  # send user to wherever (should be changed later)
    else:  # if it was not valid or correct
        form = UserCreationForm()  # if take the form data provided
    return render(request, 'accounts/signup.html', {'form': form})  # send it back to the login page


def login_view(request):  # create capture for html request from signup page
    if request.method == 'POST':  # check if it's a post message from form
        form = AuthenticationForm(
            data=request.POST)  # because the first bit of data is not the login data we use data=request.post
        if form.is_valid():  # check if its valid
            user = form.get_user()  # store form data in users
            login(request, user)  # pass valid user data to login function
            return redirect('/home/')  # send users to whatever page once logged in
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):  # handle logout requests
    if request.method == 'POST':  # check if its a post message from a button
        logout(request)  # send request to the logout function in django
        return redirect('/')  # send users to homepage of site or someplace


def delete_user_view(request):
    # add stuff to delete user here
    return redirect('/')


def user_profile_view(request):
    userprofile = user_profile.objects.get(user_name=request.user)
    latest_tweets = TwitterTweets.objects.all().order_by('published')
    postform = NewTweetForm()
    return render(request, 'accounts/userprofile.html', {'userprofile': userprofile, 'postform': postform, 'latest_tweets': latest_tweets})
