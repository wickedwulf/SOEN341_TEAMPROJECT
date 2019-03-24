from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import user_profile, user_encryption_key_list
from home.forms import NewTweetForm, Private_Message_Form
from home.models import Twitter_Tweet, Pinned_Posts, Private_Message, Blocked_Users
from . import forms
import os
import hashlib


def signup_view(request):  # create capture for html request from signup page
    if request.method == 'POST':  # check if it's a post message from form
        form = UserCreationForm(request.POST)  # create a djangos user creation form and fill it with submitted data
        if form.is_valid():  # is form valid? i.e user does not exist and requirements are met pass 8 char etc
            user = form.save()  # save the form to the data base form.save  also store the user token in user variable
            login(request, user)  # use djangos login function to login the valid user

            # create a user profile for holding users account data (independent of their login profile)
            userprofile = user_profile()
            userprofile.user_name = user
            random_number = User.objects.make_random_password(length=4, allowed_chars='123456789')  # random number to add to name so they are unique
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
    key_listing = user_encryption_key_list.objects.all()
    my_user_profile = user_profile.objects.get(user_name=request.user)
    my_mail = Private_Message.objects.all()
    # this code filters our blocked people from private  messages
    blocked_list = Blocked_Users.objects.all()
    for blacklisted in blocked_list:
        if blacklisted.blocked_by == my_user_profile.user_profile_name:
            for update_my_mail in my_mail:
                if blacklisted.blocked_user_id == update_my_mail.source_author_id:
                    update_my_mail.show_message = False

    encrypt_key_form = forms.User_Encryption_Form()
    priv_msg_form = Private_Message_Form()
    pinned = Pinned_Posts.objects.all()
    post_form = NewTweetForm()
    userprofile = user_profile.objects.all()
    tweets = Twitter_Tweet.objects.all()

    # block pinned items by users that are blocked
    for blacklisted in blocked_list:
        if blacklisted.blocked_by == my_user_profile.user_profile_name:
            for update_tweet_list in tweets:
                if blacklisted.blocked_user_id == update_tweet_list.author_id:
                    update_tweet_list.show_post = False

    # delete from history
    query = request.GET
    if 'delete' in query.keys():
        if request.method == 'POST':
            try:
                Twitter_Tweet.objects.get(tweet_id="{}".format(query.get('delete'))).delete()
            except Twitter_Tweet.DoesNotExist:
                print("Ignoring does not exist error delete")

        return redirect('accounts:user_profile_view')


    elif 'update' in query.keys():
        if request.method == 'POST':
            updated_form = forms.EditUserProfile(request.POST, request.FILES, user=request.user)  # get the data from the fields on the page
            if updated_form.is_valid():  # check if the form is valid i.e right kind of data
                update_profile = updated_form.save(commit=False)
                updatedb = user_profile.objects.get(user_name=request.user)
                if my_user_profile.user_profile_picture != 'default_user.png' and my_user_profile.user_profile_picture != update_profile.user_profile_picture:  # If the image is not default delete old one otherwise leave current
                    delete_old_profile_pictures(updatedb.user_profile_picture)
                elif update_profile.user_profile_picture != 'default_user.png':
                    updatedb.user_profile_picture = update_profile.user_profile_picture

                updatedb.user_first_name = update_profile.user_first_name
                updatedb.user_last_name = update_profile.user_last_name
                updatedb.user_website = update_profile.user_website
                updatedb.user_city = update_profile.user_city
                updatedb.user_country = update_profile.user_country
                updatedb.user_phone = update_profile.user_phone
                updatedb.user_email = update_profile.user_email
                updatedb.save()

                return redirect('accounts:user_profile_view')
            else:
                return redirect('accounts:user_profile_view')
    # pin the post by storing the id of the post and the user that pinned it

    elif 'pin' in query.keys():
        if request.method == 'POST':
            my_user_profile = user_profile.objects.get(user_name=request.user)
            try:  # used to delete a pinned post
                Pinned_Posts.objects.get(tweet_id="{}".format(query.get('pin')), pinned_by_user=my_user_profile.user_profile_name).delete()
            except Pinned_Posts.DoesNotExist:
                print("Ignoring does not exist error delete")

        return redirect('accounts:user_profile_view')

    elif 'newkeys' in query.keys():
        if request.method == 'POST':
            encrypt_form = forms.User_Encryption_Form(request.POST)
            if encrypt_form.is_valid():  # check if the form is valid i.e right kind of data
                new_key_form = encrypt_form.save(commit=False)
                new_key_form.key_id = hashlib.sha1(new_key_form.encryption_key.encode('utf-8') + new_key_form.user_profile_name.encode('utf-8')).hexdigest()
                new_key_form.encrypt_list_owner = my_user_profile.user_profile_name
                new_key_form.save()

        return redirect('accounts:user_profile_view')

    elif 'deletekey' in query.keys():
        if request.method == 'POST':
            try:
                del_key_listing = user_encryption_key_list.objects.get(key_id="{}".format(query.get('deletekey')))
                del_key_listing.delete()
            except user_encryption_key_list.DoesNotExist:
                print("was not able to delete the key")

        return redirect('accounts:user_profile_view')

    # delete blocked user from block list
    elif 'deleteblockeduser' in query.keys():
        if request.method == 'POST':  # check that this is a valid post message from botton and not someone loading page
            try:
                blocked_user = Blocked_Users.objects.get(block_id="{}".format(query.get('deleteblockeduser')))
                blocked_user.delete()
            except Blocked_Users.DoesNotExist:
                print("Could not delete blocked user")

        return redirect('accounts:user_profile_view')

    # delete users post
    elif 'delete' in query.keys():
        if request.method == 'POST':
            try:
                my_user_profile = user_profile.objects.get(user_name=request.user)
                Twitter_Tweet.objects.get(tweet_id="{}".format(query.get('delete'))).delete()
                my_user_profile.tweet_count = my_user_profile.tweet_count - 1
                my_user_profile.save()
            except Twitter_Tweet.DoesNotExist:
                print("Ignoring does not exist error delete")
        return redirect('accounts:user_profile_view')

    else:
        my_user_profile = user_profile.objects.get(user_name=request.user)
        edituserprofile = forms.EditUserProfile(user=request.user)
        if my_user_profile.tweet_count > 0:
            tweets = Twitter_Tweet.objects.all()
            return render(request, 'accounts/userprofile.html',
                          {'blocked_list': blocked_list, 'key_listing': key_listing, 'encrypt_key_form': encrypt_key_form, 'my_user_profile': my_user_profile,
                           'userprofile': userprofile, 'post_form': post_form,
                           'edituserprofile': edituserprofile, 'tweets': tweets,
                           'pinned_posts': pinned, 'priv_msg_form': priv_msg_form, 'my_mail': my_mail})
        else:
            return render(request, 'accounts/userprofile.html',
                          {'tweets': tweets, 'blocked_list': blocked_list, 'key_listing': key_listing, 'encrypt_key_form': encrypt_key_form, 'userprofile': userprofile, 'post_form': post_form,
                           'edituserprofile': edituserprofile, 'my_user_profile': my_user_profile, 'pinned_posts': pinned, 'priv_msg_form': priv_msg_form, 'my_mail': my_mail})


