from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.security.views',
    url(
        r'^success/$', TemplateView.as_view(template_name="security/data_entered.html")
    ),
    url(
        r'^parking-appeal/$', 'parking_ticket_appeal_form', name='parking_ticket_appeal_form'
    ),
)