from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Button, Submit, Fieldset, HTML, Field
from crispy_forms.bootstrap import FormActions
from timezone_field import TimeZoneFormField

from .validators import validate_email_unique, validate_username_unique


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=30,
                               validators=[validate_username_unique])
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())
    email = forms.EmailField(max_length=75, validators=[validate_email_unique])
    time_zone = TimeZoneFormField(label='Time Zone')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal col-xs-12 col-md-6 col-lg-5'
        self.helper.label_class = 'col-xs-3 col-md-3 col-lg-3'
        self.helper.field_class = 'col-xs-9 col-md-9 col-lg-9'
        self.helper.help_text_inline = False

        self. helper.layout = Layout(
            Fieldset(
                'Setup Your Account',
                Field('username', autofocus=True),
                Field('password'),
                Field('email', placeholder='e.g. john@gmail.com'),
                Field('time_zone'),
            ),
            FormActions(
                Submit('submit', 'Create My Account'),
            ),
        )


class UserSettingsForm(forms.Form):
    """
    Form to allow users to change profile settings and preferences.
    """
    username = forms.CharField(required=False)
    first_name = forms.CharField(label='First Name', required=False)
    last_name = forms.CharField(label='Last Name', required=False)
    email = forms.EmailField(
        label='Email',
        required=False,
        help_text='Please <a href="%s">contact us</a> if you need to change '
                  'your email address.' % '/core/help/',
    )
    time_zone = TimeZoneFormField(label='Time Zone')

    glucose_low = forms.IntegerField(
        label='Low', min_value=0, max_value=3000,
        help_text="Below this value is a low blood glucose."
    )
    glucose_high = forms.IntegerField(
        label='High', min_value=0, max_value=3000,
        help_text="Above this value is a high blood glucose."
    )
    glucose_target_min = forms.IntegerField(
        label='Target Min', min_value=0, max_value=3000,
        help_text="Your target range's minimum value."
    )
    glucose_target_max = forms.IntegerField(
        label='Target Max', min_value=0, max_value=3000,
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
                Field('username', readonly=True),
                Field('email', readonly=True),
                Field('first_name'),
                Field('last_name'),
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