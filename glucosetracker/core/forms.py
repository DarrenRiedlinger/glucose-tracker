from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Fieldset, HTML, Field
from crispy_forms.bootstrap import FormActions


class ContactForm(forms.Form):
    email = forms.EmailField(label='Your Email Address')
    subject = forms.CharField(required=False)
    message = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 50, 'rows': 6}))

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-xs-12 col-md-6'

        self. helper.layout = Layout(
            HTML('''
            {% if messages %}
            {% for message in messages %}
            <p {% if message.tags %} class="text-{{ message.tags }}"\
            {% endif %}>{{ message }}</p>{% endfor %}{% endif %}
            '''),
            Fieldset(
                'Contact Us',
                Field('email'),
                Field('subject'),
                Field('message'),
            ),
            FormActions(Submit('submit', 'Send', css_class='pull-right'))
        )