from django.test import TestCase
from django.contrib.auth.models import User
from .models import Issue, Vote


class TestIssuesPages(TestCase):

    def test_all_issues_page(self):
        # User should be able to access issue overview page
        response = self.client.get('/issues/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'issue_overview.html')
 
    def test_add_issue_page_logged_in_user(self):
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # User should be able to access add issue page if logged in
        response = self.client.get('/issues/report_issue/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'add_issue.html')

    def test_add_issue_page_logged_in_user_false(self):
        # User should be redirected to sign in page if not logged in
        response = self.client.get('/issues/report_issue/')
        # Check redirect
        self.assertRedirects(response, '/accounts/sign_in/?next=/issues/report_issue/')
    
    def test_full_issue_page_logged_in_user(self):
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up test issue to open
        test_issue = Issue.objects.create(title='test issue', description='test')
        test_issue.save()
        # User should be able to access add issue page if logged in
        response = self.client.get('/issues/full_issue/1/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'full_issue.html')
    
    def test_full_issue_page_logged_in_user_false(self):
        # set up test issue to open
        test_issue = Issue.objects.create(title='test issue', description='test')
        test_issue.save()
        # User should be redirected to sign in page if not logged in
        response = self.client.get('/issues/full_issue/1/')
        # Check redirect
        self.assertRedirects(response, '/accounts/sign_in/?next=/issues/full_issue/1/')
    
    def test_add_comment_page_logged_in_user(self):
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up test issue to open
        test_issue = Issue.objects.create(title='test issue', description='test')
        test_issue.save()
        # User should be able to access add issue page if logged in
        response = self.client.get('/issues/add_comment/1/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'add_comment.html')
    
    def test_add_comment_page_logged_in_user_false(self):
        # set up test issue to open
        test_issue = Issue.objects.create(title='test issue', description='test')
        test_issue.save()
        # User should be redirected to sign in page if not logged in
        response = self.client.get('/issues/add_comment/1/')
        # Check redirect
        self.assertRedirects(response, '/accounts/sign_in/?next=/issues/add_comment/1/')


class TestUpvote(TestCase):

    def test_new_upvote_applied(self):
        # set up issue
        test_issue = Issue.objects.create(title='test issue', description='test')
        test_issue.save()
        # set up and login user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # call upvote method
        data = {
            'issue': test_issue,
            'voter': test_user1,
        }
        self.client.post('/issues/upvote/1/', data, follow=True)
        test_issue.refresh_from_db()
        # assert vote object exists for this user and issue
        self.assertTrue(Vote.objects.filter()[0].voter == test_user1)
        self.assertTrue(Vote.objects.filter()[0].issue == test_issue)
        # assert vote is added to issue record
        self.assertEqual(test_issue.votes, 1)
        # assert voter is added to issue record
        self.assertEqual(test_issue.voters.filter()[0], test_user1)

    def test_upvote_not_allowed_if_already_voted(self):
        # set up issue
        test_issue = Issue.objects.create(title='test issue', description='test', votes=1)
        test_issue.save()
        # set up and login user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up vote object
        test_vote = Vote.objects.create(issue=test_issue, voter=test_user1)
        # call upvote method
        data = {
            'issue': test_issue,
            'voter': test_user1,
        }
        response = self.client.post('/issues/upvote/1/', data, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have already voted on this issue')

