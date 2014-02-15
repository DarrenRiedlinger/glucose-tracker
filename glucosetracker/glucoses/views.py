import json
from datetime import datetime, timedelta

from django.views.generic import CreateView, UpdateView, DeleteView, \
    FormView, TemplateView
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext

from braces.views import LoginRequiredMixin
from django_datatables_view.base_datatable_view import BaseDatatableView

from core.utils import glucose_by_unit_setting, to_mg

from . import utils
from .models import Glucose
from .reports import GlucoseCsvReport, GlucosePdfReport, ChartData, UserStats
from .forms import GlucoseCreateForm, GlucoseUpdateForm, GlucoseQuickAddForm, \
    GlucoseEmailReportForm, GlucoseFilterForm


DATE_FORMAT = '%m/%d/%Y'
TIME_FORMAT = '%I:%M %p'


@login_required
def filter_view(request):
    """
    Displays the glucose data table for the currently logged in user with
    filter options.

    The data is loaded by the GlucoseListJson view and rendered by the
    Datatables plugin via Javascript.
    """
    form = GlucoseFilterForm(request.user)
    form.fields['start_date'].initial = (datetime.now(
        tz=request.user.settings.time_zone) - timedelta(days=7))\
        .date().strftime(DATE_FORMAT)
    form.fields['end_date'].initial = datetime.now(
        tz=request.user.settings.time_zone).date().strftime(DATE_FORMAT)

    data = reverse('glucose_list_json')

    if request.method == 'POST' and request.is_ajax:
        # We need to create a copy of request.POST because it's immutable and
        # we need to convert the content of the Value field to mg/dL if the
        # user's glucose unit setting is set to mmol/L.
        params = request.POST.copy()
        if request.user.settings.glucose_unit.name == 'mmol/L':
            # Only do the conversion if the values are not None or empty.
            if params['start_value']:
                params['start_value'] = to_mg(params['start_value'])
            if params['end_value']:
                params['end_value'] = to_mg(params['end_value'])

        # Create the URL query string and strip the last '&' at the end.
        data = ('%s?%s' % (reverse('glucose_list_json'), ''.join(
            ['%s=%s&' % (k, v) for k, v in params.iteritems()])))\
            .rstrip('&')

        return HttpResponse(json.dumps(data), content_type='application/json')

    return render_to_response(
        'glucoses/glucose_filter.html',
        {'form': form, 'data': data},
        context_instance=RequestContext(request),
    )


@login_required
def dashboard(request):
    """
    Displays the glucose data table for the currently logged in user. A form
    for quickly adding glucose values is also included.

    The data is loaded by the GlucoseListJson view and rendered by the
    Datatables plugin via Javascript.
    """
    form = GlucoseQuickAddForm()
    form.fields['category'].initial = utils.get_initial_category(request.user)

    return render_to_response(
        'core/dashboard.html',
        {'form': form,
         'glucose_unit_name': request.user.settings.glucose_unit.name},
        context_instance=RequestContext(request),
    )


@login_required
def chart_data_json(request):
    data = {}
    params = request.GET

    days = params.get('days', 0)
    name = params.get('name', '')
    if name == 'avg_by_category':
        data['chart_data'] = ChartData.get_avg_by_category(
            user=request.user, days=int(days))
    elif name == 'avg_by_day':
        data['chart_data'] = ChartData.get_avg_by_day(
            user=request.user, days=int(days))
    elif name == 'level_breakdown':
        data['chart_data'] = ChartData.get_level_breakdown(
            user=request.user, days=int(days))
    elif name == 'count_by_category':
        data['chart_data'] = ChartData.get_count_by_category(
            user=request.user, days=int(days))

    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def stats_json(request):
    data = {'stats': UserStats(request.user).user_stats}

    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def quick_add(request):
    if request.method == 'POST' and request.is_ajax:
        # We need to create a copy of request.POST because it's immutable and
        # we need to convert the content of the Value field to mg/dL if the
        # user's glucose unit setting is set to mmol/L.
        post_values = request.POST.copy()
        if request.user.settings.glucose_unit.name == 'mmol/L':
            post_values['value'] = to_mg(post_values['value'])

        form = GlucoseCreateForm(post_values)
        if form.is_valid():
            user = request.user

            obj = form.save(commit=False)
            obj.user = user

            obj.record_date = datetime.now(tz=user.settings.time_zone).date()
            obj.record_time = datetime.now(tz=user.settings.time_zone).time()
            obj.save()

            message = {'success': True}

            return HttpResponse(json.dumps(message))
        else:
            message = {
                'success': False,
                'error': 'Invalid value.'
            }

            return HttpResponse(json.dumps(message))

    raise PermissionDenied


