from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from bootstrap3_datetime.widgets import DateTimePicker

from .models import Glucose


class GlucoseCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal col-xs-6'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.add_input(Button(
            'cancel', 'Cancel', onclick='location.href="%s";' % \
                                        reverse('glucose_list')))

        super(GlucoseCreateForm, self).__init__(*args, **kwargs)

        # Remove the blank option from the select widget.
        self.fields['category'].empty_label = None

    class Meta:
        model = Glucose
        exclude = ('user',)


class GlucoseUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-xs-6'
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.add_input(Button(
            'cancel', 'Cancel', onclick='location.href="%s";' % \
                                        reverse('glucose_list')))
        self.helper.add_input(Button(
            'delete', 'Delete', css_class='btn-danger pull-right'))

        super(GlucoseUpdateForm, self).__init__(*args, **kwargs)

        # Remove the blank option from the select widget.
        self.fields['category'].empty_label = None

    class Meta:
        model = Glucose
        exclude = ('user',)