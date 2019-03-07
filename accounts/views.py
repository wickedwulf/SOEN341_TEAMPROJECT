from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import user_profile
from home.forms import NewTweetForm
from home.models import Twitter_Tweet
from . import forms


def signup_view(request):  # create capture for html request from signup page
    if request.method == 'POST':  # check if it's a post message from form
        form = UserCreationForm(request.POST)  # create a djangos user creation form and fill it with submitted data
        if form.is_valid():  # is form valid? i.e user does not exist and requirements are met pass 8 char etc
            user = form.save()  # save the form to the data base form.save  also store the user token in user variable
            login(request, user)  # use djangos login function to login the valid user

            # create a user profile for holding users account data (independent of their login profile)
            userprofile = user_profile()
            userprofile.user_name = user
            random_number = User.objects.make_random_password(length=4,
                                                              allowed_chars='123456789')  # random number to add to name so they are unique
            userprofile.user_profile_name = '@' + "{}".format(
                user) + random_number  # set up profile user name for people to use in @ tells
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
    if request.method == 'POST':
        updated_form = forms.EditUserProfile(request.POST,
                                             request.FILES)  # get the data from the fields on the page
        if updated_form.is_valid():  # check if the form is valid i.e right kind of data
            update_image_file = updated_form.save(commit=False)
            updatedb = user_profile.objects.get(user_name=request.user)
            updatedb.user_profile_picture = update_image_file.user_profile_picture
            updatedb.user_first_name = update_image_file.user_first_name
            updatedb.user_last_name = update_image_file.user_last_name
            updatedb.user_website = update_image_file.user_website
            updatedb.user_city = update_image_file.user_city
            updatedb.user_country = update_image_file.user_country
            updatedb.user_phone = update_image_file.user_phone
            updatedb.user_email = update_image_file.user_email
            updatedb.save()
            return redirect('accounts:user_profile_view')

    else:
        userprofile = user_profile.objects.get(user_name=request.user)
        postform = NewTweetForm()
        edituserprofile = forms.EditUserProfile()
        if userprofile.tweet_count > 0:
            my_tweets = Twitter_Tweet.objects.all().filter(author_id=userprofile.user_profile_name)
            return render(request, 'accounts/userprofile.html',
                          {'userprofile': userprofile, 'postform': postform, 'edituserprofile': edituserprofile,
                           'my_tweets': my_tweets})
        else:
            return render(request, 'accounts/userprofile.html',
                          {'userprofile': userprofile, 'postform': postform, 'edituserprofile': edituserprofile})
    # delete from history
    query = request.GET
    if 'delete' in query.keys():
        if request.method == 'POST':
            try:
                Twitter_Tweet.objects.get(tweet_id="{}".format(query.get('delete'))).delete()
            except Twitter_Tweet.DoesNotExist:
                print("Ignoring does not exist error delete")

        userprofile = user_profile.objects.get(user_name=request.user)
        postform = NewTweetForm()
        edituserprofile = forms.EditUserProfile()
        my_tweets = Twitter_Tweet.objects.all().filter(author_id=userprofile.user_profile_name)
        return render(request, 'accounts/userprofile.html',
                      {'userprofile': userprofile, 'postform': postform, 'edituserprofile': edituserprofile,
                       'my_tweets': my_tweets})
