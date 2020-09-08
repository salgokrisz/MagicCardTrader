from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from Magic.models import Profile, Card
from shopping_cart.models import OrderItem, Order, Transaction
from shopping_cart.extras import generate_order_id#, transaction, generate_client_token
import datetime
import stripe
import users

#stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required()
def add_to_cart(request, **kwargs):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter cards by id
    card = Card.objects.filter(id=kwargs.get('item_id', "")).first()
    # check if the user already owns this card
    ##if card in request.user.profile.objects.all():
    ##    messages.info(request, 'You already own this card')
    ##    return redirect(reverse('Magic:cards')) 
    # create orderItem of the selected card
    order_item, status = OrderItem.objects.get_or_create(card=card)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    setattr(card, "is_ordered", True)
    card.save()
    if status:
        # generate a reference code
        user_order.ref_code = generate_order_id()
        user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect(reverse('Magic:cards'))


@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    card_id = OrderItem.objects.get(pk=item_id).card.id
    card = Card.objects.get(pk=card_id)
    setattr(card, "is_ordered", False)
    card.save()
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('Magic:order_summary'))


def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0

@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order,
        'nbar':'order-summary',
    }
    return render(request, 'shopping_cart/order_summary.html', context)

@login_required()
def checkout(request):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order,
        'nbar':'order-summary',
    }
    return render(request, 'shopping_cart/checkout.html', context)

@login_required()
def process_payment(request, order_id):
    return redirect(reverse('Magic:update_records', kwargs={'order_id': order_id,}))

""" @login_required()
def checkout(request, **kwargs):
    #client_token = generate_client_token()
    existing_order = get_user_pending_order(request)
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        token = request.POST.get('stripeToken', False)
        if token:
            try:
                charge = stripe.Charge.create(
                    amount=100*existing_order.get_cart_total(),
                    currency='usd',
                    description='Example charge',
                    source=token,
                )

                return redirect(reverse('Magic:update_records',
                        kwargs={
                            'token': token
                        })
                    )
            except stripe.CardError as e:
                message.info(request, "Your card has been declined.")
        else:
            result = transact({
                'amount': existing_order.get_cart_total(),
                'payment_method_nonce': request.POST['payment_method_nonce'],
                'options': {
                    "submit_for_settlement": True
                }
            })

            if result.is_success or result.transaction:
                return redirect(reverse('Magic:update_records',
                        kwargs={
                            'token': result.transaction.id
                        })
                    )
            else:
                for x in result.errors.deep_errors:
                    messages.info(request, x)
                return redirect(reverse('Magic:checkout'))
            
    context = {
        'order': existing_order,
        #'client_token': client_token,
        #'STRIPE_PUBLISHABLE_KEY': publishKey
    }

    return render(request, 'shopping_cart/checkout.html', context) """

""" @login_required()
def update_transaction_records(request, token):
    # get the order being processed
    order_to_purchase = get_user_pending_order(request)

    # update the placed order
    order_to_purchase.is_ordered=True
    order_to_purchase.date_ordered=datetime.datetime.now()
    order_to_purchase.save()
    
    # get all items in the order - generates a queryset
    order_items = order_to_purchase.items.all()

    # update order items
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # Add cards to user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # get the cards from the items
    order_cards = [item.card for item in order_items]
    user_profile.card_set.add(*order_cards)
    user_profile.save()

    
    # create a transaction
    transaction = Transaction(profile=request.user.profile,
                            token=token,
                            order_id=order_to_purchase.id,
                            amount=order_to_purchase.get_cart_total(),
                            success=True)
    # save the transcation (otherwise doesn't exist)
    transaction.save()


    # send an email to the customer
    # look at tutorial on how to send emails with sendgrid
    messages.info(request, "Thank you! Your purchase was successful!")
    return redirect(reverse('users:profile')) """


def update_transaction_records(request, order_id):
    # get the order being processed
    order_to_purchase = Order.objects.filter(pk=order_id).first()

    # update the placed order
    order_to_purchase.is_ordered=True
    order_to_purchase.date_ordered=datetime.datetime.now()
    order_to_purchase.save()
    
    # get all items in the order - generates a queryset
    order_items = order_to_purchase.items.all()
    # update order items
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # Add cards to user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # get the cards from the items
    """ for item in order_items:
        card_id = item.card.id
        card = Card.objects.get(pk=card_id)
 """
        
    order_cards = [item.card for item in order_items]
    user_profile.user.card_set.add(*order_cards)
    user_profile.save()
    messages.info(request, "Thank you! Your purchase was successful!")
    return redirect(reverse('users:profile'))

def success(request, **kwargs):
    # a view signifying the transcation was successful
    return render(request, 'shopping_cart/purchase_success.html', {})
