from django.db import models
from django.contrib.auth.models import User


class Subscriber(models.Model):
    user = models.ForeignKey(User)
    customer_id = models.CharField(max_length=30, blank=True)
    subscription_id = models.CharField(max_length=30, blank=True)
    card_id = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = 'subscribers'

    def __str__(self):
        return self.user.username
