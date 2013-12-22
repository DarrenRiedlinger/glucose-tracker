from django.conf.urls import patterns, url

from .views import UserSettingsView, HelpPageView


urlpatterns = patterns('',
    url(
        regex=r'^settings/',
        view=UserSettingsView.as_view(),
        name='usersettings',
    ),
    url(
        regex=r'^help/',
        view=HelpPageView.as_view(),
        name='help',
    ),
)
