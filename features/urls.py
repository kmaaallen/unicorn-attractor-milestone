from django.conf.urls import url
from .views import all_features, request_feature, add_comment, upvote, full_feature, my_features

urlpatterns = [
    url(r'^$', all_features, name="features"),
    url(r'^my_features/', my_features, name="my_features"),
    url(r'^request_feature/', request_feature, name="request_feature"),
    url(r'^upvote/(?P<feature_id>[0-9]+)/$', upvote, name='upvote'),
    url(r'^full_feature/(?P<feature_id>[0-9]+)/$', full_feature,
        name='full_feature'),
    url(r'^add_comment/(?P<feature_id>[0-9]+)/$', add_comment,
        name='add_feature_comment'),
]
