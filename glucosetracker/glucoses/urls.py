from django.conf.urls import patterns, url

from .views import (
    list_view,
    filter_view,
    GlucoseCreateView,
    GlucoseUpdateView,
    GlucoseDeleteView,
    GlucoseEmailReportView,
    GlucoseListJson,
    GlucoseChartsView,
)


urlpatterns = patterns('',
    url(
        regex=r'^add/',
        view=GlucoseCreateView.as_view(),
        name='glucose_create',
    ),
    url(
        regex=r'^list/',
        view=list_view,
        name='glucose_list',
    ),
    url(
        regex=r'^filter/',
        view=filter_view,
        name='glucose_filter',
    ),
    url(
        regex=r'^list_json/$',
        view=GlucoseListJson.as_view(),
        name='glucose_list_json',
    ),
    url(
        regex=r'^charts/$',
        view=GlucoseChartsView.as_view(),
        name='glucose_charts',
    ),
    url(
        regex=r'^email_report/',
        view=GlucoseEmailReportView.as_view(),
        name='glucose_email_report',
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
