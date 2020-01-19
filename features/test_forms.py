from django.test import TestCase
from .forms import AddFeatureForm, AddCommentForm
from .models import Feature, Comment
from django.contrib.auth.models import User, Group


class TestFeatureForms(TestCase):

    def test_valid_add_feature_form_data(self):
        form = AddFeatureForm({
            'title': "Test Feature",
            'description': "My test feature",
            'priority': 'LOW'
        })
        self.assertTrue(form.is_valid())
        feature = form.save()
        self.assertEqual(feature.title, "Test Feature")
        self.assertEqual(feature.description, "My test feature")
        self.assertEqual(feature.priority, "LOW")

    def test_valid_feature_form_redirect(self):
        # Set up and log in test user
        test_user1 = User.objects.create_user(username='testuser',
                                              password='password')
        test_user1.save()
        self.client.login(username='testuser', password='password')
        # set up and add user to subscribers group
        subscriber_group = Group.objects.create(name='Subscribers')
        subscriber_group.user_set.add(test_user1)
        data = {
            'title': "Test Feature",
            'description': "My test feature",
            'priority': 'LOW'
        }
        response = self.client.post('/features/request_feature/', data)
        self.assertRedirects(response, '/features/')

    def test_blank_feature_form_data(self):
        # Priority always has a default value
        form = AddFeatureForm({'priority': "LOW"})
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
        # set up and add user to subscribers group
        subscriber_group = Group.objects.create(name='Subscribers')
        subscriber_group.user_set.add(test_user1)
        # set up feature
        test_feature = Feature.objects.create(title='test feature', description='test')
        test_feature.save()
        data = {
            'feature': test_feature.id,
            'commenter': test_user1,
            'comment': "My comment on this feature is"}
        response = self.client.post('/features/add_comment/1/', data)
        self.assertTrue(Feature.objects.exists())
        self.assertTrue(Comment.objects.exists())
        # test redirects after successful comment submission
        self.assertRedirects(response, '/features/')
        self.assertTrue(Comment.objects.filter()[0].comment == "My comment on this feature is")
        self.assertTrue(Comment.objects.filter()[0].commenter == test_user1)
        self.assertTrue(Comment.objects.filter()[0].feature == test_feature)
        self.assertEqual(str(Comment.objects.filter()[0]), "My comment on this feature is")
   
    def test_blank_comment_form_data(self):
        form = AddCommentForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'comment': ['This field is required.'],
        })
        self.assertFalse(Comment.objects.exists())
