from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from django.template import loader

# Create your views here.

def home(request):
    # /home/
    return HttpResponse('<h1>Hi this is the mainpage</h1>')
    # TODO
    # be lehet jelentkezni 
    # itt lehet keresni usereket
    # lehet keresni lapokat
    # lesznek random userek kirakva - recommended users
    # lesznek random lapok kirakva - recommended cards from users


def users(request):
    all_users = User.objects.all()
    template = loader.get_template('magic/users.html')
    context = {
       'all_users': all_users,

    }
    return HttpResponse(template.render(context, request))

def user(request, user_id):
    template = loader.get_template('magic/user_detail.html')
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    context = {
       'user': user,

    }
    return HttpResponse(template.render(context, request))
    #TODO
    # eladó lapok listája
    # eladó lapok között a kersés
    # elérhetőség/átvételi lehetőség
    # üzenetküldés

def about(request):
    return HttpResponse('<h3>Magic Card Trader About</h3>')