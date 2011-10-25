from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

from djforms.sustainability.green.forms import PledgeForm
from djforms.sustainability.green.models import Pledge

#@login_required(login_url='https://www.carthage.edu/forms/accounts/login/?next=https://www.carthage.edu/sustainability/green/pledge/')
@login_required
def pledge_form(request):
    '''
    if not request.user.username:
        return HttpResponseRedirect("https://www.carthage.edu/forms/accounts/login/?next=https://www.carthage.edu/sustainability/green/pledge/")
    else:
        user = request.user
    '''
    user = request.user
    try:
        pledge = Pledge.objects.get(user=user)
    except:
        pledge = None

    if request.method=='POST':
        form = PledgeForm(request.POST)
        if form.is_valid() and not pledge:
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            bcc = settings.MANAGERS
            frm = user.email
            to = ["skirk@carthage.edu",]
            t = loader.get_template('sustainability/green/pledge_email.html')
            c = RequestContext(request, {'data':data,})
            email = EmailMessage(("[Sustainability Pledge] %s %s" % (user.first_name,user.last_name)), t.render(c), frm, to, bcc, headers = {'Reply-To': frm,'From': frm})
            email.content_subtype = "html"
            email.send()
            ret = '/forms/sustainability/green/pledge/success/'
            return HttpResponseRedirect(ret)
    else:
        form = PledgeForm(initial={'user':user.id})

    return render_to_response("sustainability/green/pledge_form.html", {"form": form,"pledge":pledge,}, context_instance=RequestContext(request))

def pledge_archives(request):
    pledges = Pledge.objects.all().order_by("-id")
    return render_to_response("sustainability/green/pledge_archives.html", {"pledges": pledges,}, context_instance=RequestContext(request))
