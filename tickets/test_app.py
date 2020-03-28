from django.apps import apps
from django.test import TestCase
from tickets.apps import TicketsConfig


class TestTicketsConfig(TestCase):

    def test_app(self):
        self.assertEqual("tickets", TicketsConfig.name)
        self.assertEqual("tickets", apps.get_app_config("tickets").name)
