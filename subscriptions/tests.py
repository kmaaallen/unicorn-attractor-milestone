from django.test import TestCase
from django.contrib.auth.models import User, Group
from subscriptions.models import Subscriber
from django.conf import settings

import stripe
stripe.api_key = settings.STRIPE_SECRET


class TestModel(TestCase):
    def test_subscriber_model_string(self):
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        subscriber = Subscriber(user=test_user1)
        self.assertEqual(str(subscriber), 'testuser')


class TestSubscriptionPages(TestCase):
    def test_subscriptions_page(self):
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # User should be able to access subscription page
        response = self.client.get('/subscribe/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'subscribe.html')
    
    def test_update_card_page(self):
        # User should be able to access update card page if subscribed
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up and add user to subscribers group
        subscriber_group = Group.objects.create(name='Subscribers')
        subscriber_group.user_set.add(test_user1)
        response = self.client.get('/subscribe/update_card_details/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'update_card.html')

    def test_subscribed_redirect(self):
        # User should be redirected to profile page if subscribed and trying to access subscribe link
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up and add user to subscribers group
        subscriber_group = Group.objects.create(name='Subscribers')
        subscriber_group.user_set.add(test_user1)
        response = self.client.get('/subscribe/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'user_profile.html')


class TestSubscriptionActions(TestCase):
    def test_subscribed_user_able_to_unsubscribe(self):
        # User should be redirected to profile page if subscribed and trying to access subscribe link
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up and add user to subscribers group
        subscriber_group = Group.objects.create(name='Subscribers')
        subscriber_group.user_set.add(test_user1)
        # create a customer
        customer = stripe.Customer.create(
            email='myemail@123.com',
            description=test_user1.id,
            card='tok_visa',
            subscriptions={}
            )
        # set up stripe subscription
        plan = "plan_GRYCbL4JOJXYi1"
        subscription = stripe.Subscription.create(
                        customer=customer,
                        items=[{"plan": plan}],
                    )
        # Add user to subscriber model
        test_subscriber = Subscriber.objects.create(user=test_user1,
                                                    customer_id='12345',
                                                    subscription_id=subscription.id,
                                                    card_id='123456',
                                                    active=True)
        test_subscriber.save()
        # Assert subscriber is in group
        self.assertTrue(test_user1.groups.filter(name='Subscribers').exists())
        # Assert subscriber in model
        self.assertTrue(Subscriber.objects.filter().exists())
        # unsubscribe user
        response = self.client.get('/subscribe/unsubscribe/')
        # Check redirect
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'user_profile.html')
        self.assertFalse(test_user1.groups.filter(name='Subscribers').exists())

    def test_subscriber_created(self):
        # set up subscriber group
        Group.objects.create(name='Subscribers')
        # Set up and log in test user
        test_user1 = User.objects.create_user(first_name='test',
                                              username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up form data
        data = {
            'credit_card_number': "4242424242424242",
            'cvv': "123",
            'expiry_month': '11',
            'expiry_year': '2025',
            'stripe_id': 'tok_visa',
        }
        response = self.client.post('/subscribe/', data, follow=True)
        self.assertTrue(Subscriber.objects.filter().exists())
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have successfully subscribed.')

    def test_new_subscription_created_for_previous_subscriber(self):
        # set up subscriber group
        Group.objects.create(name='Subscribers')
        # Set up and log in test user
        test_user1 = User.objects.create_user(first_name='test',
                                              username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up form data
        data = {
            'credit_card_number': "4242424242424242",
            'cvv': "123",
            'expiry_month': '11',
            'expiry_year': '2025',
            'stripe_id': 'tok_visa',
        }
        self.client.post('/subscribe/', data, follow=True)
        self.assertTrue(Subscriber.objects.filter().exists())
        # user is an active subscriber
        self.assertTrue(Subscriber.objects.filter()[0].active == True)
        # initial subscription is
        subscription = Subscriber.objects.filter()[0].subscription_id
        # unsubscribe user
        self.client.post('/subscribe/unsubscribe/')
        # Subscriber should still exist but active is false and subscription id is cleared
        self.assertTrue(Subscriber.objects.filter()[0].active == False)
        self.assertTrue(Subscriber.objects.filter()[0].subscription_id == '')
        # User subscribes again
        data2 = {
            'credit_card_number': "4242424242424242",
            'cvv': "123",
            'expiry_month': '11',
            'expiry_year': '2025',
            'stripe_id': 'tok_visa',
        }
        response = self.client.post('/subscribe/', data2, follow=True)
        # user is an active subscriber, with a new subscription id
        self.assertTrue(Subscriber.objects.filter()[0].active == True)
        self.assertFalse(Subscriber.objects.filter()[0].subscription_id == '')
        self.assertFalse(Subscriber.objects.filter()[0].subscription_id == subscription)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have successfully subscribed.')
 
    def test_subscriber_details_updated(self):
        # set up subscriber group
        Group.objects.create(name='Subscribers')
        # Set up and log in test user
        test_user1 = User.objects.create_user(first_name='test',
                                              username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up form data
        data = {
            'credit_card_number': "4242424242424242",
            'cvv': "123",
            'expiry_month': '11',
            'expiry_year': '2025',
            'stripe_id': 'tok_visa',
        }
        # subscribe user
        self.client.post('/subscribe/', data, follow=True)
        # Assert subscriber is in group and model as a check
        self.assertTrue(test_user1.groups.filter(name='Subscribers').exists())
        self.assertTrue(Subscriber.objects.filter().exists())
        # Store db first card id and subscription id as variables
        subscriber = Subscriber.objects.get(user=test_user1.id)
        card1 = subscriber.card_id
        subscription1 = subscriber.subscription_id
        # Store stripe first card id as a variable
        customer = stripe.Customer.retrieve(subscriber.customer_id)
        card_stripe = stripe.Customer.retrieve_source(
                    subscriber.customer_id,
                    customer.default_source,
                )
        card1_stripe = card_stripe.id
        subscription1_stripe = str(customer.subscriptions.data[0].id)
        # set up form data with new card details
        data2 = {
            'credit_card_number': "4242424242424242",
            'cvv': "123",
            'expiry_month': '10',
            'expiry_year': '2024',
            'stripe_id': 'tok_mastercard',
        }
        # update card details of subscribed user
        self.client.post('/subscribe/update_card_details/', data2, follow=True)
        # Assert subscriber still in group and model as a check
        self.assertTrue(test_user1.groups.filter(name='Subscribers').exists())
        self.assertTrue(Subscriber.objects.filter().exists())
        # Store second card id as variable from db
        subscriber.refresh_from_db()
        card2 = subscriber.card_id
        subscription2 = subscriber.subscription_id
        # Fetch new stripe data for current card id
        customer = stripe.Customer.retrieve(subscriber.customer_id)
        card_stripe_2 = stripe.Customer.retrieve_source(
                    subscriber.customer_id,
                    customer.default_source,
                )
        card2_stripe = card_stripe_2.id
        subscription2_stripe = str(customer.subscriptions.data[0].id)
        # Assert card details have changed both in db and on stripe
        self.assertNotEqual(card1, card2)
        self.assertNotEqual(card1_stripe, card2_stripe)
        self.assertEqual(subscription1, subscription2)
        self.assertEqual(subscription1_stripe, subscription2_stripe)


class TestErrorMessages(TestCase):
    def test_card_error_messages_declined(self):
        # set up subscriber group
        Group.objects.create(name='Subscribers')
        # Set up and log in test user
        test_user1 = User.objects.create_user(first_name='test',
                                              username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up form data declined
        data = {
            'credit_card_number': "4242424242424242",
            'cvv': "134",
            'expiry_month': '11',
            'expiry_year': '2025',
            'stripe_id': 'tok_chargeDeclined',
        }
        # subscribe user
        response = self.client.post('/subscribe/', data, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your card was declined.')

    def test_invalid_form_error_message(self):
        # set up subscriber group
        Group.objects.create(name='Subscribers')
        # Set up and log in test user
        test_user1 = User.objects.create_user(first_name='test',
                                              username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up form data invalid - invalid month choice
        data = {
            'credit_card_number': "4242424242424242",
            'cvv': "134",
            'expiry_month': '11',
            'expiry_year': '2018',
            'stripe_id': 'tok_visa',
        }
        # subscribe user
        response = self.client.post('/subscribe/', data, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'We were unable to take a payment.')

    def test_card_error_message_on_update(self):
        # set up subscriber group
        Group.objects.create(name='Subscribers')
        # Set up and log in test user
        test_user1 = User.objects.create_user(first_name='test',
                                              username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up form data
        data = {
            'credit_card_number': "4242424242424242",
            'cvv': "123",
            'expiry_month': '11',
            'expiry_year': '2025',
            'stripe_id': 'tok_visa',
        }
        # subscribe user
        self.client.post('/subscribe/', data, follow=True)
        # card is declined error
        data2 = {
            'credit_card_number': "4242424242424242",
            'cvv': "134",
            'expiry_month': '11',
            'expiry_year': '2021',
            'stripe_id': 'tok_chargeDeclined',
        }
        # subscribe user
        response = self.client.post('/subscribe/update_card_details/', data2, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        print(str(messages[0]))
        self.assertEqual(str(messages[0]), 'Unable to update card details.')




    
        
