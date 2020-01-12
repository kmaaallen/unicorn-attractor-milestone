from django.test import TestCase
from .forms import AddIssueForm, AddCommentForm
from .models import Issue, Comment
from django.contrib.auth.models import User
from django.shortcuts import reverse


class TestIssueForms(TestCase):

    def test_valid_add_issue_form_data(self):
        form = AddIssueForm({
            'title': "Test Issue",
            'description': "My test issue",
            'priority': 'LOW'
        })
        self.assertTrue(form.is_valid())
        issue = form.save()
        self.assertEqual(issue.title, "Test Issue")
        self.assertEqual(issue.description, "My test issue")
        self.assertEqual(issue.priority, "LOW")

    def test_blank_issue_form_data(self):
        # Priority always has a default value
        form = AddIssueForm({'priority': "LOW"})
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
        test_issue = Issue.objects.create(title='test issue', description='test')
        test_issue.save()
        data = {
            'issue': test_issue.id,
            'commenter': test_user1,
            'comment': "My comment on this issue is"}
        response = self.client.post('/issues/add_comment/1/', data)
        self.assertTrue(Issue.objects.exists())
        self.assertTrue(Comment.objects.exists())
        # test redirects after successful comment submission
        self.assertRedirects(response, '/issues/')
        self.assertTrue(Comment.objects.filter()[0].comment == "My comment on this issue is")
        self.assertTrue(Comment.objects.filter()[0].commenter == test_user1)
        self.assertTrue(Comment.objects.filter()[0].issue == test_issue)
   
    def test_blank_comment_form_data(self):
        form = AddCommentForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'comment': ['This field is required.'],
        })
        self.assertFalse(Comment.objects.exists())
