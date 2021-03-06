from django.conf.urls import url
from django.views.generic import TemplateView, RedirectView

from djforms.communications.metamorphosis.models import Questionnaire
from djforms.communications.printrequest import views as printrequest
from djforms.communications.metamorphosis import views as metamorphosis


urlpatterns = [
    # print request form
    url(
        r'^print-request/success/$', TemplateView.as_view(
            template_name='communications/printrequest/done.html'
        ),
        name='print_request_success'
    ),
    url(
        r'^print-request/$',
        printrequest.print_request,
        name='print_request'
    ),
    # How has your student changed since their freshman year?
    url(
        r'^metamorphosis/success/$',
        TemplateView.as_view(
            template_name='communications/metamorphosis/done.html'
        ),
        name='metamorphosis_questionnaire_success'
    ),
    url(
        r'^metamorphosis/(?P<quid>\d+)/detail/$',
        metamorphosis.questionnaire_detail,
        name='metamorphosis_questionnaire_detail'
    ),
    url(
        r'^metamorphosis/archives/$',
        TemplateView.as_view(
            template_name='communications/metamorphosis/archives.html',
        ),
        {'data':Questionnaire.objects.all()},
        name='metamorphosis_questionnaire_archives'
    ),
    url(
        r'^metamorphosis/(?P<who>[a-zA-Z0-9_-]+)/',
        metamorphosis.questionnaire_form,
        name='metamorphosis_questionnaire_form'
    )
]