def user_search_view(request):
    encrypt_key_form = forms.User_Encryption_Form()
    key_listing = user_encryption_key_list.objects.all()
    my_user_profile = user_profile.objects.get(user_name=request.user)
    my_mail = Private_Message.objects.all()
    blocked_list = Blocked_Users.objects.all()
    for blacklisted in blocked_list:
        if blacklisted.blocked_by == my_user_profile.user_profile_name:
            for update_my_mail in my_mail:
                if blacklisted.blocked_user_id == update_my_mail.source_author_id:
                    update_my_mail.show_message = False

    userprofile = user_profile.objects.all()
    priv_msg_form = Private_Message_Form()
    post_form = NewTweetForm()
    pinned = Pinned_Posts.objects.all()
    if request.method == 'GET':
        query = request.GET
        if 'search' in query.keys():
            try:
                my_user_profile = user_profile.objects.get(user_name=request.user)
                searched_profile = user_profile.objects.get(user_profile_name="{}".format(query.get('search')))
                return render(request, 'accounts/search.html',
                              {'blocked_list': blocked_list, 'key_listing': key_listing, 'encrypt_key_form': encrypt_key_form, 'my_user_profile': my_user_profile,
                               'userprofile': userprofile,
                               'post_form': post_form, 'searched_profile': searched_profile,
                               'priv_msg_form': priv_msg_form, 'my_mail': my_mail})
            except user_profile.DoesNotExist:
                Not_Found = "The user " + "{}".format(query.get('search')) + " was not found"
                return render(request, 'accounts/search.html',
                              {'blocked_list': blocked_list, 'key_listing': key_listing, 'encrypt_key_form': encrypt_key_form, 'my_user_profile': my_user_profile,
                               'userprofile': userprofile,
                               'post_form': post_form, 'priv_msg_form': priv_msg_form, 'Not_Found': Not_Found,
                               'my_mail': my_mail})


    else:
        return redirect('accounts:user_profile_view')


def delete_old_profile_pictures(file_name):
    if os.path.isfile(file_name.path):
        os.remove(file_name.path)
