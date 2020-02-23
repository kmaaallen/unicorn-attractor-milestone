from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import Feature, Vote
from django.shortcuts import reverse


class TestFeaturesPages(TestCase):

    def test_all_features_page(self):
        # User should be unable to access feature overview page without logging in
        response = self.client.get('/features/')
        # Check correct template
        self.assertRedirects(response, '/accounts/sign_in/?next=/features/')
    
    def test_all_features_page_logged_in(self):
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up and add user to subscribers group
        subscriber_group = Group.objects.create(name='Subscribers')
        subscriber_group.user_set.add(test_user1)
        # User should be abel to access feature overview page if logged in and in subscribers group
        response = self.client.get('/features/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'feature_overview.html')
 
    def test_add_feature_page_logged_in_user(self):
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # User should be able to access add feature page if logged in
        response = self.client.get('/features/request_feature/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'add_feature.html')

    def test_add_feature_page_logged_in_user_false(self):
        # User should be redirected to sign in page if not logged in
        response = self.client.get('/features/request_feature/')
        # Check redirect
        self.assertRedirects(response, '/accounts/sign_in/?next=/features/request_feature/')
    
    def test_add_comment_page_logged_in_user(self):
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up test issue to open
        test_feature = Feature.objects.create(title='test feature', description='test')
        test_feature.save()
        # User should be able to access add feature page if logged in
        response = self.client.get('/features/add_comment/1/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'add_feature_comment.html')
    
    def test_add_comment_page_logged_in_user_false(self):
        # set up test feature to open
        test_feature = Feature.objects.create(title='test feature', description='test')
        test_feature.save()
        # User should be redirected to sign in page if not logged in
        response = self.client.get('/features/add_comment/1/')
        # Check redirect
        self.assertRedirects(response, '/accounts/sign_in/?next=/features/add_comment/1/')


class TestUpvote(TestCase):

    def test_new_upvote_applied(self):
        # set up feature
        test_feature = Feature.objects.create(title='test feature', description='test')
        test_feature.save()
        # set up and login user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up and add user to subscribers group
        subscriber_group = Group.objects.create(name='Subscribers')
        subscriber_group.user_set.add(test_user1)
        # call upvote method
        data = {
            'feature': test_feature,
            'voter': test_user1,
        }
        self.client.post('/features/upvote/1/', data, follow=True)
        test_feature.refresh_from_db()
        # assert vote object exists for this user and feature
        self.assertTrue(Vote.objects.filter()[0].voter == test_user1)
        self.assertTrue(Vote.objects.filter()[0].feature == test_feature)
        # assert vote is added to issue record
        self.assertEqual(test_feature.votes, 1)
        # assert voter is added to feature record
        self.assertEqual(test_feature.voters.filter()[0], test_user1)

    def test_upvote_not_allowed_if_already_voted(self):
        # set up feature
        test_feature = Feature.objects.create(title='test feature', description='test', votes=1)
        test_feature.save()
        # set up and login user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up and add user to subscribers group
        subscriber_group = Group.objects.create(name='Subscribers')
        subscriber_group.user_set.add(test_user1)
        # set up vote object
        Vote.objects.create(feature=test_feature, voter=test_user1)
        # call upvote method
        data = {
            'feature': test_feature,
            'voter': test_user1,
        }
        response = self.client.post('/features/upvote/1/', data, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have already voted on this feature')


class TestMyFeatures(TestCase):
    def test_my_features_function(self):
        # set up and login user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up and add user to subscribers group
        subscriber_group = Group.objects.create(name='Subscribers')
        subscriber_group.user_set.add(test_user1)
        # set up features
        test_feature = Feature.objects.create(title='test feature', description='test', votes=1, reported_by=test_user1)
        test_feature.save()

        test_feature_2 = Feature.objects.create(title='test feature', description='test', votes=1, reported_by='bob')
        test_feature_2.save()