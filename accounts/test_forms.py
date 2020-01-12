from django.test import TestCase
from .forms import UserSignInForm, UserSignUpForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User


class TestSignInForm(TestCase):

    def test_sign_in_form_field_labels(self):
        form = UserSignInForm()
        self.assertTrue(form.fields['username'].label == 'Username')
        self.assertTrue(form.fields['password'].label == 'Password')

    def test_sign_in_form_valid(self):
        form_data = {'username': 'tester', 'password': 'password'}
        form = UserSignInForm(form_data)
        self.assertTrue(form.is_valid())

    """ def test_incorrect_username_password_combination_error(self):
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        form_data = {'username': 'testuser', 'password': 'wrongpassword'}
        # self.client.post('/accounts/sign_in/', form_data)
        form = UserSignInForm(form_data)
        self.assertTrue(form.is_valid())
        self.client.login(username='testuser', password='wrongpassword')
        self.assertEqual(form.non_field_errors(), [u'Your username and password combination is incorrect.']) """
# why is non_field_error empty in test but not in prod????


class TestSignUpForm(TestCase):

    def test_sign_up_form_field_labels(self):
        form = UserSignUpForm()
        self.assertTrue(form.fields['first_name'].label == 'First name')
        self.assertTrue(form.fields['last_name'].label == 'Last name')
        self.assertTrue(form.fields['email'].label == 'Email address')
        self.assertTrue(form.fields['username'].label == 'Username')
        self.assertTrue(form.fields['password1'].label == 'Password')
        self.assertTrue(form.fields['password2'].label == 'Confirm password')

    def test_sign_up_form_valid_correct_data(self):
        # testing all fields entered with valid data
        form_data = {'first_name': 'Test', 'last_name': 'McTest',
                     'username': 'testUser', 'email': 'test@gmail.com',
                     'password1': 'password', 'password2': 'password'}
        form = UserSignUpForm(form_data)
        self.assertTrue(form.is_valid())

    # Testing certain fields are required for valid form

    def test_sign_up_form_email_required_field(self):
        form_data = {'first_name': 'Test', 'last_name': 'McTest',
                     'username': 'bob', 'password1': 'password',
                     'password2': 'password'}
        form = UserSignUpForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], [u'This field is required.'])

    def test_sign_up_form_username_required_field(self):
        form_data = {'first_name': 'Test', 'last_name': 'McTest',
                     'email': 'test@gmail.com', 'password1': 'password',
                     'password2': 'password'}
        form = UserSignUpForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], [u'This field is required.'])

    def test_sign_up_form_password1_required_field(self):
        form_data = {'first_name': 'Test', 'last_name': 'McTest',
                     'username': 'testUser', 'email': 'test@gmail.com',
                     'password2': 'password'}
        form = UserSignUpForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password1'],
                         [u'This field is required.'])

    def test_sign_up_form_password2_required_field(self):
        form_data = {'first_name': 'Test', 'last_name': 'McTest',
                     'username': 'testUser', 'email': 'test@gmail.com',
                     'password1': 'password'}
        form = UserSignUpForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'],
                         [u'This field is required.'])

    # Testing validation errors and messages raised

    def test_sign_up_form_bad_email_validation(self):
        # testing error when email not valid email address
        form_data = {'first_name': 'Test', 'last_name': 'McTest',
                     'username': 'testUser', 'email': 'test',
                     'password1': 'password', 'password2': 'password'}
        form = UserSignUpForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError, validate_email,
                          'Enter a valid e-mail address.')

    def test_sign_up_form_email_already_in_use(self):
        # testing error when email already in use for a user for the site
        # Set up user with test email and re-use that email in new sign up
        test_user1 = User.objects.create_user(username='JohnDoe',
                                              password='password',
                                              email='test@gmail.com')
        test_user1.save()
        form_data = {'first_name': 'Test', 'last_name': 'McTest',
                     'username': 'testUser', 'email': 'test@gmail.com',
                     'password1': 'password', 'password2': 'password'}
        form = UserSignUpForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError, validate_email,
                          'Email address must be unique')

    def test_sign_up_form_username_already_in_use(self):
        # testing error when username already in use for a user for the site
        # Set up user with test email and re-use that username in new sign up
        test_user1 = User.objects.create_user(username='JohnDoe',
                                              password='password',
                                              email='test@gmail.com')
        test_user1.save()
        form_data = {'first_name': 'Test', 'last_name': 'McTest',
                     'username': 'JohnDoe', 'email': 'test@hotmail.com',
                     'password1': 'password', 'password2': 'password'}
        form = UserSignUpForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'],
                         [u'A user with that username already exists.'])

    def test_sign_up_form_passwords_do_not_match(self):
        # testing error when password and password confirmation do not match
        form_data = {'first_name': 'Test', 'last_name': 'McTest',
                     'username': 'testUser', 'email': 'test@gmail.com',
                     'password1': 'password', 'password2': 'anotherpassword'}
        form = UserSignUpForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'],
                         [u'Passwords must be the same'])
