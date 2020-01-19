from django.test import TestCase


class TestSubscriptionPage():
    def test_subscriptions_page(self):
        # User should be able to access subscription page
        response = self.client.get('/subscribe/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'subscribe.html')

