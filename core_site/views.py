""" View file that controls and responds tot he basics of the core site
    Mainly the default site index
"""
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import UserProfile
from home.forms import NewTweetForm


def index(request):
    """ Handles the index page quest when someone goes to the root of the site """
    form = AuthenticationForm()
    post_form = NewTweetForm()

    try:
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user_name=request.user)
            return render(request, 'core_site/index.html', {'form': form, 'userprofile': user_profile, 'postform': post_form})

            # make sure user is logged in or else when we check for a profile we get a crash
        return render(request, 'core_site/index.html', {'form': form})
        # the above forms need to send their stuff to the page so we can display  the data on the tool bar and have a working tweet modal
    except UserProfile.DoesNotExist:
        return render(request, 'core_site/index.html', {'form': form})
