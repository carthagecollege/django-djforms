from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^success/$', direct_to_template, {'template': 'alumni/data_entered.html'}),
    url(r'^memory/(?P<quid>\d+)/detail/$', 'djforms.alumni.memory.views.questionnaire_detail', name="memory_questionnaire_detail"),
    url(r'^memory/$', 'djforms.alumni.memory.views.questionnaire_form', name='memory_questionnaire_form'),
    url(r'^msw/reunion/success/$', direct_to_template, {'template': 'alumni/msw/reunion_contact_done.html'}),
    url(r'^msw/reunion/(?P<id>\d+)/detail/$', 'djforms.alumni.msw.views.reunion_contact_detail', name="reunion_contact_detail"),
    url(r'^msw/reunion/$', 'djforms.alumni.msw.views.reunion_contact_form', name='reunion_contact_form'),
    url(r'^distinguished-alumni/nomination/$', 'djforms.alumni.distinguished.views.nomination_form', name='nomination_form'),
)
