from django.conf.urls import url
from .views import all_issues, report_issue, upvote

urlpatterns = [
    url(r'^$', all_issues, name="issues"),
    url(r'^report_issue/', report_issue, name="report_issue"),
    url(r'^upvote/(?P<issue_id>[0-9]+)/$', upvote, name='upvote'),
]
