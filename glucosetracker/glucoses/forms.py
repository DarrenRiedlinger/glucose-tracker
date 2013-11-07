from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit

from .models import Glucose


class GlucoseCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GlucoseCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal col-xs-6'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
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

    class Meta:
        model = Glucose
        exclude = ('user',)


class GlucoseUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GlucoseUpdateForm, self).__init__(*args, **kwargs)

        # Set date and time formats to those supported by the
        # bootstrap-datetimepicker widget.
        self.fields['record_date'].widget.format = '%m/%d/%y'
        self.fields['record_time'].widget.format = '%I:%M %p'

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal col-xs-6'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.add_input(Button(
            'cancel', 'Cancel', onclick='location.href="%s";' % \
                                        reverse('glucose_list')))

        delete_url = reverse('glucose_delete', args=(self.instance.id,))
        self.helper.add_input(Button('delete', 'Delete',
                                     onclick='location.href="%s";' % delete_url,
                                     css_class='btn-danger pull-right'))

        # Remove the blank option from the select widget.
        self.fields['category'].empty_label = None

        # Specify which time formats are valid for this field. This setting is
        # necessary when using the bootstrap-datetimepicker widget as it
        # doesn't allow inputting of seconds.
        valid_time_formats = ['%H:%M', '%I:%M%p', '%I:%M %p']
        self.fields['record_time'].input_formats = valid_time_formats

    class Meta:
        model = Glucose
        exclude = ('user',)