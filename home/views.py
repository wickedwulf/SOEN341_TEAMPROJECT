from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from .models import Twitter_Tweet, Following_Users, Liked_Tweets, Pinned_Posts, Blocked_Users, Private_Message, Replies_To_Tweet
from accounts.models import user_profile, user_encryption_key_list
import hashlib
import random
import os
import copy


def homeactions(request):
    my_user_profile = user_profile.objects.get(user_name=request.user)

    blocked_list = Blocked_Users.objects.all()
    latest_tweets = Twitter_Tweet.objects.all().order_by('published').reverse() #used to apply  blocking feature

    # this code loops runs through our blocked list and sets show flag to false on any tweets that are by a blocked user x (filtered with if in html)
    for blacklisted in blocked_list:
      if blacklisted.blocked_by == my_user_profile.user_profile_name:
          for update_tweet_list in latest_tweets:
              if blacklisted.blocked_user_id == update_tweet_list.author_id:
                  update_tweet_list.show_post = False



    # this code filters our blocked people from private  messages
    my_mail = Private_Message.objects.all()
    for blacklisted in blocked_list:
      if blacklisted.blocked_by == my_user_profile.user_profile_name:
          for update_my_mail in my_mail:
              if blacklisted.blocked_user_id == update_my_mail.source_author_id:
                  update_my_mail.show_message = False

    # this makes encryption backend vs frontend
    encryption_key_list = user_encryption_key_list.objects.all()
    for encryption_keys in encryption_key_list:
        if encryption_keys.encrypt_list_owner == my_user_profile.user_profile_name:
            for update_tweet_list in latest_tweets:
                if update_tweet_list.encrypt_content and encryption_keys.encryption_key == update_tweet_list.content_key:
                    update_tweet_list.show_encrypted = False



    userprofile = user_profile.objects.all()
    priv_msg_form = forms.Private_Message_Form()
    following = Following_Users.objects.all()
    post_form = forms.NewTweetForm()

    query = request.GET
    # used for doing new tweets
    if 'action' in query.keys():  # used for sending parameters from buttons on the same page.. might be a better way *shrug*
        if "{}".format(query.get('action')) == "tweet":
            if request.method == 'POST':  # check that this is a valid post message from botton and not someone loading page
                post_form = forms.NewTweetForm(request.POST, request.FILES)  # get the data from the fields on the page
                if post_form.is_valid():  # check if the form is valid i.e right kind of data
                    user_profile_tmp = user_profile.objects.get(user_name=request.user)
                    new_form = post_form.save(commit=False)  # save the post in the database
                    user_profile_name = user_profile.objects.get(user_name=request.user)  # use username to get profile
                    user_profile_tmp.tweet_count = user_profile_tmp.tweet_count + 1  # increase post count by 1
                    user_profile_tmp.save()  # save updated count
                    new_form.author_id = user_profile_name.user_profile_name  # set the author id
                    new_form.tweet_id = hashlib.sha1(new_form.content.encode('utf-8') + new_form.author_id.encode('utf-8')).hexdigest()
                    new_form.encrypted_content = emoji_encrypt(random.randint(10, len(new_form.content)))
                    if new_form.encrypt_content:
                        new_form.show_encrypted = True
                    new_form.save()  # save updated tweet to db
                    return redirect('home:home_actions')  # send user to latest page to view their tweet
                return HttpResponse('somethings wrong - check homeactions code in home/views.py file')

        elif "{}".format(query.get('action')) == "privatemsg":
            if request.method == 'POST':  # check that this is a valid post message from botton and not someone loading page
                priv_msg_form = forms.Private_Message_Form(request.POST, request.FILES)  # get the data from the fields on the page
                if priv_msg_form.is_valid():
                    tmp_form = priv_msg_form.save(commit=False)
                    tmp_form.source_author_id = user_profile.objects.get(user_name=request.user).user_profile_name
                    tmp_form.private_message_id = hashlib.sha1(tmp_form.content.encode('utf-8') + tmp_form.source_author_id.encode('utf-8')).hexdigest()
                    tmp_form.save()
                return redirect('home:home_actions')  # send user to latest page to view their tweet
            return HttpResponse('somethings wrong - check homeactions code in home/views.py file')



  # this handles deleting the private messages and removing any attached pictures
    elif 'deleteprivatemsg' in query.keys():
        if request.method == 'POST':  # check that this is a valid post message from botton and not someone loading page
            try:
                priv_msg_delete = Private_Message.objects.get(private_message_id="{}".format(query.get('deleteprivatemsg')))
                if priv_msg_delete.media_attachment != 'default.png':
                    delete_old_pictures(priv_msg_delete.media_attachment)  # send the message string to the delete function
                priv_msg_delete.delete()
            except Private_Message.DoesNotExist:
                print("Could not find private message")
            my_user_profile = user_profile.objects.get(user_name=request.user)
            return render(request, 'home/home.html',
                          {'my_user_profile': my_user_profile, 'userprofile': userprofile, 'post_form': post_form, 'latest_tweets': latest_tweets, 'following': following,
                           'blocked_list': blocked_list, 'priv_msg_form': priv_msg_form, 'my_mail': my_mail})

        return HttpResponse('somethings wrong - check homeactions code in home/views.py file')



    # This handles looking for the tweet ID from the passed variables and liking it
    elif 'liked' in query.keys():
        if request.method == 'POST':
            like_tweet = Twitter_Tweet.objects.get(tweet_id="{}".format(query.get('liked')))
            try:
                user_profile_tmp = user_profile.objects.get(user_name=request.user)
                Liked_Tweets.objects.get(tweet_id="{}".format(query.get('liked')), liked_by_user=user_profile_tmp.user_profile_name).delete()
                print("deleted like from tweet")
                user_profile_tmp = user_profile.objects.get(user_name=request.user)
                user_profile_tmp.liked_tweet_count = user_profile_tmp.liked_tweet_count - 1
                user_profile_tmp.save()
                like_tweet.favourites = like_tweet.favourites - 1
                like_tweet.save()
                my_user_profile = user_profile.objects.get(user_name=request.user)
                return render(request, 'home/home.html',
                              {'my_user_profile': my_user_profile, 'userprofile': userprofile, 'post_form': post_form, 'latest_tweets': latest_tweets, 'following': following,
                               'blocked_list': blocked_list, 'priv_msg_form': priv_msg_form, 'my_mail': my_mail})
            except Liked_Tweets.DoesNotExist:
                print("Does not exist so creating it. Liked Post")
                user_profile_tmp = user_profile.objects.get(user_name=request.user)
                like_add = Liked_Tweets()
                like_tweet.favourites = like_tweet.favourites + 1
                user_profile_tmp.liked_tweet_count = user_profile_tmp.liked_tweet_count + 1
                like_add.author_id = like_tweet.author_id
                like_add.tweet_id = like_tweet.tweet_id
                like_add.liked_by_user = user_profile_tmp.user_profile_name
                like_add.save()
                user_profile_tmp.save()
                like_tweet.save()
        my_user_profile = user_profile.objects.get(user_name=request.user)
        return render(request, 'home/home.html',
                      {'my_user_profile': my_user_profile, 'userprofile': userprofile, 'post_form': post_form, 'latest_tweets': latest_tweets, 'following': following,
                       'blocked_list': blocked_list, 'priv_msg_form': priv_msg_form, 'my_mail': my_mail})

    elif 'delete' in query.keys():
        if request.method == 'POST':
            try:
                user_profile_tmp = user_profile.objects.get(user_name=request.user)
                get_pic_path = Twitter_Tweet.objects.get(tweet_id="{}".format(query.get('delete')))
                if get_pic_path.media_attachment != 'default.png':  # delete the old picture from the tweet to save server space
                    delete_old_pictures(get_pic_path.media_attachment)
                get_pic_path.delete()
                user_profile_tmp.tweet_count = user_profile_tmp.tweet_count - 1
                user_profile_tmp.save()
            except Twitter_Tweet.DoesNotExist:
                print("Ignoring does not exist error delete")
        my_user_profile = user_profile.objects.get(user_name=request.user)
        return render(request, 'home/home.html',
                      {'my_user_profile': my_user_profile, 'userprofile': userprofile, 'post_form': post_form, 'latest_tweets': latest_tweets, 'following': following,
                       'blocked_list': blocked_list, 'priv_msg_form': priv_msg_form, 'my_mail': my_mail})

    elif 'follow' in query.keys():
        if request.method == 'POST':
            try:
                user_profile_tmp = user_profile.objects.get(user_name=request.user)
                Following_Users.objects.get(followed_user="{}".format(query.get('follow')), liked_by_user=user_profile_tmp.user_profile_name).delete()
                follow_profile = user_profile.objects.get(user_profile_name="{}".format(query.get('follow')))
                follow_profile.follower_count = follow_profile.follower_count + 1
                follow_profile.save()
                print("deleted like from tweet")
                my_user_profile = user_profile.objects.get(user_name=request.user)
                return render(request, 'home/home.html',
                              {'my_user_profile': my_user_profile, 'userprofile': userprofile, 'post_form': post_form, 'latest_tweets': latest_tweets, 'following': following,
                               'blocked_list': blocked_list, 'priv_msg_form': priv_msg_form, 'my_mail': my_mail})

            except Following_Users.DoesNotExist:
                print("Does not exist so create it. Now following user")
                user_profile_tmp = user_profile.objects.get(user_name=request.user)
                follow_add = Following_Users()
                follow_add.liked_by_user = user_profile_tmp.user_profile_name
                follow_add.followed_user = "{}".format(query.get('follow'))
                follow_add.save()
                follow_profile = user_profile.objects.get(user_profile_name="{}".format(query.get('follow')))
                follow_profile.follower_count = follow_profile.follower_count + 1
                follow_profile.save()
        my_user_profile = user_profile.objects.get(user_name=request.user)
        return render(request, 'home/home.html',
                      {'my_user_profile': my_user_profile, 'userprofile': userprofile, 'post_form': post_form, 'latest_tweets': latest_tweets, 'following': following,
                       'blocked_list': blocked_list, 'priv_msg_form': priv_msg_form, 'my_mail': my_mail})

    # pin the post by storing the id of the post and the user that pinned it
    elif 'pin' in query.keys():
        if request.method == 'POST':
            try:  # used to delete a pinned post
                user_profile_tmp = user_profile.objects.get(user_name=request.user)
                Pinned_Posts.objects.get(tweet_id="{}".format(query.get('pin')), pinned_by_user=user_profile_tmp.user_profile_name).delete()
                print("Removing Pin")
            except Pinned_Posts.DoesNotExist:
                print("Does not exist so create it. Post has been pinned")
                user_profile_tmp = user_profile.objects.get(user_name=request.user)
                pin = Pinned_Posts()
                pin.tweet_id = "{}".format(query.get('pin'))
                pin.pinned_by_user = user_profile_tmp.user_profile_name
                pin.save()
        my_user_profile = user_profile.objects.get(user_name=request.user)
        return render(request, 'home/home.html',
                      {'my_user_profile': my_user_profile, 'userprofile': userprofile, 'post_form': post_form, 'latest_tweets': latest_tweets, 'following': following,
                       'blocked_list': blocked_list, 'priv_msg_form': priv_msg_form, 'my_mail': my_mail})


    # block a user so we can't see them
    elif 'block' in query.keys():
        if request.method == 'POST':
            try:  # used to delete a blocked user from db
                user_profile_tmp = user_profile.objects.get(user_name=request.user)
                Blocked_Users.objects.get(blocked_user_id="{}".format(query.get('block')), blocked_by=user_profile_tmp.user_profile_name).delete()
                print("Removing block")
            except Blocked_Users.DoesNotExist:
                print("Does not exist so create it. User has been blocked")
                user_profile_tmp = user_profile.objects.get(user_name=request.user)
                block = Blocked_Users()
                block.blocked_user_id = "{}".format(query.get('block'))
                block.blocked_by = user_profile_tmp.user_profile_name
                block.save()
        my_user_profile = user_profile.objects.get(user_name=request.user)
        return render(request, 'home/home.html',
                      {'my_user_profile': my_user_profile, 'userprofile': userprofile, 'post_form': post_form, 'latest_tweets': latest_tweets, 'following': following,
                       'blocked_list': blocked_list, 'priv_msg_form': priv_msg_form, 'my_mail': my_mail})

    # need to send all that above data to the page so we can access it for the modal boxes and stuff
    else:
        emoji_encrypt(100)
        my_user_profile = user_profile.objects.get(user_name=request.user)
        return render(request, 'home/home.html',
                      {'my_user_profile': my_user_profile, 'userprofile': userprofile, 'post_form': post_form, 'latest_tweets': latest_tweets, 'following': following,
                       'blocked_list': blocked_list,
                       'priv_msg_form': priv_msg_form, 'my_mail': my_mail})
    # need to send all that above data to the page so we can access it for the modal boxes and stuff



