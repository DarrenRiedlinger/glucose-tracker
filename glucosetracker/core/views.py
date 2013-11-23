from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, FormView
from django.core.urlresolvers import reverse
from django.contrib import messages

from braces.views import LoginRequiredMixin

from .models import UserSettings
from .forms import UserSettingsForm


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

    # Remove method below when we're ready to go to production.
    def get(self, request, *args, **kwargs):
        """
        Redirect to 'dashboard.'
        """
        return HttpResponseRedirect(reverse('dashboard'))


class UserSettingsView(LoginRequiredMixin, FormView):
    success_url = '.'
    form_class = UserSettingsForm
    template_name = 'core/usersettings.html'

    def get_initial(self):
        user = self.request.user
        settings = user.settings
        
        return {'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'time_zone': settings.user.settings.time_zone,
                'glucose_low': settings.glucose_low,
                'glucose_high': settings.glucose_high,
                'glucose_target_min': settings.glucose_target_min,
                'glucose_target_max': settings.glucose_target_max,}

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Settings saved!')
        return super(UserSettingsView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.full_clean()

        if form.is_valid():
            user = self.request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            user.settings.time_zone = form.cleaned_data['time_zone']
            user.settings.glucose_low = form.cleaned_data['glucose_low']
            user.settings.glucose_high = form.cleaned_data['glucose_high']
            user.settings.glucose_target_min = form.cleaned_data[
                'glucose_target_min']
            user.settings.glucose_target_max = form.cleaned_data[
                'glucose_target_max']
            user.settings.save()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)
