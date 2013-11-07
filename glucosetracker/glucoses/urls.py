from django.conf.urls import patterns, url

from .views import GlucoseCreateView, GlucoseListView, GlucoseUpdateView, \
    GlucoseDeleteView


urlpatterns = patterns('',
    url(
        regex=r'^add/',
        view=GlucoseCreateView.as_view(),
        name='glucose_create',
    ),
    url(
        regex=r'^list/',
        view=GlucoseListView.as_view(),
        name='glucose_list',
    ),
    url(
        regex=r'^(?P<pk>\d+)/edit/',
        view=GlucoseUpdateView.as_view(),
        name='glucose_update',
    ),
    url(
        regex=r'^(?P<pk>\d+)/delete/',
        view=GlucoseDeleteView.as_view(),
        name='glucose_delete',
    ),
)
