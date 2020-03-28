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
