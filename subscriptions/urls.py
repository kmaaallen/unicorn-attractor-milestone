from django.conf.urls import url
from .views import new_subscription, unsubscribe

urlpatterns = [
    url(r'^$', new_subscription, name="subscribe"),
    url(r"^unsubscribe/", unsubscribe, name="unsubscribe"),
]
