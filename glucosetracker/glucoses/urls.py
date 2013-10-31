from django.conf.urls import patterns, url

from .views import GlucoseCreateView


urlpatterns = patterns('',
    url(
        regex=r'^add$',
        view=GlucoseCreateView.as_view(),
        name='add_glucose',
    ),
)
