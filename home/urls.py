from django.conf.urls import url
from home.views import landing_page, find_out_more, contact_us, thanks


urlpatterns = [
    url(r'^$', landing_page, name="landing_page"),
    url(r'^more/', find_out_more, name="find_out_more"),
    url(r'^contact/', contact_us, name="contact_us"),
    url(r'^thanks/', thanks, name='thanks'),
]
