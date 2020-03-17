from django.test import TestCase
from subscriptions.forms import SubscriptionForm


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

    def test_invalid_subscription_form_data(self):
        form = SubscriptionForm({
            'credit_card_number': "4242424242424242",
            'cvv': "123",
            'expiry_month': '11',
            'expiry_year': '2019',
            'stripe_id': 'tok_visa'
        })
        self.assertFalse(form.is_valid())
        #response = self.client.post('/subscribe/', form, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your card was declined.')

    
    
