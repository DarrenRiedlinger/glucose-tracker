from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from core.views import HomePageView
from glucoses.views import dashboard


urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('accounts.urls')),
    url(r'^core/', include('core.urls')),
    url(r'^glucoses/', include('glucoses.urls')),

    url(r'^dashboard/$', view=dashboard, name='dashboard'),
    url(r'^subscribe/$', view='subscribers.views.subscribe_view', name='subscribe'),
)

# For serving static files on Heroku, see
# http://matthewphiong.com/managing-django-static-files-on-heroku
from django.conf import settings
urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
)