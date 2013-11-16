from django.views.generic import CreateView, ListView, UpdateView, \
    DeleteView, FormView
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse

from braces.views import LoginRequiredMixin
from django_datatables_view.base_datatable_view import BaseDatatableView

from .models import Glucose
from .reports import GlucoseCsvReport
from .forms import GlucoseCreateForm, GlucoseUpdateForm, GlucoseEmailReportForm


class GlucoseEmailReportView(LoginRequiredMixin, FormView):
    success_url = '.'
    template_name = 'glucoses/glucose_email_report.html'
    form_class = GlucoseEmailReportForm

    def get_initial(self):
        return {'recipient': self.request.user.email,
                'message': 'Glucose data for %s.' % self.request.user.username}

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Email sent!')
        return super(GlucoseEmailReportView, self).form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING,
                             'Email not sent. Please try again.')
        return super(GlucoseEmailReportView, self).form_invalid(form)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            report = GlucoseCsvReport(form.cleaned_data['start_date'],
                                      form.cleaned_data['end_date'],
                                      request.user)
            report.email(form.cleaned_data['recipient'],
                         form.cleaned_data['subject'])

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class GlucoseCreateView(LoginRequiredMixin, CreateView):
    model = Glucose
    success_url = '/glucoses/list/'
    template_name = 'glucoses/glucose_create.html'
    form_class = GlucoseCreateForm

    def form_valid(self, form):
        """
        Set the value of the 'user' field to the currently logged-in user.
        """
        form.instance.user = self.request.user
        return super(GlucoseCreateView, self).form_valid(form)


class GlucoseDeleteView(LoginRequiredMixin, DeleteView):
    model = Glucose
    success_url = '/glucoses/list/'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # If the record's user doesn't match the currently logged-in user,
        # deny viewing/updating of the object by showing the 403.html
        # forbidden page. This can occur when the user changes the id in
        # the URL field to a record that the user doesn't own.
        if self.object.user != request.user:
            raise PermissionDenied
        else:
            return super(GlucoseDeleteView, self).get(request, *args, **kwargs)


class GlucoseListJson(LoginRequiredMixin, BaseDatatableView):
    model = Glucose

    columns = ['value', 'category', 'record_date', 'record_time', 'notes']
    order_columns = ['value', 'category', 'record_date', 'record_time', 'notes']
    max_display_length = 500

    def render_column(self, row, column):
        low = 60
        high = 180
        target = range(70, 121)

        if column == 'value':
            if row.value < low or row.value > high:
                return """<center><b><a href="%s"><font color="red">%s
                </font></a></b></center>""" % (
                    reverse('glucose_update', args=(row.id,)), row.value)
            elif row.value in target:
                return """<center><b><a href="%s"><font color="green">%s
                </font></a></b></center>""" % (
                    reverse('glucose_update', args=(row.id,)), row.value)
            else:
                return """<center><b><a href="%s">%s</a></b></center>""" % \
                   (reverse('glucose_update', args=(row.id,)), row.value)
        elif column == 'category':
            return '%s' % row.category.name
        elif column == 'record_date':
            return row.record_date.strftime('%m/%d/%Y')
        elif column == 'record_time':
            return row.record_time.strftime('%I:%M %p')
        else:
            return super(GlucoseListJson, self).render_column(row, column)

    def get_initial_queryset(self):
        """
        Filter records to show only entries from the currently logged-in user.
        """
        return Glucose.objects.by_user(self.request.user)


class GlucoseListView(LoginRequiredMixin, ListView):
    model = Glucose
    template_name = 'glucoses/glucose_list.html'

    def get_queryset(self):
        """
        Filter records to show only entries from the currently logged-in user.
        """
        return Glucose.objects.by_user(self.request.user)


class GlucoseUpdateView(LoginRequiredMixin, UpdateView):
    model = Glucose
    context_object_name = 'glucose'
    success_url = '/glucoses/list/'
    template_name = 'glucoses/glucose_update.html'
    form_class = GlucoseUpdateForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # If the record's user doesn't match the currently logged-in user,
        # deny viewing/updating of the object by showing the 403.html
        # forbidden page. This can occur when the user changes the id in
        # the URL field to a record that the user doesn't own.
        if self.object.user != request.user:
            raise PermissionDenied
        else:
            return super(GlucoseUpdateView, self).get(request, *args, **kwargs)