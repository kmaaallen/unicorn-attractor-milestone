from django.shortcuts import render, get_object_or_404, redirect
from .models import Issue
from .forms import AddIssueForm


# Create your views here.
def all_issues(request):
    issues = Issue.objects.all()
    return render(request, "issue_overview.html", {"issues": issues})


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
