from django.test import TestCase
from django.contrib.auth.models import Group, User
from django.urls import reverse


class TestAccountsPages(TestCase):
    def test_sign_in_page_user_logged_out(self):
        # User should be able to access this page
        response = self.client.get('/accounts/sign_in/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'sign_in.html')

    def test_sign_in_page_user_logged_in(self):
        # User should be redirected to index page if already logged in
        # set up and log in user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        response = self.client.get('/accounts/sign_in/')
        # check correct redirect
        self.assertRedirects(response, '/')

    def test_sign_up_page_user_logged_out(self):
        # User should be able to access this page if logged out
        response = self.client.get('/accounts/sign_up/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'sign_up.html')

    def test_sign_up_page_user_logged_in(self):
        # User should be redirected to index page if already logged in
        # set up and log in user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        response = self.client.get('/accounts/sign_up/')
        # check correct redirect
        self.assertRedirects(response, '/')

    def test_user_profile_page_user_logged_in(self):
        # create 'Subscribers' group for test database
        Group.objects.get_or_create(name='Subscribers')
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('profile'))
        # Check user is logged in
        self.assertEqual(str(response.context['user']), 'testuser')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'user_profile.html')

    def test_user_profile_page_user_logged_out(self):
        # user should be redirected to sign in page
        response = self.client.get(reverse('profile'))
        # check correct redirect
        self.assertRedirects(response,
                             '/accounts/sign_in/?next=/accounts/profile/')


class TestLoginLogout(TestCase):

    def test_user_logout(self):
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        response = self.client.get('/accounts/sign_out/')
        self.assertRedirects(response, '/accounts/sign_in/')

    def test_user_login(self):
        # create 'Subscribers' group for test database
        Group.objects.get_or_create(name='Subscribers')
        # Set up test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        data = {
            'username': 'testuser',
            'password': 'password'
        }
        response = self.client.post('/accounts/sign_in/', data)
        self.assertRedirects(response, '/home/more/')