class GlucoseChartsView(LoginRequiredMixin, TemplateView):
    template_name = 'glucoses/glucose_charts.html'


class GlucoseEmailReportView(LoginRequiredMixin, FormView):
    """
    Sends out an email containing the glucose data report.
    """
    success_url = '.'
    form_class = GlucoseEmailReportForm
    template_name = 'glucoses/glucose_email_report.html'

    def get_initial(self):
        return {'recipient': self.request.user.email,
                'message': 'Glucose data for %s.' % self.request.user}

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Email Sent!')
        return super(GlucoseEmailReportView, self).form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING,
                             'Email not sent. Please try again.')
        return super(GlucoseEmailReportView, self).form_invalid(form)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            if form.cleaned_data['report_format'] == 'pdf':
                report = GlucosePdfReport(form.cleaned_data['start_date'],
                                          form.cleaned_data['end_date'],
                                          request.user)
            else:
                report = GlucoseCsvReport(form.cleaned_data['start_date'],
                                          form.cleaned_data['end_date'],
                                          request.user)

            report.email(form.cleaned_data['recipient'],
                         form.cleaned_data['subject'],
                         form.cleaned_data['message'])

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class GlucoseCreateView(LoginRequiredMixin, CreateView):
    model = Glucose
    success_url = '/dashboard/'
    template_name = 'glucoses/glucose_create.html'
    form_class = GlucoseCreateForm

    def get_initial(self):
        time_zone = self.request.user.settings.time_zone
        record_date = datetime.now(tz=time_zone).date().strftime(DATE_FORMAT)
        record_time = datetime.now(tz=time_zone).time().strftime(TIME_FORMAT)

        return {
            'category': utils.get_initial_category(self.request.user),
            'record_date': record_date,
            'record_time': record_time,
        }


    def form_valid(self, form):
        # If the 'Save & Add Another' button is clicked, the submit_button_type
        # field will be set to 'submit_and_add' by Javascript. We'll change
        # the success URL to go back to the Add Glucose page and display a
        # successful message in this case.
        if form.cleaned_data['submit_button_type'] == 'submit_and_add':
            self.success_url = '/glucoses/add/'
            value = form.cleaned_data['value']
            messages.add_message(self.request, messages.SUCCESS,
                                 "Glucose '%s' successfully added. You may "
                                 "add another." % value)

        # Set the value of the 'user' field to the currently logged-in user.
        form.instance.user = self.request.user

        # Set the values of the record date and time to the current date and
        # time factoring in the user's timezone setting if they're not
        # specified.
        if not form.instance.record_date:
            form.instance.record_date = datetime.now(
                tz=self.request.user.settings.time_zone).date()

        if not form.instance.record_time:
            form.instance.record_time = datetime.now(
                tz=self.request.user.settings.time_zone).time()

        return super(GlucoseCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        # We need to create a copy of request.POST because it's immutable and
        # we need to convert the content of the Value field to mg/dL if the
        # user's glucose unit setting is set to mmol/L.
        request.POST = request.POST.copy()
        if request.user.settings.glucose_unit.name == 'mmol/L':
            request.POST['value'] = to_mg(request.POST['value'])

        return super(GlucoseCreateView, self).post(request, *args, **kwargs)


class GlucoseUpdateView(LoginRequiredMixin, UpdateView):
    model = Glucose
    context_object_name = 'glucose'
    success_url = '/dashboard/'
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

    def get_object(self, queryset=None):
        obj = Glucose.objects.get(pk=self.kwargs['pk'])

        # Convert the value based on user's glucose unit setting.
        obj.value = glucose_by_unit_setting(self.request.user, obj.value)

        return obj

    def post(self, request, *args, **kwargs):
        # We need to create a copy of request.POST because it's immutable and
        # we need to convert the content of the Value field to mg/dL if the
        # user's glucose unit setting is set to mmol/L.
        request.POST = request.POST.copy()
        if request.user.settings.glucose_unit.name == 'mmol/L':
            request.POST['value'] = to_mg(request.POST['value'])

        return super(GlucoseUpdateView, self).post(request, *args, **kwargs)


class GlucoseDeleteView(LoginRequiredMixin, DeleteView):
    model = Glucose
    success_url = '/dashboard/'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # If the record's user doesn't match the currently logged-in user,
        # deny viewing/updating of the object by showing the 403.html
        # forbidden page. This can occur when the user changes the id in
        # the URL field to a record that the user doesn't own.
        if self.object.user != request.user:
            raise PermissionDenied
        else:
            # Convert the value based on user's glucose unit setting.
            self.object.value = glucose_by_unit_setting(request.user,
                                                        self.object.value)
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)


