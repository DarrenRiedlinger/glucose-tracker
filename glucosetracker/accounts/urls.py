from django.contrib.auth.views import (
    logout,
    password_change,
    password_change_done,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete
)
from django.conf.urls import patterns, url

from .views import login_view, UserSettingsView, SignUpView


urlpatterns = patterns('',
    url(
        regex=r'^signup/',
        view=SignUpView.as_view(),
        name='signup',
    ),
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
        regex=r'^logout/$',
        view=logout,
        kwargs={'next_page': '/accounts/login/'},
        name='logout'
    ),
    url(
        regex=r'^password/change/$',
        view=password_change,
        name='password_change'
    ),
    url(
        regex=r'^password/change/done/$',
        view=password_change_done,
        name='password_change_done'
    ),
    url(
        regex=r'^password/reset/$',
        view=password_reset,
        name='password_reset'
    ),
    url(
        regex=r'^password/reset/done/$',
        view=password_reset_done,
        name='password_reset_done'
    ),
    url(
        regex=r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        view=password_reset_confirm,
        name='password_reset_confirm'
    ),
    url(
        regex=r'^password_reset_complete/$',
        view=password_reset_complete,
        name='password_reset_complete'
    ),
)
