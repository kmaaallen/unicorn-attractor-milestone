from django.apps import apps
from django.test import TestCase
from .apps import FeaturesConfig


class TestFeaturesConfig(TestCase):

    def test_app(self):
        self.assertEqual("features", FeaturesConfig.name)
        self.assertEqual("features", apps.get_app_config("features").name)
