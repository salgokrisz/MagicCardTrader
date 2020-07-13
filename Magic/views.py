from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    # /home/
    return HttpResponse('<h1>Hi this is the mainpage</h1>')

def users(request):
    return HttpResponse("<h1>Users here</h1>")

def user(request, user_id):
    return HttpResponse("<h2>This is user " + str(user_id) + "</h2>")

def about(request):
    return HttpResponse('<h3>Magic Card Trader About</h3>')