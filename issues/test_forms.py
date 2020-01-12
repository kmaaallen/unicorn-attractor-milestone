from django.test import TestCase
from .forms import AddIssueForm, AddCommentForm
from .models import Issue
from django.contrib.auth.models import User


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
    
    """ def test_valid_add_comment_form_data(self):
        # Have to have an issue
        test_issue = Issue.objects.create(title='test issue', description='test')
        test_issue.save()
        form = AddCommentForm({
            'comment': "My comment on this issue is"
        })
        self.assertTrue(form.is_valid())s
        comment = form.save()
        self.assertEqual(comment.comment, 'My comment on this issue is') """

    def test_blank_comment_form_data(self):
        form = AddCommentForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'comment': ['This field is required.'],
        })
