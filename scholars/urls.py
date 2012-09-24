from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('djforms.scholars.views',
    url(r'^presentation/success/$', direct_to_template, {'template': 'scholars/presentation_done.html'}),
    url(r'^presentation/(?P<pid>\d+)/$', 'presentation_detail', name="presentation_detail"),
    url(r'^presentation/(?P<pid>\d+)/update/$', 'presentation_form', name="presentation_update"),
    url(r'^presentation/$', 'presentation_form', name='presentation_form'),
    url(r'^archives/(?P<year>\d{4})/$', 'scholars_archives', name="scholars_archives"),
)
