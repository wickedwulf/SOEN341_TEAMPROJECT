"""" This is the accounts view that handles user profile creation and logging in etc """
import os
import hashlib
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # , PasswordChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from home.models import TwitterTweet, PinnedPosts, PrivateMessage, BlockedUsers
from home.forms import NewTweetForm, PrivateMessageForm
from .models import UserProfile, UserEncryptionKeyList

from . import forms


def signup_view(request):  # create capture for html request from signup page
    """" Sign up view to handle the new user account creation """
    # check if it's a post message from form
    if request.method == 'POST':
        # create a djangos user creation form and fill it with submitted data
        form = UserCreationForm(request.POST)
        # is form valid? i.e user does not exist and requirements are met pass 8 char etc
        if form.is_valid():
            # save the form to the data base form.save  also store the user token in user variable
            user = form.save()
            # use djangos login function to login the valid user
            login(request, user)
            # create a user profile for holding users account data (independent of their login profile)
            user_profile = UserProfile()
            user_profile.user_name = user
            # random number to add to name so they are unique
            random_number = User.objects.make_random_password(length=4, allowed_chars='123456789')
            # set up profile user name for people to use in @ tells
            user_profile.user_profile_name = '@' + "{}".format(
                user) + random_number
            user_profile.tweet_count = 0
            user_profile.follower_count = 0
            user_profile.liked_tweet_count = 0
            user_profile.user_password = '**********'
            user_profile.user_first_name = ' '
            user_profile.user_last_name = ' '
            # end create user profile
            user_profile.save()
            # send user to wherever (should be changed later)
            return redirect('/home/')
    # if take the form data provided
    form = UserCreationForm()
    # send it back to the login page
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """" handle login requests """
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


def logout_view(request):  #
    """" handle logout requests """
    if request.method == 'POST':  # check if its a post message from a button
        logout(request)  # send request to the logout function in django
    return redirect('/')  # send users to homepage of site or someplace


def user_profile_view(request):
    """" Handles all the main requests of the userprofile page """
    key_listing = UserEncryptionKeyList.objects.all()
    my_user_profile = UserProfile.objects.get(user_name=request.user)
    edit_user_profile = forms.EditUserProfile(user=request.user)
    my_mail = PrivateMessage.objects.all()
    # this code filters our blocked people from private  messages
    blocked_list = BlockedUsers.objects.all()
    for blacklisted in blocked_list:
        if blacklisted.blocked_by == my_user_profile.user_profile_name:
            for update_my_mail in my_mail:
                if blacklisted.blocked_user_id == update_my_mail.source_author_id:
                    update_my_mail.show_message = False

    encrypt_key_form = forms.UserEncryptionForm()
    priv_msg_form = PrivateMessageForm()
    pinned = PinnedPosts.objects.all()
    post_form = NewTweetForm()
    user_profile = UserProfile.objects.all()
    tweets = TwitterTweet.objects.all().order_by('published').reverse()

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
                TwitterTweet.objects.get(tweet_id="{}".format(query.get('delete'))).delete()
            except TwitterTweet.DoesNotExist:
                print("Ignoring does not exist error delete")
            return redirect('accounts:user_profile_view')

    elif 'update' in query.keys():
        if request.method == 'POST':
            updated_form = forms.EditUserProfile(request.POST, request.FILES, user=request.user)  # get the data from the fields on the page
            if updated_form.is_valid():  # check if the form is valid i.e right kind of data
                update_profile = updated_form.save(commit=False)
                update_db = UserProfile.objects.get(user_name=request.user)
                if my_user_profile.user_profile_picture != 'default_user.png' and my_user_profile.user_profile_picture != update_profile.user_profile_picture:  # If the image is not default delete old one otherwise leave current
                    delete_old_profile_pictures(update_db.user_profile_picture)
                elif update_profile.user_profile_picture != 'default_user.png':
                    update_db.user_profile_picture = update_profile.user_profile_picture
                update_db.user_first_name = update_profile.user_first_name
                update_db.user_last_name = update_profile.user_last_name
                update_db.user_website = update_profile.user_website
                update_db.user_city = update_profile.user_city
                update_db.user_country = update_profile.user_country
                update_db.user_phone = update_profile.user_phone
                update_db.user_email = update_profile.user_email
                update_db.save()
                return redirect('accounts:user_profile_view')

    # pin the post by storing the id of the post and the user that pinned it
    elif 'pin' in query.keys():
        if request.method == 'POST':
            my_user_profile = UserProfile.objects.get(user_name=request.user)
            try:  # used to delete a pinned post
                PinnedPosts.objects.get(tweet_id="{}".format(query.get('pin')), pinned_by_user=my_user_profile.user_profile_name).delete()
            except PinnedPosts.DoesNotExist:
                print("Ignoring does not exist error delete")

        return redirect('accounts:user_profile_view')

    elif 'newkeys' in query.keys():
        if request.method == 'POST':
            encrypt_form = forms.UserEncryptionForm(request.POST)
            if encrypt_form.is_valid():  # check if the form is valid i.e right kind of data
                new_key_form = encrypt_form.save(commit=False)
                new_key_form.key_id = hashlib.sha1(new_key_form.encryption_key.encode('utf-8') + new_key_form.user_profile_name.encode('utf-8')).hexdigest()
                new_key_form.encrypt_list_owner = my_user_profile.user_profile_name
                new_key_form.save()

        return redirect('accounts:user_profile_view')

    elif 'deletekey' in query.keys():
        if request.method == 'POST':
            try:
                del_key_listing = UserEncryptionKeyList.objects.get(key_id="{}".format(query.get('deletekey')))
                del_key_listing.delete()
            except UserEncryptionKeyList.DoesNotExist:
                print("was not able to delete the key")

        return redirect('accounts:user_profile_view')

    # delete blocked user from block list
    elif 'deleteblockeduser' in query.keys():
        if request.method == 'POST':  # check that this is a valid post message from botton and not someone loading page
            try:
                blocked_user = BlockedUsers.objects.get(block_id="{}".format(query.get('deleteblockeduser')))
                blocked_user.delete()
            except BlockedUsers.DoesNotExist:
                print("Could not delete blocked user")

        return redirect('accounts:user_profile_view')

    # delete users post
    elif 'delete' in query.keys():
        if request.method == 'POST':
            try:
                my_user_profile = UserProfile.objects.get(user_name=request.user)
                TwitterTweet.objects.get(tweet_id="{}".format(query.get('delete'))).delete()
                my_user_profile.tweet_count = my_user_profile.tweet_count - 1
                my_user_profile.save()
            except TwitterTweet.DoesNotExist:
                print("Ignoring does not exist error delete")
        return redirect('accounts:user_profile_view')

    else:
        return render(request, 'accounts/userprofile.html',
                      {'tweets': tweets, 'blocked_list': blocked_list, 'key_listing': key_listing, 'encrypt_key_form': encrypt_key_form, 'userprofile': user_profile,
                       'post_form': post_form,
                       'edituserprofile': edit_user_profile, 'my_user_profile': my_user_profile, 'pinned_posts': pinned, 'priv_msg_form': priv_msg_form, 'my_mail': my_mail})


