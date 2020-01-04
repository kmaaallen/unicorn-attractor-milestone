from django.test import TestCase
from django.contrib.auth.models import Group

# Create your tests here.


class TestAccounts(TestCase):
    def test_sign_in_page(self):
        response = self.client.get('/accounts/sign_in')
        self.assertEqual(response.status_code, 200)

    def test_sign_up_page(self):
        response = self.client.get('/more/')
        self.assertEqual(response.status_code, 200) 

    def test_user_profile_page(self):
        # create 'Subscribers' group for test database
        Group.objects.get_or_create(name='Subscribers')
        User.objects.create()
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
