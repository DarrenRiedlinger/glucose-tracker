from django.conf.urls import patterns, url

from .views import GlucoseCreateView, GlucoseListView, GlucoseDetailView


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
        regex=r'^detail/(?P<pk>\d+)/',
        view=GlucoseDetailView.as_view(),
        name='glucose_detail',
    ),
)
