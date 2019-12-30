from django.shortcuts import render
from .forms import SubscriptionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import Group


import stripe
stripe.api_key = settings.STRIPE_SECRET


# Create your views here.


@login_required
def new_subscription(request):
    """
    Create a view that allows users to subscribe to feature support/requests
    """
    plan = "plan_GRYCbL4JOJXYi1"

    if request.method == 'POST':
        subscribe_form = SubscriptionForm(request.POST)
        if subscribe_form.is_valid():
            try:
                customer = stripe.Customer.create(
                    description=request.user.email,
                    card=subscribe_form.cleaned_data['stripe_id'],
                    subscriptions={}
                )
                stripe.Subscription.create(
                    customer=customer,
                    items=[{"plan": plan}],
                )
                subscriber_group = Group.objects.get(name='Subscribers')
                subscriber_group.user_set.add(request.user)
                messages.error(request, "You have successfully subscribed.")
                return render(request, "subscribe.html",
                              {'form': subscribe_form,
                               'publishable': settings.STRIPE_PUBLISHABLE})
            except stripe.error.CardError:
                messages.error(request, "Your card was declined.")
        else:
            print(subscribe_form.errors)
            messages.error(request, "We were unable to take a payment.")
    else:
        subscribe_form = SubscriptionForm

    return render(request, "subscribe.html",
                  {'form': subscribe_form,
                   'publishable': settings.STRIPE_PUBLISHABLE})


