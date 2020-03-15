from django.conf.urls import url
from .views import all_tickets, my_tickets, report_issue, request_feature
from .views import add_ticket_comment, upvote, full_ticket, edit_ticket
from .views import delete_ticket, feature_tickets, issue_tickets

urlpatterns = [
    url(r'^$', all_tickets, name="tickets"),
    url(r'^my_tickets/', my_tickets, name="my_tickets"),
    url(r'^feature_tickets/', feature_tickets, name="feature_tickets"),
    url(r'^issue_tickets/', issue_tickets, name="issue_tickets"),
    url(r'^report_issue/', report_issue, name="report_issue"),
    url(r'^request_feature/', request_feature, name="request_feature"),
    url(r'^edit_ticket/(?P<ticket_id>[0-9]+)/$', edit_ticket,
        name='edit_ticket'),
    url(r'^delete_ticket/(?P<ticket_id>[0-9]+)/$', delete_ticket,
        name='delete_ticket'),
    url(r'^upvote/(?P<ticket_id>[0-9]+)/$', upvote, name='upvote'),
    url(r'^full_ticket/(?P<ticket_id>[0-9]+)/$', full_ticket,
        name='full_ticket'),
    url(r'^add_ticket_comment/(?P<ticket_id>[0-9]+)/$', add_ticket_comment,
        name='add_ticket_comment'),
]
