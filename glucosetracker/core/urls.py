from django.conf.urls import patterns, url

from .views import HelpPageView


urlpatterns = patterns('',
    url(
        regex=r'^help/',
        view=HelpPageView.as_view(),
        name='help',
    ),
)
