from django.contrib.auth.views import (
    logout,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete
)

from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from core.views import HomePageView
from glucoses.views import GlucoseListView


urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^glucoses/', include('glucoses.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Redirect to 'glucose_list' for now, update later.
    url(r'^dashboard/$', view=GlucoseListView.as_view(), name='dashboard'),

    url(r'^login/$', view='core.views.login_view', name='login'),
    url(regex=r'^logout/$', view=logout, kwargs={'next_page': '/login/'}, name='logout'),
)
