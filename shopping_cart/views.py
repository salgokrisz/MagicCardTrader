from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, View
from Magic.models import Profile, Card, Address
from shopping_cart.models import OrderItem, Order, Payment
from shopping_cart.extras import generate_order_id#, transaction, generate_client_token
from .forms import CheckoutForm
import datetime
from django.utils import timezone
import stripe

stripe.api_key = "pk_test_51HVekUJly0GQJLGzsXDmnaob6xs4nfDOyKtoRs867birofGl247Q3dtV7xURK9vzPWQWLAlcLd3KWl2Z3PrGIBqJ001FiFfrz5"

# `source` is obtained with Stripe.js; see https://stripe.com/docs/payments/accept-a-payment-charges#web-create-token

@login_required()
def add_to_cart(request, item_id):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter cards by id
    card = Card.objects.filter(id=item_id).first()
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
    user_profile = get_object_or_404(Profile, user=request.user.id)
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
    user_profile = get_object_or_404(User, user=request.user)
    # get the cards from the items
    """ for item in order_items:
        card_id = item.card.id
        card = Card.objects.get(pk=card_id)
 """
        
    order_cards = [item.card for item in order_items]
    user_profile.user.card_set.add(*order_cards)
    user_profile.save()
    messages.info(request, "Thank you! Your purchase was successful!")
    return redirect(reverse('Magic:profile'))

def success(request, **kwargs):
    # a view signifying the transcation was successful
    return render(request, 'shopping_cart/purchase_success.html', {})


#-------------

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.filter(owner=self.request.user.profile).last()
            
            context = {
                'order': order,
            }
            return render(self.request, 'shopping_cart/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order!")
            return redirect('Magic:cards')

class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        #form
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'shopping_cart/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.filter(owner=self.request.user.profile).last()
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_number = form.cleaned_data.get('apartment_number')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip_code')
                payment_option = form.cleaned_data.get('payment_option')
                shipping_address = Address(
                    user = self.request.user,
                    street_address = street_address,
                    apartment_number = apartment_number,
                    country = country,
                    zip_code = zip_code,
                )
                shipping_address.save()
                order.address = shipping_address
                order.save()

                #return redirect('Magic:payment', payment_option='stripe')
                return redirect('Magic:payment')
            messages.warning(self.request, "Failed to checkout!")
            return redirect('Magic:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order!")
            return redirect('Magic:order-summary')
        

class PaymentView(View):
    def get(self, *args, **kwargs):
        # order
        return render(self.request, 'shopping_cart/payment.html')
    
    def post(self, *args, **kwargs):
        order = Order.objects.get(owner=self.request.user.profile, is_ordered=False)
        #token = self.request.POST.get('stripeToken')
        token = stripe.Token.create(
            card={
                "number": "4242424242424242",
                "exp_month": 9,
                "exp_year": 2021,
                "cvc": "314",
            },
        )
        amount=int(order.get_cart_total()*100)
        

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
            )
            charge.save()


            order_items = order.items.all()
            # update order items
            order_items.update(is_ordered=True, date_ordered=timezone.now())
            # Add cards to user profile
            user = get_object_or_404(Profile, user=self.request.user.profile.user)
            # get the cards from the items
            #order_cards = [item.card for item in order_items]
            for item in order_items:
                user.user.card_set.add(item.card)
                #item.card.update(user=user)
                #item.card.save()
                user.save()
            #user.card_set.add(order_cards)
            #user.save()
                    
            #create payment
            payment = Payment()
            payment.stripe_charge_id = charge.id
            payment.user = self.request.user
            payment.amount = amount / 100
            payment.save()

            #assing the payment to the order
            order.is_ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Your order was succesful")
            return redirect("Magic:profile")

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', )
            messages.info(self.request, "{err.get('message')}")
        except stripe.error.RateLimitError as e:
            messages.info(self.request, "Rate limit error")
            return redirect("Magic:profile")

        except stripe.error.InvalidRequestError as e:
            messages.info(self.request, e)
            return redirect("Magic:profile")
            
        except stripe.error.AuthenticationError as e:
            messages.info(self.request, "Not authenticated")
            return redirect("Magic:profile")
            
        except stripe.error.APIConnectionError as e:
            messages.info(self.request, "Network error")
            return redirect("Magic:profile")
            
        except stripe.error.StripeError as e:
            messages.info(self.request, "Something went wrong. You are not charged. Please try again.")
            return redirect("Magic:profile")
            
      

