from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from djforms.characterquest.forms import ApplicationForm, ApplicationProfileForm
from djforms.core.models import UserProfile

@login_required
def application_profile_form(request):
    try:
        profile = request.user.get_profile()
    except:
        p = UserProfile(user=request.user)
        p.save()
        profile = request.user.get_profile()
    if request.method=='POST':
        form = ApplicationForm(request.POST, prefix="applicant")
        profile_form = ApplicationProfileForm(request.POST, prefix="profile", instance=profile)
        if form.is_valid() and profile_form.is_valid():
            profile = profile_form.save()
            applicant = form.save(commit=False)
            applicant.profile = profile
            applicant.save()

            bcc = settings.MANAGERS
            recipient_list = ["jramirez@carthage.edu",request.user.email]
            t = loader.get_template('characterquest/application_email.txt')
            c = RequestContext(request, {'data':applicant,})
            email = EmailMessage(("CharacterQuest Application: %s %s" % (applicant.profile.user.first_name,applicant.profile.user.last_name)), t.render(c), request.user.email, recipient_list, bcc_list, headers = {'Reply-To': request.user.email,'From': request.user.email})
            email.content_subtype = "html"
            email.send(fail_silently=True)
            return HttpResponseRedirect('/forms/character-quest/data-entered')
    else:
        form = ApplicationForm(prefix="applicant")
        profile_form = ApplicationProfileForm(prefix="profile", instance=profile)
    return render_to_response("characterquest/application_form.html", {"form": form, "profile_form":profile_form}, context_instance=RequestContext(request))
