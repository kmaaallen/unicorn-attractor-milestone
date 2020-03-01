from django import forms
from .models import Ticket, Comment


class AddTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'priority',)


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
