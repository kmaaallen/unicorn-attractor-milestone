from django.db import models
from django.conf import settings

# Create your models here.


class Ticket(models.Model):

    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    REPORTED = 'REPORTED'
    REQUESTED = 'REQUESTED'
    WORKING = 'IN PROGRESS'
    COMPLETED = 'COMPLETED'
    STATE_CHOICES = [
        (REQUESTED, 'REQUESTED'),
        (REPORTED, 'REPORTED'),
        (WORKING, 'IN PROGRESS'),
        (COMPLETED, 'COMPLETED')
    ]

    ISSUE = 'ISSUE'
    FEATURE = 'FEATURE'
    CATEGORY_CHOICES = [
        (ISSUE, 'ISSUE'),
        (FEATURE, 'FEATURE')
    ]

    title = models.CharField(max_length=254, default='')
    created_on = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES,
                                default=ISSUE,)
    description = models.TextField(max_length=300)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES,
                                default=LOW,)
    state = models.CharField(max_length=11, choices=STATE_CHOICES,
                             default=REPORTED,)
    votes = models.IntegerField(default=0)
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='ticket_reported_by',
                                    null=True,
                                    blank=True)

    class Meta:
        ordering = ('-votes',)

    def __str__(self):
        return self.title


class Vote(models.Model):
    ticket = models.ForeignKey('Ticket')
    voter = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='ticket_voter', default='')

    class Meta:
        unique_together = ('ticket', 'voter')


class Comment(models.Model):
    ticket = models.ForeignKey('Ticket', related_name='comments', default=None)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='ticket_commenter', default=0)
    comment = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.comment
