from django.views.generic import CreateView, ListView, DetailView

from braces.views import LoginRequiredMixin

from .models import Glucose


class GlucoseDetailView(LoginRequiredMixin, DetailView):
    model = Glucose