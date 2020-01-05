from django.test import TestCase
from django.contrib.auth.models import Group

# Create your tests here.


class TestHome(TestCase):

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_more_page(self):
        # create 'Subscribers' group for test database
        Group.objects.get_or_create(name='Subscribers')
        response = self.client.get('/more/')
        self.assertEqual(response.status_code, 200)

    def test_contact_page(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
