import itertools
from datetime import date, timedelta

from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Button, Submit, MultiField, Div, HTML, \
    Field, Fieldset, Reset
from crispy_forms.bootstrap import FormActions

from .models import Glucose, Category
from .fields import RestrictedFileField


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

    def __init__(self, user, *args, **kwargs):
        super(GlucoseFilterForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'filter_form'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'

        self.fields['tags'] = forms.ChoiceField(
            choices=self.get_tags(Glucose.objects.filter(user=user).exclude(
                tags__name__isnull=True)),
            required=False)

        self. helper.layout = Layout(
            'quick_date_select',
            Field('start_date', placeholder='From (mm/dd/yyyy)'),
            Field('end_date', placeholder='To (mm/dd/yyyy)'),
            'category',
            Field('start_value', placeholder='From', step='any'),
            Field('end_value', placeholder='To', step='any'),
            'notes',
            Field('tags'),
            FormActions(
                Submit('submit', 'Filter'),
                Reset('reset', 'Reset'),
            ),
        )

    def get_tags(self, queryset):
        """
        Iterate through the queryset and get the unique tag names.
        """
        tag_list = list(itertools.chain.from_iterable(
            [i.tags.names() for i in queryset]))

        empty_label = [('', '---------')]
        # The tag_list here is converted to a set to create a unique
        # collection.
        choices = empty_label + [
            (tag, tag) for tag in sorted(list(set(tag_list)))]

        return choices


class GlucoseQuickAddForm(forms.ModelForm):
    """
    A simple form for adding glucose values. Date and time are automatically
    set to the user's current local date and time using Javascript (see
    dashboard.html template).
    """
    def __init__(self, *args, **kwargs):
        super(GlucoseQuickAddForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'quick_add_form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-inline'
        self.helper.form_show_labels = False

        # Remove the blank option from the select widget.
        self.fields['category'].empty_label = None

        self.helper.layout = Layout(
            HTML('''
            <div id="div_id_value" class="form-group"> <div class="controls">
            <input autofocus="True" class="numberinput form-control"
            id="id_value" name="value"
            placeholder="Value ({{ user.settings.glucose_unit.name }})"
            required="True" type="number" step="any" min="0"/></div></div>
            '''),
            Field('category'),
            Field('record_date', type='hidden'),
            Field('record_time', type='hidden'),
            Submit('submit', 'Quick Add'),
        )

    class Meta:
        model = Glucose
        exclude = ('user', 'notes')


class GlucoseEmailReportForm(forms.Form):
    report_format = forms.ChoiceField(
        label='Format',
        choices=(
            ('csv', 'CSV'),
            ('pdf', 'PDF'),
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
        self.helper.label_class = 'col-sm-3 col-md-3'
        self.helper.field_class = 'col-sm-9 col-md-9'

        self. helper.layout = Layout(
            MultiField(
                None,
                Div(
                    HTML('''
                    {% if messages %}
                    {% for message in messages %}
                    <p {% if message.tags %}
                    class="alert alert-{{ message.tags }}"
                    {% endif %}>{{ message }}</p>{% endfor %}{% endif %}
                    '''),
                    Div(
                        'report_format',
                        Field('start_date', required=True),
                        Field('end_date', required=True),
                        css_class='well col-sm-4 col-md-4',
                    ),
                    Div('subject',
                        Field('recipient', placeholder='Email address',
                              required=True, autofocus=True),
                        'message',
                        FormActions(
                            Submit('submit', 'Send'),
                            css_class='pull-right'
                        ),
                        css_class='col-sm-8 col-md-8',
                    ),
                    css_class='row'
                ),
            ),
        )

        # Initial values.
        now = date.today()
        last_90_days = now - timedelta(days=90)
        self.fields['start_date'].initial = last_90_days.strftime(DATE_FORMAT)
        self.fields['end_date'].initial = now.strftime(DATE_FORMAT)

        self.fields['report_format'].initial = 'pdf'
        self.fields['subject'].initial = '[GlucoseTracker] Glucose Data Report'


class GlucoseInputForm(forms.ModelForm):
    # This is a hidden field that holds the submit type value. Used to
    # determine whether the user clicked 'Save' or 'Save & Add Another' in
    # the Glucose Create Form.
    submit_button_type = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(GlucoseInputForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal col-xs-12 col-md-6 col-lg-5'
        self.helper.label_class = 'col-xs-3 col-md-2 col-lg-2'
        self.helper.field_class = 'col-xs-9 col-md-10 col-lg-10'
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.add_input(Button(
            'cancel', 'Cancel', onclick='location.href="%s";' % \
                                        reverse('dashboard')))

        # Remove the blank option from the select widget.
        self.fields['category'].empty_label = None
        self.fields['category'].required = False

        # Specify which time formats are valid for this field. This setting is
        # necessary when using the bootstrap-datetimepicker widget as it
        # doesn't allow inputting of seconds.
        valid_time_formats = ['%H:%M', '%I:%M%p', '%I:%M %p']
        self.fields['record_time'].input_formats = valid_time_formats

        self. helper.layout = Layout(
            HTML(
                '''
                {% if messages %}
                {% for message in messages %}
                <p {% if message.tags %}
                class="alert alert-{{ message.tags }}"
                {% endif %}>{{ message }}</p>{% endfor %}{% endif %}
                '''
            ),
            Field('value', placeholder='Value', required=True, autofocus=True,
                  min=0, step='any'),
            'category',
            'record_date',
            'record_time',
            'notes',
            Field('tags', placeholder='e.g. fasting, sick, "after meal"'),
            Field('submit_button_type', type='hidden')
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

        # Make record date and time not required. If these fields are empty
        # the current date and time will be used.
        self.fields['record_date'].required = False
        self.fields['record_time'].required = False

        self.helper.add_input(Submit('submit_and_add', 'Save & Add Another',
                                     css_class='pull-right'))


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


class GlucoseImportForm(forms.Form):
    # File size limited to 2MB
    file = RestrictedFileField(
        label='CSV File (Max Size 2MB)',
        content_types=['text/csv'],
        max_upload_size=2097152,
    )

    def __init__(self, *args, **kwargs):
        super(GlucoseImportForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self. helper.layout = Layout(
            MultiField(
                None,
                Fieldset(
                    'Instructions',
                    HTML(
                        '''
                        To properly import your data, the CSV file must follow
                        this order and format: <br><br>
                        <ol>
                        <li>Value</li>
                        <li>Category (if no matching category in our system,
                        'No Category' will be assigned)</li>
                        <li>Date (in m/d/yyyy format, e.g. 5/6/2014 or
                        05/06/2014)</li>
                        <li> Time (in h:m am/pm format, e.g. 8:01 AM or
                        08:01 PM)</li>
                        <li>Notes</li>
                        </ol>
                        <p>You can also download this template as a guide:
                        <a href="{{ STATIC_URL }}samples/csv_import_template.csv">
                        csv_import_template.csv</a></p>
                        <br>
                        '''
                    ),
                ),
                HTML(
                    '''
                    {% if messages %}
                    {% for message in messages %}
                    <p {% if message.tags %}
                    class="alert alert-{{ message.tags }}"
                    {% endif %}>{{ message }}</p>{% endfor %}{% endif %}
                    '''
                ),
                Div(
                    'file',
                    FormActions(
                        Submit('submit', 'Import'),
                        css_class='pull-right',
                    ),
                    css_class='well col-xs-8 col-sm-8 col-md-8',
                ),
            ),
        )