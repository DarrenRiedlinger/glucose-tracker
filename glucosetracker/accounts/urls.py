from django.contrib.auth.views import (
    logout,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete
)

from django.conf.urls import patterns, url

from .views import login_view, UserSettingsView


urlpatterns = patterns('',
    url(
        regex=r'^settings/',
        view=UserSettingsView.as_view(),
        name='usersettings',
    ),
    url(
        regex=r'^login/$',
        view=login_view,
        name='login',
    ),
    url(
        r'^logout/$',
        view=logout,
        kwargs={'next_page': '/accounts/login/'},
        name='logout'
    ),
)
