from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import User
from .models import Card
from django.template import loader
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm

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
        'nbar': 'home'
    }
    return HttpResponse(template.render(context, request))

def users(request):
    all_users = User.objects.all()
    template = loader.get_template('magic/users.html')
    context = {
       'all_users': all_users,
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
    all_cards = Card.objects.all()
    template = loader.get_template('magic/cards.html')
    context = {
        'all_cards': all_cards,
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

class CardCreate(CreateView):
    model = Card
    fields = ['name', 'set_name', 'price', 'user', 'is_foil']
    context = {
        'nbar': 'add_cards',
    }

class CardUpdate(UpdateView):
    model = Card
    fields = ['name', 'set_name', 'price', 'user', 'is_foil']
    #form = self.form_class(Card.name, Card.set_name, Card.price, Card.user, Card.is_foil)

class CardDelete(DeleteView):
    model = Card
    success_url = reverse_lazy('Magic:cards')

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

            # cleaned (normalitzed) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user.set_password(password)
            user.save()
            new_user = User(name=username, email_address=email)
            new_user.save()

            # returns user objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('Magic:index')
        
        return render(request, self.template_name, {'form': form})




