from .models import Card, Profile
from .filters import CardFilter, UserFilter
from Magic.forms import CardForm
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.functions import Lower
from shopping_cart.views import get_user_pending_order


# Create your views here.

#def home(request):
#    # /home/
#    return HttpResponse('<h1>Hi this is the mainpage</h1>')
   
def index(request):
    # TODO
    # be lehet jelentkezni - DONE
    # itt lehet keresni usereket
    # lehet keresni lapokat
    # lesznek random userek kirakva - recommended users
    # lesznek random lapok kirakva - recommended cards from users
    users = User.objects.all()
    cards = Card.objects.all()
    profiles = Profile.objects.all()
    for profile in profiles:
        if profile.address:
            profile.address = None
            profile.save()
    template = loader.get_template('magic/index.html')
    context = {
        'users': users,
        'cards': cards,
        'nbar': 'home',
    }
    return HttpResponse(template.render(context, request))

def users(request):
    template = loader.get_template('magic/users.html')
    all_users = User.objects.all()
    order_by = request.GET.get('order_by')
    #order_by = Lower(order_by)
    #ordering
    direction = request.GET.get('direction')
    if direction == 'desc':
         all_users = all_users.order_by(Lower(order_by)).reverse()
    elif direction == 'asc':
        all_users = all_users.order_by(Lower(order_by))
    #filter(search) 
    user_filter = UserFilter(request.GET, queryset=all_users)
    all_users = user_filter.qs
    #paginator
    page = request.GET.get('page', 1)
    paginator = Paginator(all_users, 7)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    context = {
       'all_users': all_users,
       'users': users,
       'nbar': 'users',
       'user_filter': user_filter,
       'order_by': order_by,
       'direction': direction,
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
        'nbar': 'users',

    }
    return HttpResponse(template.render(context, request))
    #TODO
    # eladó lapok listája
    # eladó lapok között a kersés
    # elérhetőség/átvételi lehetőség
    # üzenetküldés

def cards(request):
    #template_name to render the view
    template = loader.get_template('magic/cards.html')
    #if the user is authenticated he/she cannot see his/her cards in the cards_for_sale view
    if request.user.is_authenticated:
        all_cards = Card.objects.filter(is_ordered=False).exclude(user=request.user)
    else:
        all_cards = Card.objects.filter(is_ordered=False)
    #ordering
    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')
    if direction == 'desc':
        if order_by == 'price':
            all_cards = all_cards.order_by(order_by).reverse()
        else:
            all_cards = all_cards.order_by(Lower(order_by)).reverse()
         
    elif direction == 'asc':
        if order_by == 'price':
            all_cards = all_cards.order_by(order_by)
        else: 
            all_cards = all_cards.order_by(Lower(order_by))

    #filtering
    card_filter = CardFilter(request.GET, queryset=all_cards)
    all_cards = card_filter.qs

    #pagination
    paginator = Paginator(all_cards, 7)
    page = request.GET.get('page', 1)
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        cards = paginator.page(1)
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)
    
    #context to allow the template get access to the variables
    context = {
        'all_cards': all_cards,
        'cards': cards,
        'nbar':'cards',
        'order_by': order_by,
        'direction': direction,
        'card_filter': card_filter,
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
        'nbar':'cards',
    }
    return HttpResponse(template.render(context, request))

def about(request):
    return HttpResponse('<h3>Magic Card Trader About</h3>')

class CardCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Card
    form_class = CardForm
    success_url = reverse_lazy('Magic:profile')
    context = {
        'nbar': 'add_cards',
    }
    def test_func(self):
        if self.request.user:
            return True
        else:
            return False
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CardUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Card
    fields = ['name', 'set_name', 'price', 'user', 'is_foil', 'is_ordered']
    #form = self.form_class(Card.name, Card.set_name, Card.price, Card.user, Card.is_foil)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


class CardDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Card
    success_url = reverse_lazy('Magic:profile')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


