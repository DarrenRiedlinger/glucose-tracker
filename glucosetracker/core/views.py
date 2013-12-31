from django.shortcuts import HttpResponseRedirect
from django.views.generic import TemplateView, FormView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings

from braces.views import LoginRequiredMixin

from .forms import ContactForm


class HomePageView(TemplateView):
    template_name = 'home.html'


class HelpPageView(LoginRequiredMixin, FormView):
    success_url = '.'
    form_class = ContactForm
    template_name = 'core/help.html'

    def get_initial(self):
        return {
            'email': self.request.user.email
        }

    def form_valid(self, form):
        success_message = '''Email sent! We'll try to get back to you as
            soon as possible.'''
        messages.add_message(self.request, messages.SUCCESS, success_message)

        return super(HelpPageView, self).form_valid(form)

    def form_invalid(self, form):
        failure_message = 'Email not sent. Please try again.'
        messages.add_message(self.request, messages.WARNING, failure_message)

        return super(HelpPageView, self).form_invalid(form)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            support_email = settings.CONTACTS['support_email']

            message = 'Sent By: %s (%s)\n\n%s' % (
                form.cleaned_data['email'],
                self.request.user.username,
                form.cleaned_data['message'])

            email = EmailMessage(
                from_email=support_email,
                subject='[Help] %s ' % form.cleaned_data['subject'],
                body=message,
                to=[support_email])

            email.send()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)