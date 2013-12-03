from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Button, ButtonHolder, Submit, MultiField, \
    Fieldset, Div, HTML, Field
from crispy_forms.bootstrap import FormActions, StrictButton, InlineField
from timezone_field import TimeZoneFormField


class UserSettingsForm(forms.Form):
    """
    Form to allow users to change profile settings and preferences.
    """
    first_name = forms.CharField(label='First Name',required=False)
    last_name = forms.CharField(label='Last Name', required=False)
    email = forms.CharField(label='Email')
    time_zone = TimeZoneFormField(label='Time Zone')

    glucose_low = forms.IntegerField(
        label='Low', min_value=0, required=False,
        help_text="Below this value is a low blood glucose."
    )
    glucose_high = forms.IntegerField(
        label='High', min_value=0, required=False,
        help_text="Above this value is a high blood glucose."
    )
    glucose_target_min = forms.IntegerField(
        label='Target Min', min_value=0, required=False,
        help_text="Your target range's minimum value."
    )
    glucose_target_max = forms.IntegerField(
        label='Target Max', min_value=0, required=False,
        help_text="Your target range's maximum value."
    )

    def __init__(self, *args, **kwargs):
        super(UserSettingsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal col-xs-12 col-md-6 col-lg-5'
        self.helper.label_class = 'col-xs-3 col-md-3 col-lg-3'
        self.helper.field_class = 'col-xs-9 col-md-9 col-lg-9'
        self.helper.help_text_inline = False

        self. helper.layout = Layout(
            Fieldset(
                'Profile',
                Field('first_name', css_class='col-xs-4'),
                Field('last_name'),
                Field('email'),
                Field('time_zone'),
            ),
            Fieldset(
                'Glucose Levels (mg/dL)',
                Field('glucose_low'),
                Field('glucose_high'),
                Field('glucose_target_min'),
                Field('glucose_target_max'),
            ),
            FormActions(
                Submit('submit', 'Save'),
                Button('cancel', 'Cancel',
                       onclick='location.href="%s";' \
                       % reverse('dashboard')),
            ),
        )