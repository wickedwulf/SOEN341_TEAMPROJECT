from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import user_profile
from home.forms import NewTweetForm



def index(request):
    form = AuthenticationForm()
    postform = NewTweetForm()
    if request.user.is_authenticated:
     userprofile = user_profile.objects.get(user_name=request.user)
     return render(request, 'core_site/index.html', {'form': form, 'userprofile': userprofile, 'postform': postform })
    else: # make sure user is logged in or else when we check for a profile we get a crash
     return render(request, 'core_site/index.html', {'form': form})
    # the above forms need to send their stuff to the page so we can display  the data on the tool bar and have a working tweet modal
