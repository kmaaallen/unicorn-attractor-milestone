from django.conf.urls import url, include
from accounts.views import sign_up, sign_in, sign_out, user_profile
from accounts import url_reset


urlpatterns = [
    url(r"^sign_out/", sign_out, name="sign_out"),
    url(r"^sign_in/", sign_in, name="sign_in"),
    url(r"^sign_up/", sign_up, name="sign_up"),
    url(r"^profile/", user_profile, name="profile"),
    url(r"password_reset/", include(url_reset)),
]
