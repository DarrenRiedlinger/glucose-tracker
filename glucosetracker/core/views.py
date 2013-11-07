from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout

from django.views.generic import TemplateView


def login_user(request):
    logout(request)
    username = password = ''

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
    return render_to_response('registration/login.html', context_instance=RequestContext(request))


class HomePageView(TemplateView):
    template_name = 'home.html'