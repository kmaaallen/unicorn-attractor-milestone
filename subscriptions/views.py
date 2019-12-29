from django.shortcuts import render
from .forms import SubscriptionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

import stripe

# Create your views here.


@login_required
def new_subscription(request):
    """
    Create a view that allows users to subscribe to feature support/requests
    """
    plan = "plan_GRYCbL4JOJXYi1"

    if request.method == 'POST':
        form = SubscriptionForm()
        if form.is_valid():
            try:
                customer = stripe.Charge.create(
                    amount=5000,
                    currency="GBP",
                    description=request.user.email,
                    card=form.cleaned_data['stripe_id'],
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined.")
        
            if customer.paid:
                stripe.Subscription.create(
                    customer=request.user.stripe_id,
                    items=[{"plan": plan}],
                )
                messages.error(request, "You have successfully subscribed.")
                return render(request, "subscribe.html", {'form': form,
                              'publishable': settings.STRIPE_PUBLISHABLE})
            else:
                messages.error(request, "Unable to take payment.")
        else:
            print(form.errors)
            messages.error(request, "We were unable to take a payment.")
    else:
        form = SubscriptionForm
        
    return render(request, "subscribe.html", {'form': form, 'publishable': 
                  settings.STRIPE_PUBLISHABLE})





