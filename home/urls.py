from django.conf.urls import url
from home.views import find_out_more, contact_us, thanks


urlpatterns = [
    url(r'^more/', find_out_more, name="find_out_more"),
    url(r'^contact/', contact_us, name="contact_us"),
    url(r'^thanks/', thanks, name='thanks'),
]
