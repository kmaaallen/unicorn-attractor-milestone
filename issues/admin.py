from django.contrib import admin
from .models import Issue, Vote, Comment

# Register your models here.
admin.site.register(Issue)
admin.site.register(Vote)
admin.site.register(Comment)
