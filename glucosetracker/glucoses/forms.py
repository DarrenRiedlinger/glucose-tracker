from datetime import datetime, date, timedelta

from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Button, Submit, MultiField, Fieldset, Div, \
    HTML, Field, Reset
from crispy_forms.bootstrap import FormActions, StrictButton, InlineField

from .models import Glucose, Category


DATE_FORMAT = '%m/%d/%Y'
TIME_FORMAT = '%I:%M %p'


class GlucoseFilterForm(forms.Form):
    quick_date_select = forms.ChoiceField(
        label='Quick Date Select',
        choices=(
            (7, 'Last 7 Days'),
            (30, 'Last 30 Days'),
            (60, 'Last 60 Days'),
            (90, 'Last 90 Days'),
        ),
        required=False,
    )
    start_date = forms.DateField(
        label='Date Range', required=False, input_formats=[DATE_FORMAT])
    end_date = forms.DateField(
        label='', required=False, input_formats=[DATE_FORMAT])

    start_value = forms.IntegerField(
        label='Value Range', required=False, min_value=0)
    end_value = forms.IntegerField(label='', required=False, min_value=0)

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), required=False)

    notes = forms.CharField(label='Notes Contains', required=False,
                            widget=forms.Textarea(attrs={'rows': 2}))

    tags = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(GlucoseFilterForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '.'

        self. helper.layout = Layout(
            'quick_date_select',
            Field('start_date', placeholder='From (mm/dd/yyyy)'),
            Field('end_date', placeholder='To (mm/dd/yyyy)'),
            'category',
            Field('start_value', placeholder='From'),
            Field('end_value', placeholder='To'),
            'notes',
            Field('tags', placeholder='e.g. exercise, sick, medication'),
            FormActions(
                Submit('submit', 'Filter'),
                Reset('reset', 'Reset'),
                Button('cancel', 'Cancel', onclick='location.href="%s";' \
                       % reverse('dashboard'), css_class='pull-right'),
            ),
        )


class GlucoseQuickAddForm(forms.ModelForm):
    """
    A simple form for adding glucose values. Date and time are automatically
    set to the user's current local date and time using Javascript (see
    glucose_list.html template).
    """

    def __init__(self, *args, **kwargs):
        super(GlucoseQuickAddForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'quick_add_form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'glucose_create'
        self.helper.form_class = 'form-inline'
        self.helper.form_show_labels = False

        # Remove the blank option from the select widget.
        self.fields['category'].empty_label = None

        self.helper.layout = Layout(
            InlineField('value', required=True, autofocus=True),
            InlineField('category'),
            Field('record_date', type='hidden'),
            Field('record_time', type='hidden'),
            StrictButton('Quick Add', css_class='btn-primary',
                         type='submit', action='submit'),
        )

    class Meta:
        model = Glucose
        exclude = ('user', 'notes')


class GlucoseEmailReportForm(forms.Form):
    report_format = forms.ChoiceField(
        label='Format',
        choices=(
            ('csv', 'CSV'),
            #('html', 'HTML'),
        )
    )
    start_date = forms.DateField(label='From')
    end_date = forms.DateField(label='To')
    subject = forms.CharField(required=False)
    recipient = forms.EmailField(label='Send To')
    message = forms.CharField(widget=forms.Textarea(attrs={'cols':50}),
                              required=False)

    def __init__(self, *args, **kwargs):
        super(GlucoseEmailReportForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'

        self. helper.layout = Layout(
            MultiField(
                None,
                HTML("""
                {% if messages %}
                {% for message in messages %}
                <p {% if message.tags %} class="text-{{ message.tags }}"\
                {% endif %}>{{ message }}</p>{% endfor %}{% endif %}
                """),
                Div('report_format',
                    Field('start_date', required=True),
                    Field('end_date', required=True),
                    css_class='well row col-md-4',
                ),
                Div('subject',
                    Field('recipient', placeholder='Email address',
                          required=True, autofocus=True),
                    'message',
                    FormActions(
                        Submit('submit', 'Send'),
                        Button('cancel', 'Cancel',
                               onclick='location.href="%s";' \
                               % reverse('dashboard')),
                        css_class='pull-right'
                    ),
                    css_class='row col-md-7',
                ),
            ),
        )

        # Initial values.
        now = date.today()
        last_90_days = now - timedelta(days=90)
        self.fields['start_date'].initial = last_90_days.strftime(DATE_FORMAT)
        self.fields['end_date'].initial = now.strftime(DATE_FORMAT)

        self.fields['subject'].initial = '[GlucoseTracker] Glucose Data Report'


class GlucoseInputForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GlucoseInputForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal col-xs-12 col-md-6 col-lg-5'
        self.helper.label_class = 'col-xs-2 col-md-2 col-lg-2'
        self.helper.field_class = 'col-xs-10 col-md-10 col-lg-10'
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.add_input(Button(
            'cancel', 'Cancel', onclick='location.href="%s";' % \
                                        reverse('glucose_list')))


        # Remove the blank option from the select widget.
        self.fields['category'].empty_label = None

        # Specify which time formats are valid for this field. This setting is
        # necessary when using the bootstrap-datetimepicker widget as it
        # doesn't allow inputting of seconds.
        valid_time_formats = ['%H:%M', '%I:%M%p', '%I:%M %p']
        self.fields['record_time'].input_formats = valid_time_formats

        self. helper.layout = Layout(
            Field('value', placeholder='Value in mg/dL', required=True,
                  autofocus=True),
            'category',
            'record_date',
            'record_time',
            'notes',
            Field('tags', placeholder='e.g. exercise, sick, medication'),
        )

    class Meta:
        model = Glucose
        exclude = ('user',)
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }


class GlucoseCreateForm(GlucoseInputForm):

    def __init__(self, *args, **kwargs):
        super(GlucoseCreateForm, self).__init__(*args, **kwargs)

        self.fields['category'].required = False

        # Make record date and time not required. If these fields are empty
        # the current date and time will be used.
        self.fields['record_date'].required = False
        self.fields['record_time'].required = False


class GlucoseUpdateForm(GlucoseInputForm):

    def __init__(self, *args, **kwargs):
        super(GlucoseUpdateForm, self).__init__(*args, **kwargs)

        # Set date and time formats to those supported by the
        # bootstrap-datetimepicker widget.
        self.fields['record_date'].widget.format = DATE_FORMAT
        self.fields['record_time'].widget.format = TIME_FORMAT

        delete_url = reverse('glucose_delete', args=(self.instance.id,))
        self.helper.add_input(Button('delete', 'Delete',
                                     onclick='location.href="%s";' % delete_url,
                                     css_class='btn-danger pull-right'))