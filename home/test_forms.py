from django.test import TestCase
from .forms import ContactForm


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

    def test_blank_contact_form_data(self):
        form = ContactForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['This field is required.'],
            'email': ['This field is required.'],
            'message': ['This field is required.'],
        })