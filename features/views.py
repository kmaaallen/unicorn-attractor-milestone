from django.shortcuts import render, get_object_or_404, redirect
from .models import Feature
from .forms import AddFeatureForm


# Create your views here.
def all_features(request):
    features = Feature.objects.all()
    return render(request, "feature_overview.html", {"features": features})


def request_feature(request, pk=None):
    """
    Create a view that allows users to create or edit a feature request
    """
    feature = get_object_or_404(Feature, pk=pk) if pk else None
    if request.method == 'POST':
        form = AddFeatureForm(request.POST, request.FILES, instance=feature)
        if form.is_valid():
            issue = form.save()
            return redirect('features')
    else:
        form = AddFeatureForm(instance=feature)
    return render(request, 'add_feature.html', {'form': form})
