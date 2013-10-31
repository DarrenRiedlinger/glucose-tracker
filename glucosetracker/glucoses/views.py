from django.views.generic import CreateView, ListView, DetailView

from braces.views import LoginRequiredMixin

from .models import Glucose
from .forms import GlucoseCreateForm


class GlucoseCreateView(LoginRequiredMixin, CreateView):
    model = Glucose
    success_url = '/'
    template_name = 'glucoses/add_glucose.html'
    form_class = GlucoseCreateForm