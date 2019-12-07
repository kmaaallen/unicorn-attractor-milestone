from django.shortcuts import render

# Create your views here.


def landing_page(request):
    """
    A view that displays the landing page
    """
    return render(request, 'index.html')


def find_out_more(request):
    """
    A view that displays the find out more page
    """
    return render(request, 'more.html')
    