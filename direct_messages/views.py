from Magic.models import Card, Profile, Address
from Magic.forms import CardForm, AddressUpdateForm
from direct_messages.models import Message
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages as DjangoMessages


def messages(request):
    
    context = {
        'nbar': 'messages',
    }

    return render(request, 'direct_messages/messages.html', context)

# filtering the messages where the logged in user is the sender and the receiver
@login_required
def inbox(request):
    user = request.user
    messages = Message.get_messages(user=user)
    active_direct = None
    directs = None
    total_unread = 0
    
    if messages:
        message = messages[0]
        #active_direct = message['user'].username
        directs_got = Message.objects.filter(user=user, to_user=message['user'])
        directs_sent = Message.objects.filter(user=user, from_user=message['user'])
        directs = directs_got | directs_sent
        #directs.update(is_read=False)

        for message in messages:
            total_unread = total_unread + message['unread']
                #message['unread'] = 0
        
    context = {
        #'directs': directs,
        'd_messages': messages,
        'active_direct': active_direct,
        'nbar': 'messages',
        'total_unread': total_unread,
    }

    return render(request, 'direct_messages/messages.html', context)

# filtering message objects where the sender and the receiver is the chosen user
# chosen username got in parameter
# sending the message object to the template
@login_required
def directs(request, username):
    user = request.user
    messages = Message.get_messages(user=user)
    active_direct = username
    directs_got = Message.objects.filter(user=user, to_user__username=username)
    directs_sent = Message.objects.filter(user=user, from_user__username=username)
    directs = directs_got | directs_sent
    directs.update(is_read=True)
    total_unread = 0

    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0

    for message in messages:
        total_unread = total_unread + message['unread']

    context = {
        'directs': directs,
        'd_messages': messages,
        'active_direct': active_direct,
        'nbar': 'messages',
        'total_unread': total_unread,
    }

    return render(request, 'direct_messages/messages.html', context)

# send message to the user got from POST req
@login_required
def send_message(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    content = request.POST.get('content')

    if request.method == 'POST':
        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user, content)
        return redirect('Magic:directs', username=to_user)
    else:
        DjangoMessages.info(request, "Your message could not be delivered")
        return redirect('Magic:inbox')


# starting new conv.
# send the first message to the user got in param
@login_required
def new_conversation(request, username):
    from_user = request.user
    send_content = request.POST.get('content')
    
    try:
        to_user = User.objects.get(username=username)
    except Exception as e:
        return redirect('Magic:inbox')
    if from_user != to_user:
        Message.send_message(from_user, to_user, send_content)
    return redirect('Magic:directs', username=username)