def user_search_view(request):
    """" Handles requests for searching the user database and returning the information """
    encrypt_key_form = forms.UserEncryptionForm()
    key_listing = UserEncryptionKeyList.objects.all()
    my_user_profile = UserProfile.objects.get(user_name=request.user)
    my_mail = PrivateMessage.objects.all()
    blocked_list = BlockedUsers.objects.all()
    for blacklisted in blocked_list:
        if blacklisted.blocked_by == my_user_profile.user_profile_name:
            for update_my_mail in my_mail:
                if blacklisted.blocked_user_id == update_my_mail.source_author_id:
                    update_my_mail.show_message = False

    user_profile = UserProfile.objects.all()
    priv_msg_form = PrivateMessageForm()
    post_form = NewTweetForm()
    my_user_profile = UserProfile.objects.get(user_name=request.user)
    if request.method == 'GET':
        query = request.GET
        if 'search' in query.keys():
            try:
                searched_profile = UserProfile.objects.get(user_profile_name="{}".format(query.get('search')))
                return render(request, 'accounts/search.html',
                              {'blocked_list': blocked_list, 'key_listing': key_listing, 'encrypt_key_form': encrypt_key_form, 'my_user_profile': my_user_profile,
                               'userprofile': user_profile,
                               'post_form': post_form, 'searched_profile': searched_profile,
                               'priv_msg_form': priv_msg_form, 'my_mail': my_mail})
            except UserProfile.DoesNotExist:
                not_found = "The user " + "{}".format(query.get('search')) + " was not found"
                return render(request, 'accounts/search.html',
                              {'blocked_list': blocked_list, 'key_listing': key_listing, 'encrypt_key_form': encrypt_key_form, 'my_user_profile': my_user_profile,
                               'userprofile': user_profile,
                               'post_form': post_form, 'priv_msg_form': priv_msg_form, 'Not_Found': not_found,
                               'my_mail': my_mail})


def delete_old_profile_pictures(file_name):
    """" Handles deleting the local images when they are replied. Profile pictures etc. """
    if os.path.isfile(file_name.path):
        os.remove(file_name.path)
