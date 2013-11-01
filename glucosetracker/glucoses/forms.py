from django import forms

from crispy_forms import bootstrap
from .models import Glucose


class GlucoseCreateForm(forms.ModelForm):

    class Meta:
        model = Glucose
        exclude = ('created', 'modified',)