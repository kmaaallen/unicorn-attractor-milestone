from django.conf.urls import url
from .views import new_subscription

urlpatterns = [
    url(r'^$', new_subscription, name="new_subscription"),
]
