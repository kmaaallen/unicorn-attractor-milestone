from django.conf.urls import url
from .views import all_issues, report_issue

urlpatterns = [
    url(r'^$', all_issues, name="issues"),
    url(r'^report_issue/', report_issue, name="report_issue"),
]
