from django.conf.urls import url
from accounts.views import sign_up, sign_in, sign_out

urlpatterns = [
    url(r"^sign_out/$", sign_out, name="sign_out"),
    url(r"^sign_in/$", sign_in, name="sign_in"),
    url(r"^sign_up/$", sign_up, name="sign_up"),
]
