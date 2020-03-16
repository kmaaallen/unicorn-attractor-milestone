from django.test import TestCase
from django.contrib.auth.models import User, Group
from subscriptions.models import Subscriber
from django.conf import settings

import stripe
stripe.api_key = settings.STRIPE_SECRET


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
        self.client.post('/subscribe/', data, follow=True)
        self.assertTrue(Subscriber.objects.filter().exists())

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
        card1 = 'tok_visa'
        data = {
            'credit_card_number': "4242424242424242",
            'cvv': "123",
            'expiry_month': '11',
            'expiry_year': '2025',
            'stripe_id': card1,
        }
        # subscribe user
        self.client.post('/subscribe/', data, follow=True)
        # Assert subscriber is in group and model as a check
        self.assertTrue(test_user1.groups.filter(name='Subscribers').exists())
        self.assertTrue(Subscriber.objects.filter().exists())
        # Store first card id as variable
        subscriber = Subscriber.objects.get(user=test_user1.id)
        card1 = subscriber.card_id
        print('card 1 is', card1)
        # set up form data
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
        # Store second card id as variable
        card2 = subscriber.card_id
        print('card 2 is', card2)
        # Assert card details have changed
        self.assertNotEqual(card1, card2)
        
        