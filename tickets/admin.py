from django.contrib import admin
from .models import Ticket, Vote, Comment

# Register your models here.
admin.site.register(Ticket)
admin.site.register(Vote)
admin.site.register(Comment)
