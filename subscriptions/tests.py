from django.test import TestCase
from django.contrib.auth.models import User, Group


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

