from django.conf.urls import url
from .views import all_tickets, my_tickets, report_issue, request_feature, add_comment, upvote, full_ticket

urlpatterns = [
    url(r'^$', all_tickets, name="tickets"),
    url(r'^my_tickets/', my_tickets, name="my_tickets"),
    url(r'^report_issue/', report_issue, name="report_issue"),
    url(r'^request_feature/', request_feature, name="request_feature"),
    url(r'^upvote/(?P<ticket_id>[0-9]+)/$', upvote, name='upvote'),
    url(r'^full_ticket/(?P<ticket_id>[0-9]+)/$', full_ticket, name='full_ticket'),
    url(r'^add_comment/(?P<ticket_id>[0-9]+)/$', add_comment,
        name='add_comment'),
]
