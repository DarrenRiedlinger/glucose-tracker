from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from .views import HomePageView


urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^glucoses/', include('glucoses.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
