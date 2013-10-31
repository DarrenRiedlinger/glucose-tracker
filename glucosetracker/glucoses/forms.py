from django import forms

from .models import Glucose

class GlucoseCreateForm(forms.ModelForm):
    class Meta:
        model = Glucose
        exclude = ('created', 'modified',)
