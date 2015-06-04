from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.global_bridge.views',
    # registration
    url(
        r'^registration/success/$',
        TemplateView.as_view(
            template_name="global_bridge/registration_done.html"
        ),
        name="global_bridge_registration_success"
    ),
    url(
        r'^registration/$', 'index',
        name="global_bridge_registration"
    ),
)
