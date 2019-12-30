from django.db import models
from django.conf import settings

# Create your models here.


class Feature(models.Model):

    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    REQUESTED = 'REQUESTED'
    WORKING = 'IN PROGRESS'
    COMPLETED = 'COMPLETED'
    STATE_CHOICES = [
        (REQUESTED, 'REQUESTED'),
        (WORKING, 'IN PROGRESS'),
        (COMPLETED, 'COMPLETED')
    ]

    title = models.CharField(max_length=254, default='')
    description = models.TextField()
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES,
                                default=LOW,)
    state = models.CharField(max_length=11, choices=STATE_CHOICES,
                             default=REQUESTED,)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Vote(models.Model):
    feature = models.ForeignKey('Feature')
    voter = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name="featurevoter", default=0)

    class Meta:
        unique_together = ('feature', 'voter')


class Comment(models.Model):
    feature = models.ForeignKey('Feature', related_name='comments',
                                default=None)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name="featurecommenter", default=0)
    comment = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.comment
