from django.conf.urls import url
from .views import new_subscription, unsubscribe, update_card_details

urlpatterns = [
    url(r'^$', new_subscription, name="subscribe"),
    url(r"^unsubscribe/", unsubscribe, name="unsubscribe"),
    url(r'^update_card_details/', update_card_details, name="update_card_details")
]
