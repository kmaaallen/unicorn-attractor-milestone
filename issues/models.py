from django.db import models
from django.conf import settings

# Create your models here.


class Issue(models.Model):

    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    REPORTED = 'REPORTED'
    WORKING = 'IN PROGRESS'
    COMPLETED = 'COMPLETED'
    STATE_CHOICES = [
        (REPORTED, 'REPORTED'),
        (WORKING, 'IN PROGRESS'),
        (COMPLETED, 'COMPLETED')
    ]

    title = models.CharField(max_length=254, default='')
    description = models.TextField(max_length=300)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES,
                                default=LOW,)
    state = models.CharField(max_length=11, choices=STATE_CHOICES,
                             default=REPORTED,)
    votes = models.IntegerField(default=0)
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL)

    class Meta:
        ordering = ('-votes',)

    def __str__(self):
        return self.title


class Vote(models.Model):
    issue = models.ForeignKey('Issue')
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, default=0)

    class Meta:
        unique_together = ('issue', 'voter')


class Comment(models.Model):
    issue = models.ForeignKey('Issue', related_name='comments', default=None)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, default=0)
    comment = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.comment
