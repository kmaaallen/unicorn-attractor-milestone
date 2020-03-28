from django.test import TestCase
from tickets.forms import AddTicketForm, AddCommentForm
from tickets.models import Ticket, Comment
from django.contrib.auth.models import User, Group


class TestTicketForms(TestCase):

    def test_valid_add_ticket_form_data(self):
        form = AddTicketForm({
            'title': "Test Issue",
            'description': "My test issue",
            'priority': 'LOW',
        })
        self.assertTrue(form.is_valid())
        ticket = form.save()
        self.assertEqual(ticket.title, "Test Issue")
        self.assertEqual(ticket.description, "My test issue")
        self.assertEqual(ticket.priority, "LOW")

    def test_valid_add_ticket_form_data_issue(self):
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        data = {
            'title': "Test Issue",
            'description': "My test issue",
            'priority': 'LOW',
        }
        self.client.post('/tickets/report_issue/', data)
        tick_rec = Ticket.objects.filter()[0]
        self.assertEqual(tick_rec.title, "Test Issue")
        self.assertEqual(tick_rec.description, "My test issue")
        self.assertEqual(tick_rec.priority, "LOW")
        self.assertEqual(tick_rec.category, "ISSUE")

    def test_valid_add_ticket_form_data_feature(self):
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        subscriber_group = Group.objects.create(name='Subscribers')
        subscriber_group.user_set.add(test_user1)

        data = {
            'title': "Test Feature",
            'description': "My test feature",
            'priority': 'HIGH',
        }
        self.client.post('/tickets/request_feature/', data)
        tick_rec2 = Ticket.objects.filter()[0]
        self.assertEqual(tick_rec2.title, "Test Feature")
        self.assertEqual(tick_rec2.description, "My test feature")
        self.assertEqual(tick_rec2.priority, "HIGH")
        self.assertEqual(tick_rec2.category, "FEATURE")

    def test_valid_ticket_form_redirect(self):
        Group.objects.create(name='Subscribers')
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        data = {
            'title': "Test Issue",
            'description': "My test issue",
            'priority': 'LOW',
            'category': 'ISSUE'
        }
        response = self.client.post('/tickets/report_issue/', data)
        self.assertRedirects(response, '/tickets/')

    def test_blank_ticket_form_data(self):
        # Priority always has a default value
        form = AddTicketForm({'priority': "LOW"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'title': ['This field is required.'],
            'description': ['This field is required.'],
        })

    def test_valid_add_comment_form_data(self):
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up ticket
        test_ticket = Ticket.objects.create(title='test issue',
                                            description='test',
                                            category='ISSUE')
        test_ticket.save()
        Group.objects.create(name='Subscribers')
        data = {
            'ticket': test_ticket.id,
            'commenter': test_user1,
            'comment': "My comment on this issue is"}
        response = self.client.post('/tickets/add_ticket_comment/1/', data)
        self.assertTrue(Ticket.objects.exists())
        self.assertTrue(Comment.objects.exists())
        # test redirects after successful comment submission
        self.assertRedirects(response, '/tickets/')
        comm_rec = Comment.objects.filter()[0]
        self.assertTrue(comm_rec.comment == "My comment on this issue is")
        self.assertTrue(comm_rec.commenter == test_user1)
        self.assertTrue(comm_rec.ticket == test_ticket)
        self.assertEqual(str(comm_rec),
                         "My comment on this issue is")

    def test_blank_comment_form_data(self):
        form = AddCommentForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'comment': ['This field is required.'],
        })
        self.assertFalse(Comment.objects.exists())

    def test_edit_ticket_data(self):
        Group.objects.create(name='Subscribers')
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up ticket
        test_ticket = Ticket.objects.create(title='test issue',
                                            description='test',
                                            category='ISSUE')
        test_ticket.save()
        self.assertTrue(Ticket.objects.exists())
        self.assertTrue(Ticket.objects.filter()[0].title == "test issue")
        data = {
            'title': "Test Issue Edit",
            'description': "My test issue",
            'priority': 'LOW',
            'category': 'ISSUE'
        }
        self.client.post('/tickets/edit_ticket/1/', data)
        self.assertTrue(Ticket.objects.exists())
        self.assertTrue(Ticket.objects.filter()[0].title == "Test Issue Edit")
