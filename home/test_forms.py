from django.test import TestCase
from home.forms import ContactForm
from django.core import mail
from django.conf import settings
from django.contrib.auth.models import User


class TestHomeForms(TestCase):

    def test_valid_contact_form_data(self):
        form = ContactForm({
            'name': "Test User",
            'email': "mytestuser@example.com",
            'message': "Here is my test message",
        })
        self.assertTrue(form.is_valid())
        message = form.save()
        self.assertEqual(message.name, "Test User")
        self.assertEqual(message.email, "mytestuser@example.com")
        self.assertEqual(message.message, "Here is my test message")
        self.assertTrue('contacted')

    def test_valid_contact_form_data_logged_in(self):
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password',
                                              first_name='Test',
                                              last_name='User',
                                              email='mytestuser@example.com')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # go to contact form
        response = self.client.get('/home/contact/')
        self.assertEqual(response.context['form'].initial['name'], 'Test User')
        self.assertEqual(response.context['form'].initial['email'],
                         'mytestuser@example.com')

    def test_blank_contact_form_data(self):
        form = ContactForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['This field is required.'],
            'email': ['This field is required.'],
            'message': ['This field is required.'],
        })

    def test_send_contact_form(self):
        """
        Sends an email with details from the contact form
        """
        self.client.post("/home/contact/",
                         {'name': "Test User",
                          'email': "mytestuser@example.com",
                          'message': "Here is my test message"})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Contact Form')
        self.assertEqual(mail.outbox[0].from_email, 'mytestuser@example.com')
        self.assertEqual(mail.outbox[0].to, [settings.EMAIL_HOST_USER])
        self.assertEqual(mail.outbox[0].body,
                         '{0} has sent you a new message:\n\n{1} \n\nTheir'
                         ' contact email'
                         ' is: {2}'.format('Test User',
                                           'Here is my test message',
                                           'mytestuser@example.com'))
