from django import forms
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Button, Submit, Fieldset, HTML, Field
from crispy_forms.bootstrap import FormActions
from timezone_field import TimeZoneFormField

from glucoses.models import Category, Unit

from .validators import validate_email_unique, validate_username_unique


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=30,
                               validators=[validate_username_unique])
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())
    email = forms.EmailField(max_length=75, validators=[validate_email_unique])
    glucose_unit = forms.ModelChoiceField(Unit.objects.all(), empty_label=None,
                                          label='Glucose Unit')
    time_zone = TimeZoneFormField(label='Time Zone')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal col-xs-12 col-md-6 col-lg-5'
        self.helper.label_class = 'col-xs-4 col-md-4 col-lg-4'
        self.helper.field_class = 'col-xs-8 col-md-8 col-lg-8'

        self. helper.layout = Layout(
            Fieldset(
                'Create Your Account',
                Field('username', autofocus=True),
                Field('password'),
                Field('email', placeholder='e.g. willywonka@gmail.com'),
                Field('glucose_unit'),
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
    email = forms.EmailField(label='Email', required=False)
    time_zone = TimeZoneFormField(label='Time Zone')

    glucose_unit = forms.ModelChoiceField(
        Unit.objects.all(), label='Glucose Unit', empty_label=None)
    default_category = forms.ModelChoiceField(
        Category.objects.all(), label='Default Category',
        empty_label='Auto', required=False)

    glucose_low = forms.DecimalField(
        label='Low', max_digits=6, max_value=3000, min_value=0,
        help_text="Below this value is a low blood glucose."
    )
    glucose_high = forms.DecimalField(
        label='High', max_digits=6, max_value=3000, min_value=0,
        help_text="Above this value is a high blood glucose."
    )
    glucose_target_min = forms.DecimalField(
        label='Target Min', max_digits=6, max_value=3000, min_value=0,
        help_text="Your target range's minimum value."
    )
    glucose_target_max = forms.DecimalField(
        label='Target Max', max_digits=6, max_value=3000, min_value=0,
        help_text="Your target range's maximum value."
    )

    def __init__(self, *args, **kwargs):
        super(UserSettingsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal col-xs-12 col-md-6 col-lg-6'
        self.helper.label_class = 'col-xs-4 col-md-4 col-lg-4'
        self.helper.field_class = 'col-xs-8 col-md-8 col-lg-8'
        self.helper.help_text_inline = False

        self. helper.layout = Layout(
            HTML('''
            {% if messages %}
            {% for message in messages %}
            <p {% if message.tags %} class="alert alert-{{ message.tags }}"\
            {% endif %}>{{ message }}</p>{% endfor %}{% endif %}
            </p>
            '''),
            Fieldset(
                'Profile',
                Field('username', readonly=True),
                Field('email'),
                Field('first_name'),
                Field('last_name'),
                Field('time_zone'),
            ),
            Fieldset(
                'Preferences',
                Field('glucose_unit'),
                Field('default_category'),
            ),
            Fieldset(
                'Glucose Levels',
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

    def clean_email(self):
        """
        Validates the email field.

        Check if the email field changed. If true, check whether the new email
        address already exists in the database and raise an error if it does.
        """
        email = self.cleaned_data['email']
        user = User.objects.get(username=self.cleaned_data['username'])

        if email != user.email:
            if User.objects.filter(email=email):
                raise forms.ValidationError('Another account is already using '
                                            'this email address.')

        return email
