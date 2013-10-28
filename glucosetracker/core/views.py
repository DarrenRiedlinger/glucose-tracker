from django.shortcuts import render


def home(request):
    """ The home page. """
    return render(request, 'base/home.html')