from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('htmlmail.views',
    url(r'^$', 'home', name='home'),
    url(r'^preview/(?P<name>\w+)$', 'preview', name='preview'),
)

urlpatterns += patterns('',
    # url(r'^htmlmail/', include('htmlmail.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
