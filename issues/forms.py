from django import forms
from .models import Issue


class AddIssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('title', 'description', 'priority',)
