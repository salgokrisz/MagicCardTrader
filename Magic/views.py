from .models import Card, Profile, Address
from .filters import CardFilter, UserFilter
from Magic.forms import CardForm, AddressUpdateForm
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
import random
from datetime import date, timedelta, datetime
from django.utils import timezone
from mtgsdk import Card as MtgCard
from mtgsdk import Set as MtgSet
#from shopping_cart.views import get_user_pending_order


# Create your views here.

# this view sends the content of the index page to the index.html template
def index(request):
    users = User.objects.all()
    cards = Card.objects.all()
    card_count = cards.count()
    user_count = users.count()
    profiles = Profile.objects.all()
    random_cards = []
    for i in range(0, 4):
        rnd_number = random.randint(0, card_count-1)
        if cards[rnd_number].is_ordered == False:
            random_cards.append(cards[rnd_number])
        else:
            random_cards.append(cards[random.randint(0, card_count-1)])

    latest_users = []
    now = timezone.now()
    register_scope = now - timedelta(weeks=2)
    for user in users:
        if register_scope <= user.profile.date_registered:
            latest_users.append(user)

    random_users = []
    for i in range(0, 4):
        rnd_number = random.randint(0, user_count-1)
        random_users.append(users[rnd_number])
    


    template = loader.get_template('magic/index.html')
    context = {
        'users': users,
        'cards': cards,
        'nbar': 'home',
        'random_cards': random_cards,
        'latest_users': latest_users,
        'random_users': random_users
    }
    return HttpResponse(template.render(context, request))

# this view sends the content of the users page to the users frontend page
def users(request):
    template = loader.get_template('magic/users.html')
    all_users = User.objects.all()
    #ordering
    order_by = request.GET.get('order_by')
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
    paginator = Paginator(all_users, 10)
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

# this view sends the details of a specific user to the user_details frontend page
def user_detail(request, user_id):
    user = User.objects.get(pk=user_id)
    total_cards = user.card_set.all()
    template = loader.get_template('magic/user_detail.html')
    try:
        user = User.objects.get(pk=user_id)
        card = Card.objects.all()
    except User.DoesNotExist:
        raise Http404("User does not exist")
    context = {
        'user': user,
        'user_id': user.id,
        'card': card,
        'nbar': 'user',
        'nbar_card': 'users_card_profile',

    }
    return HttpResponse(template.render(context, request))

# this view sends the cards owned by a specific user to the frontend
def user_detail_cards(request, user_id):
    user = User.objects.get(pk=user_id)
    all_cards = user.card_set.all()

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

    #pagination
    paginator = Paginator(all_cards, 5)
    page = request.GET.get('page', 1)
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        cards = paginator.page(1)
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)

    context = {
        'all_cards': all_cards,
        'cards': cards,
        'user': user,
        'order_by': order_by,
        'direction': direction,
        'nbar_card': 'user_card_cards',
    }
    return render(request, 'magic/user_detail_cards.html', context)

# this view sends the content of the cards page to the cards frontend page
def cards(request):
    #template_name to render the template
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
    paginator = Paginator(all_cards, 10)
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

# this view sends the details of a specific card to the card_details frontend page
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
        'nbar':'card',
    }
    return HttpResponse(template.render(context, request))


    return HttpResponse('<h3>Magic Card Trader About</h3>')

# this class based view uses the address create form and validates it
class AddressCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Address
    form_class = AddressUpdateForm
    success_url = reverse_lazy('Magic:profile')
    context = {
        'nbar': 'profile'
    }
    def test_func(self):
        if self.request.user:
            return True
        else:
            return False
    def form_valid(self, form):
        form.instance.user = self.request.user
        model_instance = form.save(commit=False)
        self.request.user.profile.address = model_instance
        self.request.user.profile.address.save()
        self.request.user.profile.save()
        self.request.user.save()
        model_instance.save()
        form.save()
        return super().form_valid(form)

# this class based view uses the card create form and validates it
# also communicates with the MTG API
class CardCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Card
    form_class = CardForm
    success_url = reverse_lazy('Magic:profile_cards')
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
        versions = []
        name = form.cleaned_data['name']
        set_name = form.cleaned_data['set_name']
        sets = MtgSet.where(name=set_name).all()
        if len(sets) > 0:
            code = sets[0].code
            versions = MtgCard.where(name=name, set=code).all()
        else:
            versions = MtgCard.where(name=name).all()
        if len(versions) > 0:
            retval = versions[0].image_url
        else:
            retval = "https://static.wikia.nocookie.net/mtgsalvation_gamepedia/images/f/f8/Magic_card_back.jpg"
        if form.is_valid():
            obj = form.save(commit=False)
            obj.image_url = retval
            #form.cleaned_data['image_url'] = retval
            obj.save()
        
        return super().form_valid(form)

# this class based view controls the card update 
class CardUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Card
    fields = ['name', 'set_name', 'price', 'user', 'is_foil', 'is_ordered']
    success_url = reverse_lazy('Magic:profile_cards')
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

# this view deletes cards from the DB
class CardDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Card
    success_url = reverse_lazy('Magic:profile_cards')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


