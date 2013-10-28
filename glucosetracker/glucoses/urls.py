from django.conf.urls import patterns
from django.conf.urls import url

from .views import GlucoseDetailView


urlpatterns = patterns('',
    url(
        regex=r'^(?P<pk>\d+)/$',
        view=GlucoseDetailView.as_view(),
        name='detail'
    ),
)
