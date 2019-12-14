from django.conf.urls import url
from .views import all_features, request_feature

urlpatterns = [
    url(r'^$', all_features, name="features"),
    url(r'^request_feature/', request_feature, name="request_feature"),
]
