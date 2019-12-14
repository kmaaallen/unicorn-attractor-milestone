from django.db import models

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
