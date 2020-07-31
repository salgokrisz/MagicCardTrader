from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import User
from .models import Card
from django.template import loader

# Create your views here.

#def home(request):
#    # /home/
#    return HttpResponse('<h1>Hi this is the mainpage</h1>')
   
def index(request):
    # TODO
    # be lehet jelentkezni 
    # itt lehet keresni usereket
    # lehet keresni lapokat
    # lesznek random userek kirakva - recommended users
    # lesznek random lapok kirakva - recommended cards from users
    users = User.objects.all()
    cards = Card.objects.all()
    template = loader.get_template('magic/index.html')
    context = {
        'users': users,
        'cards': cards,
    }
    return HttpResponse(template.render(context, request))

def users(request):
    all_users = User.objects.all()
    template = loader.get_template('magic/users.html')
    context = {
       'all_users': all_users,

    }
    return HttpResponse(template.render(context, request))

def user_detail(request, user_id):
    total_cards = User.objects.all()
    template = loader.get_template('magic/user_detail.html')
    try:
        user = User.objects.get(pk=user_id)
        card = Card.objects.all()
    except User.DoesNotExist:
        raise Http404("User does not exist")
    context = {
       'user': user,
       'card': card,

    }
    return HttpResponse(template.render(context, request))
    #TODO
    # eladó lapok listája
    # eladó lapok között a kersés
    # elérhetőség/átvételi lehetőség
    # üzenetküldés

def cards(request):
    all_cards = Card.objects.all()
    template = loader.get_template('magic/cards.html')
    context = {
        'all_cards': all_cards,
    }
    return HttpResponse(template.render(context, request))

def card_detail(request, card_id):
    
    template = loader.get_template('magic/card_detail.html')
    try:
        card = Card.objects.get(pk=card_id)
        user = User.objects.all()
    except Card.DoesNotExist:
        raise Http404("Card does not exists")
    context = {
        'card': card,
        'user': user,
    }
    return HttpResponse(template.render(context, request))

def about(request):
    return HttpResponse('<h3>Magic Card Trader About</h3>')