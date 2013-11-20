from django.conf.urls import patterns, url

from .views import UserSettingsView


urlpatterns = patterns('',
    url(
        regex=r'^settings/',
        view=UserSettingsView.as_view(),
        name='usersettings',
    ),

)
