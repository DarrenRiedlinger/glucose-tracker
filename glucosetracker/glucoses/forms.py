from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout

from .models import Glucose


class GlucoseCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

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
        self.helper.add_input(Submit('submit', 'Save'))

        super(GlucoseUpdateForm, self).__init__(*args, **kwargs)

        # Remove the blank option from the select widget.
        self.fields['category'].empty_label = None

    class Meta:
        model = Glucose
        exclude = ('user',)