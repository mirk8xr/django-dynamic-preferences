# !/usr/bin/env python
# encoding:UTF-8

from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf import settings
from dynamic_preferences.registries import autodiscover

admin.autodiscover()

urlpatterns = i18n_patterns(
    '',
    url(r'^$', 'example.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^preferences/', include('dynamic_preferences.urls')),
    url(r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

autodiscover(True)