def emoji_encrypt(len):
    emoji_list = ['😀', '😁', '😂', '🤣', '😃', '😄', '😅', '😆', '😉', '😊', '😋', '😎', '😍', '😘', '😗', '😙', '😚', '🙂', '🍆', '🔥', '🍪', '🐔', '☘', '🍣', '🍥', '👯♀', '👯♂',
                  '🕴', '🚶♀', '🚶♂', '🏃♀', '🏃♂', '👫', '👭', '👬', '🧙♀', '️🧙♂', '️🧝♀', '️🧝♂', '️🧛♀', '️🧛♂', '️🧟♀', '️🧟♂', '️🧞♀', '️🧞♂', '♀', '♂', '✍', '🙏', '💍',
                  '💄', '💋', '👄', '👅', '👂', '👃', '👣', '👁', '👀', '🧠', '✌', '🤟', '🤘', '👌', '👈', '👉', '👆', '👇', '☝', '✋', '🤚', '🖐', '🖖', '👋', '🤙', '💪', '🖕',
                  '🍐', '🍊', '🍋', '🍌', '🥐', '🍞', '🥖', '🥨', '🥦', '🥒', '🥓', '🥩', '💣', '🔪', '🗡', '⚔', '🛡', '🚬', '⚰', '♾', '🏴', '☠', '♾', '💲', '💱', '™', '©', '®',
                  '〰', '➰', '➿', '🔚', '🔙', '🔛', '🔝', '🔜', '✔', '☑', '🔘', '⚪', '⚫', '❤', '🧡', '💛', '💚', '💙', '💜', '🖤', '💔', '❣', '💕', '💞', '💓', '💗', '💖', '💘',
                  '💝', '💟', '☮', '✝', '☪', '🕉', '☸', '✡', '🔯', '🕎', '☯', '☦', '🛐', '⛎', '♈', '♉', '♊', '♋', '♌', '♍', '♎', '♏', '♐', '♑', '♒', '♓', '🆔', '⚛', '🉑', '☢', '☣',
                  '📴', '📳', '🈶', '🈚', '🈸', '🈺', '🈷️', '✴', '🆚', '💮', '🉐', '㊙', '㊗', '🈴', '🈵', '🈹', '🈲', '🅰️', '🅱️', '🆎', '🆑', '🅾️', '🆘', '❌', '⭕', '🛑', '⛔',
                  '📛', '🚫', '💯', '💢', '♨', '🚷', '🚯', '🚳', '🚱', '🔞', '📵', '🚭', '❗', '❕', '❓', '❔', '‼', '⁉', '🎗', '🎲']
    line = random.sample(emoji_list, len)
    return "".join(map(str, line))


def delete_old_pictures(file_name):
    if os.path.isfile(file_name.path):
        os.remove(file_name.path)
