from django.shortcuts import render,render_to_response
from django.http import HttpResponse
# Create your views here.
#

def index(request):
    return HttpResponse("<center><H1>Welcome to the SOEN341 Twitter Test Site</center>")


