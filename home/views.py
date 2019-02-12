from django.shortcuts import render,render_to_response, redirect
from django.http import HttpResponse
# Create your views here.
# return HttpResponse("<center><H1>Welcome to the SOEN341 Twitter Test Site</center>")

def index(request):
    return render(request,'home/index.html')
