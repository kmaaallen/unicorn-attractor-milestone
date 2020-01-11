from django.test import TestCase
from django.contrib.auth.models import Group, User


class TestHome(TestCase):

    def test_homepage(self):
        # User should be able to access index homepage
        response = self.client.get('/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'index.html')

    def test_homepage_button_if_not_logged_in(self):
        # Test dynamic content button on index page is 'Sign up/Sign In'
        # when user is not logged in
        response = self.client.get('/')
        self.assertContains(response, 'Sign Up / Sign In', html=True)

    def test_homepage_button_if_logged_in(self):
        # Test dynamic content button on index page is 'Logout'
        # when user is logged in
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        response = self.client.get('/')
        self.assertContains(response, 'Logout', html=True)

    def test_more_page(self):
        # create 'Subscribers' group for test database
        Group.objects.get_or_create(name='Subscribers')
        # User should be able to access find out more page
        response = self.client.get('/home/more/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'more.html')

    def test_contact_page_reachable(self):
        # User should be able to access contact page
        response = self.client.get('/home/contact/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'contact.html')

    def test_thanks_page_not_reachable_without_contact_variable(self):
        # User should not be able to access thanks page without filling in contact form
        response = self.client.get('/home/thanks/')
        # Check response "success"
        self.assertNotEqual(response.status_code, 200)
    
    def test_thanks_page_reachable_with_contact_variable(self):
        # set contact session variable
        session = self.client.session
        session['contacted'] = True
        session.save()
        # User should be able to access thanks page after filling in contact form
        response = self.client.get('/home/thanks/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'thanks.html')
