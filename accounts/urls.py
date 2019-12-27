from django.conf.urls import url, include
from django.contrib.auth.views import password_reset, password_reset_complete, password_reset_confirm, password_reset_done
from accounts.views import sign_up, sign_in, sign_out
from accounts import url_reset


urlpatterns = [
    url(r"^sign_out/", sign_out, name="sign_out"),
    url(r"^sign_in/", sign_in, name="sign_in"),
    url(r"^sign_up/", sign_up, name="sign_up"),
    url(r"password_reset/", include(url_reset)),
]

