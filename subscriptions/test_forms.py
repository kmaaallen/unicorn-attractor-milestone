from django.test import TestCase
from subscriptions.forms import SubscriptionForm
from subscriptions.models import Subscriber
from django.contrib.auth.models import User


class TestSubscriptionForm(TestCase):

    def test_valid_subscription_form_data(self):
        form = SubscriptionForm({
            'credit_card_number': "4242424242424242",
            'cvv': "123",
            'expiry_month': '11',
            'expiry_year': '2025',
            'stripe_id': 'tok_visa'
        })
        self.assertTrue(form.is_valid())

    """ def test_subscriber_created(self):
        # Set up and log in test user
        test_user1 = User.objects.create_user(first_name='test', username='testuser',
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
        self.client.post('/subscribe/', data, follow=True) """
        #self.assertTrue(Subscriber.objects.exists())
        #self.assertEqual(str(Subscriber.objects.filter()[0]), "test")
