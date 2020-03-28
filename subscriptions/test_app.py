from django.apps import apps
from django.test import TestCase
from subscriptions.apps import SubscriptionsConfig


class TestHomeConfig(TestCase):

    def test_app(self):
        self.assertEqual("subscriptions", SubscriptionsConfig.name)
        self.assertEqual("subscriptions",
                         apps.get_app_config("subscriptions").name)
