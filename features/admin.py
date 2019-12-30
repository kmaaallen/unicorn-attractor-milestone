from django.contrib import admin
from .models import Feature, Comment, Vote

# Register your models here.
admin.site.register(Feature)
admin.site.register(Vote)
admin.site.register(Comment)
