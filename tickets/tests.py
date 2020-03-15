from django.test import TestCase
from django.contrib.auth.models import User, Group
from tickets.models import Ticket, Vote
from django.core.urlresolvers import reverse


class TestTicketsPages(TestCase):

    def test_all_tickets_page(self):
        Group.objects.create(name='Subscribers')
        # User should be able to access ticket overview page
        response = self.client.get('/tickets/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'ticket_overview.html')

    def test_my_tickets_page(self):
        Group.objects.create(name='Subscribers')
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()

        test_user2 = User.objects.create_user(username='testuser2',
                                              password='password2')
        test_user2.save()
        self.client.login(username='testuser', password='password')

        # set up test issue to open
        test_ticket = Ticket.objects.create(title='test issue',
                                            description='test',
                                            reported_by=test_user1)
        test_ticket.save()
        test_ticket_2 = Ticket.objects.create(title='test issue 2',
                                              description='test',
                                              reported_by=test_user2)
        test_ticket_2.save()

        # User should be able to access ticket overview page
        response = self.client.get('/tickets/my_tickets/')
        # Check response status
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'ticket_overview.html')
        self.assertQuerysetEqual(response.context['tickets'], ['<Ticket: test issue>'])
    
    def test_feature_tickets_page(self):
        Group.objects.create(name='Subscribers')
         # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up test issue to open
        test_ticket = Ticket.objects.create(title='test issue',
                                            description='test',
                                            category='ISSUE',
                                            reported_by=test_user1)
        test_ticket.save()
        test_ticket_2 = Ticket.objects.create(title='test issue 2',
                                              description='test',
                                              category='FEATURE',
                                              reported_by=test_user1)
        test_ticket_2.save()

        # User should be able to access ticket overview page
        response = self.client.get('/tickets/feature_tickets/')
        # Check response status
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'ticket_overview.html')
        self.assertQuerysetEqual(response.context['tickets'], ['<Ticket: test issue 2>'])
    
    def test_issue_tickets_page(self):
        Group.objects.create(name='Subscribers')
         # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up test issue to open
        test_ticket = Ticket.objects.create(title='test issue 1',
                                            description='test',
                                            category='ISSUE',
                                            reported_by=test_user1)
        test_ticket.save()
        test_ticket_2 = Ticket.objects.create(title='test issue 2',
                                              description='test',
                                              category='FEATURE',
                                              reported_by=test_user1)
        test_ticket_2.save()

        # User should be able to access ticket overview page
        response = self.client.get('/tickets/issue_tickets/')
        # Check response status
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'ticket_overview.html')
        self.assertQuerysetEqual(response.context['tickets'], ['<Ticket: test issue 1>'])
 
    def test_add_issue_page_logged_in_user(self):
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # User should be able to access add issue page if logged in
        response = self.client.get('/tickets/report_issue/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'add_ticket_issue.html')

    def test_add_issue_page_logged_in_user_false(self):
        # User should be redirected to sign in page if not logged in
        response = self.client.get('/tickets/report_issue/')
        # Check redirect
        self.assertRedirects(response, '/accounts/sign_in/?next=/tickets/report_issue/')

    def test_add_feature_page_logged_in_subscribed_user(self):
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # Add user to subscriber group
        subscriber_group = Group.objects.create(name='Subscribers')
        subscriber_group.user_set.add(test_user1)
        # User should be able to access add feature page if logged in and subscribed
        response = self.client.get('/tickets/request_feature/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'add_ticket_feature.html')

    def test_add_feature_page_logged_in_unsubscribed_user(self):
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')

        Group.objects.create(name='Subscribers')
        # User should not be able to access add feature page if logged in
        response = self.client.get('/tickets/request_feature/')
        # Check redirect
        self.assertRedirects(response, '/subscribe/')

    def test_add_feature_page_logged_in_user_false(self):
        # User should be redirected to sign in page if not logged in
        response = self.client.get('/tickets/request_feature/')
        # Check redirect
        self.assertRedirects(response, '/accounts/sign_in/')
    
    def test_full_ticket_page_logged_in_user(self):
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up test issue to open
        test_ticket = Ticket.objects.create(title='test issue', description='test')
        test_ticket.save()
        # User should be able to access add issue page if logged in
        response = self.client.get('/tickets/full_ticket/1/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'full_ticket.html')
    
    def test_full_ticket_page_logged_in_user_false(self):
        # set up test issue to open
        test_ticket = Ticket.objects.create(title='test issue', description='test')
        test_ticket.save()
        # User should be redirected to sign in page if not logged in
        response = self.client.get('/tickets/full_ticket/1/')
        # Check redirect
        self.assertRedirects(response, '/accounts/sign_in/?next=/tickets/full_ticket/1/')
    
    def test_add_comment_page_logged_in_user(self):
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up test issue to open
        test_ticket = Ticket.objects.create(title='test issue', description='test')
        test_ticket.save()
        # User should be able to access add issue page if logged in
        response = self.client.get('/tickets/add_ticket_comment/1/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'add_ticket_comment.html')
    
    def test_add_comment_page_logged_in_user_false(self):
        # set up test issue to open
        test_ticket = Ticket.objects.create(title='test issue', description='test')
        test_ticket.save()
        # User should be redirected to sign in page if not logged in
        response = self.client.get('/tickets/add_ticket_comment/1/')
        # Check redirect
        self.assertRedirects(response, '/accounts/sign_in/?next=/tickets/add_ticket_comment/1/')

    def test_edit_tickets_page(self):
        Group.objects.create(name='Subscribers')
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up test issue to open
        test_ticket = Ticket.objects.create(title='test issue', description='test', reported_by=test_user1)
        test_ticket.save()
        # User should be able to access ticket overview page
        response = self.client.get('/tickets/edit_ticket/1/')
        # Check response "success"
        self.assertEqual(response.status_code, 200)
        # Check correct template
        self.assertTemplateUsed(response, 'edit_ticket.html')


class TestUpvote(TestCase):

    def test_new_upvote_applied(self):
        Group.objects.create(name='Subscribers')
        # set up issue
        test_ticket = Ticket.objects.create(title='test issue',
                                            description='test',
                                            category='ISSUE')
        test_ticket.save()
        # set up and login user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # call upvote method
        data = {
            'ticket': test_ticket,
            'voter': test_user1,
        }
        self.client.post('/tickets/upvote/1/', data, follow=True)
        test_ticket.refresh_from_db()
        # assert vote object exists for this user and issue
        self.assertTrue(Vote.objects.filter()[0].voter == test_user1)
        self.assertTrue(Vote.objects.filter()[0].ticket == test_ticket)
        # assert vote is added to issue record
        self.assertEqual(test_ticket.votes, 1)
        # assert voter is added to issue record
        self.assertEqual(test_ticket.voters.filter()[0], test_user1)


class TestDelete(TestCase):

    def test_delete_successful(self):
        Group.objects.create(name='Subscribers')
        # set up and login user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up issue
        test_ticket = Ticket.objects.create(title='test issue',
                                            description='test',
                                            category='ISSUE',
                                            reported_by=test_user1)
        test_ticket.save()
        self.assertTrue(Ticket.objects.exists())
        self.client.post('/tickets/delete_ticket/1/', follow=True)
        self.assertFalse(Ticket.objects.exists())