class GlucoseListJson(LoginRequiredMixin, BaseDatatableView):
    model = Glucose

    columns = ['value', 'category', 'record_date', 'record_time',
               'notes', 'actions']
    order_columns = ['value', 'category', 'record_date', 'record_time', 'notes']
    max_display_length = 500

    def render_column(self, row, column):
        user = self.request.user
        user_settings = user.settings
        low = user_settings.glucose_low
        high = user_settings.glucose_high
        target_min = user_settings.glucose_target_min
        target_max = user_settings.glucose_target_max

        if column == 'value':
            value_by_unit_setting = glucose_by_unit_setting(user, row.value)
            edit_url = reverse('glucose_update', args=(row.id,))
            if row.value < low or row.value > high:
                return self.get_value_cell_style(edit_url, value_by_unit_setting,
                                                 'red')
            elif row.value >= target_min and row.value <= target_max:
                return self.get_value_cell_style(edit_url, value_by_unit_setting,
                                                 'green')
            else:
                return self.get_value_cell_style(edit_url, value_by_unit_setting)
        elif column == 'category':
            return '%s' % row.category.name
        elif column == 'record_date':
            return row.record_date.strftime('%m/%d/%Y')
        elif column == 'record_time':
            return row.record_time.strftime('%I:%M %p')
        elif column == 'actions':
            edit_link = """<a href="%s">
                <img src="/static/images/icons/icon_changelink.gif"></a>""" % \
                reverse('glucose_update', args=(row.id,))
            delete_link = """<a href="%s">
                <img src="/static/images/icons/icon_deletelink.gif"></a>""" % \
                reverse('glucose_delete', args=(row.id,))
            return '<center>%s&nbsp;%s</center>' % (edit_link, delete_link)
        else:
            return super(GlucoseListJson, self).render_column(row, column)

    def get_value_cell_style(self, url, value, color=None):
        style = '''<center><a href="%s">%s</a></center>''' % (url, value)
        if color:
            style = '''<center><a href="%s"><font color="%s">%s</font></a>
                </center>''' % (url, color, value)

        return style

    def get_initial_queryset(self):
        """
        Filter records to show only entries from the currently logged-in user.
        """
        return Glucose.objects.by_user(self.request.user)

    def filter_queryset(self, qs):
        params = self.request.GET

        start_date = params.get('start_date', '')
        if start_date:
            qs = qs.filter(record_date__gte=datetime.strptime(
                start_date, DATE_FORMAT))
            
        end_date = params.get('end_date', '')
        if end_date:
            qs = qs.filter(record_date__lte=datetime.strptime(
                end_date, DATE_FORMAT))

        start_value = params.get('start_value', '')
        if start_value:
            qs = qs.filter(value__gte=start_value)
            
        end_value = params.get('end_value', '')
        if end_value:
            qs = qs.filter(value__lte=end_value)

        category = params.get('category', '')
        if category:
            qs = qs.filter(category=category)

        notes = params.get('notes', '')
        if notes:
            qs = qs.filter(notes__contains=notes)

        tags = params.get('tags', '')
        if tags:
            qs = qs.filter(tags__name=tags)

        return qs