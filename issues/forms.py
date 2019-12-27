from django import forms
from .models import Issue, Comment


class AddIssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('title', 'description', 'priority',)


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
