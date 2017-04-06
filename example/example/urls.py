from django.conf.urls import patterns, include, url
from django.contrib import admin
from dynamic_preferences.registries import autodiscover

admin.autodiscover()


urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'example.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^preferences/', include('dynamic_preferences.urls')),
)

autodiscover(True)
