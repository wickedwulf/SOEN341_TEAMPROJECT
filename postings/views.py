from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms


@login_required(login_url="/accounts/login/")
def post_view(request):
    return render(request, 'postings/posting.html')


@login_required(login_url="/accounts/login/")
def new_tweet(request):
    form = forms.NewPostsForm()
    return render(request, 'postings/tweets.html', {'form': form})
