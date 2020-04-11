from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, Vote, Comment
from .forms import AddTicketForm, AddCommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.contrib import messages

# Create your views here.


def all_tickets(request):
    tickets = Ticket.objects.all()
    context = {
        'ticket_view': 'all'
    }
    return render(request, "ticket_overview.html", {"tickets": tickets},
                  context)

@login_required
def search_tickets(request):
    """ Display search results from query across title and description fields"""
    q = request.GET.get('q')
    if q:
        query = SearchQuery(q)
        tickets = Ticket.objects.annotate(search=SearchVector('title', 'description'),).filter(search=query)
    context = {
        'ticket_view': 'search_results'
    }
    return render(request, "ticket_overview.html", {"tickets": tickets}, context)


@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(reported_by=request.user)
    context = {
        'ticket_view': 'mine'
    }
    return render(request, "ticket_overview.html", {"tickets": tickets},
                  context)


@login_required
def feature_tickets(request):
    tickets = Ticket.objects.filter(category='FEATURE')
    context = {
        'ticket_view': 'features'
    }
    return render(request, "ticket_overview.html", {"tickets": tickets},
                  context)

@login_required
def issue_tickets(request):
    tickets = Ticket.objects.filter(category='ISSUE')
    context = {
        'ticket_view': 'issues'
    }
    return render(request, "ticket_overview.html", {"tickets": tickets},
                  context)


@login_required
def report_issue(request, pk=None):
    """
    Create a view that allows users to report an issue
    """
    issue = get_object_or_404(Ticket, pk=pk) if pk else None
    if request.method == 'POST':
        form = AddTicketForm(request.POST, request.FILES, instance=issue)
        if form.is_valid():
            issue = form.save()
            issue.reported_by = request.user
            issue.category = 'ISSUE'
            issue.save()
            return redirect('tickets')
    else:
        form = AddTicketForm(instance=issue)
    return render(request, 'add_ticket_issue.html', {'form': form})


@login_required(redirect_field_name=None)
def request_feature(request, pk=None):
    """
    Create a view that allows users to request a feature
    """
    if request.user.groups.filter(name='Subscribers').exists():
        feature = get_object_or_404(Ticket, pk=pk) if pk else None
        if request.method == 'POST':
            form = AddTicketForm(request.POST, request.FILES, instance=feature)
            if form.is_valid():
                feature = form.save()
                feature.reported_by = request.user
                feature.category = 'FEATURE'
                feature.save()
                return redirect('tickets')
        else:
            form = AddTicketForm(instance=feature)
        return render(request, 'add_ticket_feature.html', {'form': form})
    else:
        return redirect('/subscribe/')


@login_required
def edit_ticket(request, ticket_id):
    """
    Create a view that allows users to edit their own tickets
    """
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        form = AddTicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            ticket.save()
            return redirect('tickets')
    else:
        form = AddTicketForm(instance=ticket)
    return render(request, 'edit_ticket.html', {'form': form}, ticket_id)


@login_required
def delete_ticket(request, ticket_id):
    """
    Create a view that allows users to delete their own tickets
    """
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    title = ticket.title
    ticket.delete()
    messages.success(request, "You have successfully deleted your ticket: "
                   + "'" + title + "'")
    return redirect('tickets')


@login_required
def full_ticket(request, ticket_id):
    """
    Create a view that allows users to view an ticket in full page
    """
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    return render(request, 'full_ticket.html', {"ticket": ticket})


@login_required
def add_ticket_comment(request, ticket_id, pk=None):
    """
    Add a comment to a ticket
    """
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    commenter = request.user
    new_comment = get_object_or_404(Comment, pk=pk) if pk else None
    if request.method == 'POST':
        form = AddCommentForm(request.POST, request.FILES,
                              instance=new_comment)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.commenter = commenter
            new_comment.ticket = ticket
            new_comment.save()
            return redirect('tickets')
    else:
        form = AddCommentForm(instance=new_comment)
    return render(request, 'add_ticket_comment.html', {'form': form,
                  'ticket': ticket})


@login_required
def upvote(request, ticket_id):
    """
    Upvote a ticket if not already voted
    """
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    voter = request.user
    try:
        Vote.objects.get(ticket=ticket, voter=voter)
    except Vote.DoesNotExist:
        Vote.objects.create(voter=voter, ticket=ticket)
        ticket.votes += 1
        ticket.save()
        ticket.voters.add(voter)
    return redirect('tickets')
