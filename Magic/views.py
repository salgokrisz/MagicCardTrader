from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse('<h1>Hi this is the mainpage</h1>')

def about(request):
    return HttpResponse('<h3>Magic Card Trader About</h3>')