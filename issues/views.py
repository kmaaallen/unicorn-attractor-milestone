from django.shortcuts import render, get_object_or_404, redirect
from .models import Issue, Vote
from .forms import AddIssueForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def all_issues(request):
    issues = Issue.objects.all()
    return render(request, "issue_overview.html", {"issues": issues})


@login_required
def report_issue(request, pk=None):
    """
    Create a view that allows users to report or edit an issue
    """
    issue = get_object_or_404(Issue, pk=pk) if pk else None
    if request.method == 'POST':
        form = AddIssueForm(request.POST, request.FILES, instance=issue)
        if form.is_valid():
            issue = form.save()
            return redirect('issues')
    else:
        form = AddIssueForm(instance=issue)
    return render(request, 'add_issue.html', {'form': form})


@login_required
def full_issue(request, issue_id):
    """
    Create a view that allows users to view an issue in full page
    """
    issue = get_object_or_404(Issue, pk=issue_id)
    return render(request, 'full_issue.html', {"issue": issue})


@login_required
def upvote(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    voter = request.user
    try:
        Vote.objects.get(issue=issue, voter=voter)
        messages.error(request, 'You have already voted on this issue')
    except Vote.DoesNotExist:
        Vote.objects.create(voter=voter, issue=issue)
        issue.votes += 1
        issue.save()
    return redirect('issues')

