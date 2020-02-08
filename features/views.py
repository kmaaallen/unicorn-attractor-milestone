from django.shortcuts import render, get_object_or_404, redirect
from .models import Feature, Vote, Comment
from .forms import AddFeatureForm, AddCommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
@login_required
def all_features(request):
    features = Feature.objects.all()
    return render(request, "feature_overview.html", {"features": features})


@login_required
def my_features(request):
    features = Feature.objects.filter(reported_by=request.user)
    return render(request, "feature_overview.html", {"features": features},)


@login_required
def full_feature(request, feature_id):
    """
    Create a view that allows users to view a feature in full page
    """
    feature = get_object_or_404(Feature, pk=feature_id)
    return render(request, 'full_feature.html', {"feature": feature})


@login_required
def request_feature(request, pk=None):
    """
    Create a view that allows users to create or edit a feature request
    """
    feature = get_object_or_404(Feature, pk=pk) if pk else None
    if request.method == 'POST':
        form = AddFeatureForm(request.POST, request.FILES, instance=feature)
        if form.is_valid():
            feature = form.save()
            return redirect('features')
    else:
        form = AddFeatureForm(instance=feature)
    return render(request, 'add_feature.html', {'form': form})


@login_required
def add_comment(request, feature_id, pk=None):
    """
    Add a comment to a feature
    """
    feature = get_object_or_404(Feature, pk=feature_id)
    commenter = request.user
    new_comment = get_object_or_404(Comment, pk=pk) if pk else None
    if request.method == 'POST':
        form = AddCommentForm(request.POST, request.FILES,
                              instance=new_comment)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.commenter = commenter
            new_comment.feature = feature
            new_comment.save()
            return redirect('features')
    else:
        form = AddCommentForm(instance=new_comment)
    return render(request, 'add_feature_comment.html', {'form': form,
                  'feature': feature})


@login_required
def upvote(request, feature_id):
    """
    Upvote a feature if not already voted
    """
    feature = get_object_or_404(Feature, pk=feature_id)
    voter = request.user
    try:
        Vote.objects.get(feature=feature, voter=voter)
        messages.error(request, 'You have already voted on this feature')
    except Vote.DoesNotExist:
        Vote.objects.create(voter=voter, feature=feature)
        feature.votes += 1
        feature.save()
        feature.voters.add(voter)
    return redirect('features')
