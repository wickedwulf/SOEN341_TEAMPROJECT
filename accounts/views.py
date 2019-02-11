from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


def signup_view(request):  # create capture for html request from signup page
    if request.method == ('POST'):  # check if it's a post message from form
        form = UserCreationForm(request.POST)  # create a djangos user creation form and fill it with submitted data
        if form.is_valid():  # check if the form is valid? i.e user does not exist and requirements are met pass 8 char etc
            user = form.save()  # save the form to the data base form.save  also store the user token in user variable
            login(request, user)  # use djangos login function to login the valid user
            return redirect('/postings/')  # send user to wherever (should be changed later)
    else:  # if it was not valid or correct
        form = UserCreationForm()  # if take the form data provided
    return render(request, 'accounts/signup.html', {'form': form})  # send it back to the login page


def login_view(request):  # create capture for html request from signup page
    if request.method == ('POST'):  # check if it's a post message from form
        form = AuthenticationForm(
            data=request.POST)  # because the first bit of data is not the login data we use data=request.post
        if form.is_valid():  # check if its valid
            user = form.get_user()  # store form data in users
            login(request, user)  # pass valid user data to login function
            return redirect('/postings/')  # send users to whatever page once logged in
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):  # handle logout requests
    if request.method == ('POST'):  # check if its a post message from a button
        logout(request)  # send request to the logout function in django
        return redirect('')  # send users to homepage of site or someplace
