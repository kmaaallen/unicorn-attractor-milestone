from django.shortcuts import render
from .forms import SubscriptionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import Group
from .models import Subscriber


import stripe
stripe.api_key = settings.STRIPE_SECRET


@login_required
def new_subscription(request):
    """
    Create a view that allows users to subscribe to feature support/requests
    """
    plan = "plan_GRYCbL4JOJXYi1"
    # redirect users if they are already subscribed so they cannot access form
    user = request.user
    if user.groups.filter(name='Subscribers').exists():
        return render(request, "user_profile.html")

    elif request.method == 'POST':
        subscribe_form = SubscriptionForm(request.POST)
        if subscribe_form.is_valid():
            try:
                # See if customer already exists in Subscriber model
                subscriber = Subscriber.objects.get(user=request.user.id)
                # add new card details and update subscriber data
                customer = stripe.Customer.modify(
                    subscriber.customer_id,
                    card=subscribe_form.cleaned_data['stripe_id'],
                )
                card = stripe.Customer.retrieve_source(
                    subscriber.customer_id,
                    customer.default_source,
                )
                # create subscription
                subscription = stripe.Subscription.create(
                    customer=subscriber.customer_id,
                    items=[{"plan": plan}],
                )
                Subscriber.objects.filter(user=request.user.id).update(
                    subscription_id=subscription.id)
                Subscriber.objects.filter(
                    user=request.user.id).update(card_id=card.id)
                Subscriber.objects.filter(
                    user=request.user.id).update(active=True)
                subscriber_group = Group.objects.get(name='Subscribers')
                subscriber_group.user_set.add(request.user)
                messages.error(request, "You have successfully subscribed.")
                return render(request, "user_profile.html")
            except Subscriber.DoesNotExist:
                try:
                    # Create new customer and subscription
                    # and store details for stripe
                    customer = stripe.Customer.create(
                        email=request.user.email,
                        description=request.user.id,
                        card=subscribe_form.cleaned_data['stripe_id'],
                        subscriptions={}
                    )
                    subscription = stripe.Subscription.create(
                        customer=customer,
                        items=[{"plan": plan}],
                    )
                    # create new Subscriber object and store details
                    Subscriber.objects.create(user=request.user,
                                              customer_id=customer.id,
                                              subscription_id=subscription.id,
                                              card_id=customer.default_source,
                                              active=True)
                    subscriber_group = Group.objects.get(name='Subscribers')
                    subscriber_group.user_set.add(request.user)
                    messages.error(
                        request, "You have successfully subscribed.")
                    return render(request, "user_profile.html")
                except stripe.error.CardError:
                    messages.error(request, "Your card was declined.")
        else:
            messages.error(request, "We were unable to take a payment.")
    else:
        subscribe_form = SubscriptionForm

    return render(request, "subscribe.html",
                  {'form': subscribe_form,
                   'publishable': settings.STRIPE_PUBLISHABLE})


@login_required
def unsubscribe(request):
    """
    Create a view that allows users to unsubscribe to feature support/requests
    """
    subscriber = Subscriber.objects.get(user=request.user.id)
    subscription = subscriber.subscription_id
    stripe.Subscription.delete(subscription)
    Subscriber.objects.filter(user=request.user.id).update(subscription_id='')
    subscriber_group = Group.objects.get(name='Subscribers')
    # Remove user from subscriber group to
    # revoke access to add and upvote on features
    subscriber_group.user_set.remove(request.user)
    # Set as inactive in Subscriber model for info
    Subscriber.objects.filter(user=request.user.id).update(active=False)

    return render(request, "user_profile.html")


@login_required
def update_card_details(request):
    """
    Create a view that allows subscribed users to update
    card details for taking subscription payment
    """
    if request.method == 'POST':
        subscribe_form = SubscriptionForm(request.POST)
        if subscribe_form.is_valid():
            try:
                # See if customer already exists in Subscriber model
                subscriber = Subscriber.objects.get(user=request.user.id)
                # add new card details and update subscriber data
                customer = stripe.Customer.modify(
                    subscriber.customer_id,
                    card=subscribe_form.cleaned_data['stripe_id'],
                )
                card = stripe.Customer.retrieve_source(
                    subscriber.customer_id,
                    customer.default_source,
                )
                Subscriber.objects.filter(
                    user=request.user.id).update(card_id=card.id)
            except stripe.error.CardError:
                messages.error(request, "Unable to update card details.")
            return render(request, "user_profile.html")
    else:
        subscribe_form = SubscriptionForm

    return render(request, "update_card.html",
                  {'form': subscribe_form,
                   'publishable': settings.STRIPE_PUBLISHABLE})
