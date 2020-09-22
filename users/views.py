from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from Magic.forms import AddressUpdateForm
from shopping_cart.views import get_user_pending_order
from Magic.models import Address


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
    print(address)
    context = {
        'nbar': 'profile',
        'address': address,
        #'order': existing_order,
    }
    return render(request, 'users/profile.html', context)

@login_required
def update_profile(request):
    existing_order = get_user_pending_order(request)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        a_form = AddressUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid() and p_form.is_valid() and a_form.is_valid():
            u_form.save()
            p_form.save()
            a_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        a_form = AddressUpdateForm(instance=request.user.profile.address)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'a_form': a_form,
        'nbar': 'profile',
        'order': existing_order,
    }
    return render(request, 'users/update.html', context)

