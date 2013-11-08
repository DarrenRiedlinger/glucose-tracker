from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView


def login_view(request):
    # Force logout.
    logout(request)
    username = password = ''

    # Flag to keep track whether the login was invalid.
    login_failed = False

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
        else:
            login_failed = True

    return render_to_response('registration/login.html',
                              {'login_failed': login_failed},
                              context_instance=RequestContext(request))


class HomePageView(TemplateView):
    template_name = 'home.html'