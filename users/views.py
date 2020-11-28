from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import Lower
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from Magic.forms import AddressUpdateForm
#from shopping_cart.views import get_user_pending_order
from Magic.models import Address, Card


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created! Now you are able to log in')
            return redirect('login')

    else:
        form = UserRegisterForm()
    context = {
         'form': form,
    }
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    #existing_order = get_user_pending_order(request)
    user = request.user
    address = Address.user
    context = {
        'nbar': 'profile',
        'address': address,
        #'order': existing_order,
    }
    return render(request, 'users/profile.html', context)

@login_required
def profile_cards(request):
    user = request.user
    #all_cards = Card.objects.filter(is_ordered=False, user=user)
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
        'order_by': order_by,
        'direction': direction,
        'nbar': 'profile_cards',
    }
    return render(request, 'users/profile_cards.html', context)

@login_required
def profile_purchases(request):
    user = request.user
    context = {
        'nbar': 'profile_purchases',
    }
    return render(request, 'users/profile_purchases.html', context)

@login_required
def update_profile(request):
    #existing_order = get_user_pending_order(request)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        #a_form = AddressUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            #a_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        #a_form = AddressUpdateForm(instance=request.user.profile.address)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        #'a_form': a_form,
        'nbar': 'profile',
        #'order': existing_order,
    }
    return render(request, 'users/update.html', context)

