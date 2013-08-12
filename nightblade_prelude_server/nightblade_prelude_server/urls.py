from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nightblade_prelude_server.views.home', name='home'),
    # url(r'^nightblade_prelude_server/', include('nightblade_prelude_server.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^prelude/api/v0_2/$', 'prelude.views.main'),
    url(r'^prelude/api/v0_2/auth/$', 'prelude.views.authenticate'),
    url(r'^prelude/api/v0_2/character:(?P<query>.*)/$', 'prelude.views.character'),
    url(r'^prelude/api/v0_2/location:(?P<query>.*)/$', 'prelude.views.location'),
    url(r'^prelude/api/v0_2/action:(?P<query>.*)/$', 'prelude.views.action'),
    url(r'^prelude/.*$', 'prelude.views.redirect'),

    #url(r'^.*$', 'prelude.views.main'),
)
