from .models import Card
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
from shopping_cart.views import get_user_pending_order

#generic views but neet to figure out how these work
#class indexView(generic.ListView):
#    tamplate_name = 'magic/index.html'
#
#class UsersView(generic.ListView):
#    tamplate_name = 'magic/users.html'
#    context_object_name = 'all_users'
#
#    def get_queryset(self):
#        return User.objects.all()
#
#class UserDetailView(generic.ListView):
#    model = User
#    template_name = 'magic/user_detail.html'

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
        'nbar': 'home',
    }
    return HttpResponse(template.render(context, request))

def users(request):
    all_users = User.objects.all()
    page = request.GET.get('page', 1)
    template = loader.get_template('magic/users.html')
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
    if request.user.is_authenticated:
        all_cards = Card.objects.filter(is_ordered=False).exclude(user=request.user)
    else:
        all_cards = Card.objects.filter(is_ordered=False)
    page = request.GET.get('page', 1)
    template = loader.get_template('magic/cards.html')
    paginator = Paginator(all_cards, 7)
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        cards = paginator.page(1)
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)
    
    context = {
        'all_cards': all_cards,
        'cards': cards,
        'nbar':'cards',
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

'''
class UserFormView(View):
    form_class = UserForm
    template_name = 'magic/registration_form.html'


    #display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})


    # process form data, add user to database
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            # returns user objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('Magic:index')
        
        return render(request, self.template_name, {'form': form})
'''




