from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from djforms.characterquest.forms import ApplicationForm
from djforms.characterquest.forms import ApplicationProfileForm
from djforms.core.models import UserProfile

from djtools.utils.mail import send_mail
from djtools.fields import TODAY

from datetime import date


@login_required
def application_profile_form(request):
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL]
    else:
        TO_LIST = list(settings.CHARACTER_QUEST_TO_LIST)
    BCC = settings.MANAGERS

    s_date = date(
        TODAY.year,
        settings.CHARACTER_QUEST_START_MONTH,
        settings.CHARACTER_QUEST_START_DAY
    )
    x_date = date(
        TODAY.year,
        settings.CHARACTER_QUEST_END_MONTH,
        settings.CHARACTER_QUEST_END_DAY
    )
    expired = False
    if x_date < TODAY or s_date > TODAY:
        if not request.user.is_staff and \
        not request.user.has_perm('characterquest.change_applicationprofile'):
            expired = True
    try:
        profile = request.user.userprofile
    except:
        p = UserProfile(user=request.user)
        p.save()
        profile = request.user.userprofile
    if request.method=='POST':
        form = ApplicationForm(request.POST, prefix='applicant')
        profile_form = ApplicationProfileForm(
            request.POST,
            prefix='profile',
            instance=profile
        )
        if form.is_valid() and profile_form.is_valid():
            profile = profile_form.save()
            applicant = form.save(commit=False)
            applicant.profile = profile
            applicant.save()
            if not settings.DEBUG:
                TO_LIST.append(request.user.email)
            subject = "LEAD Retreat Application: {} {}".format(
                applicant.profile.user.first_name,
                applicant.profile.user.last_name
            )
            send_mail (
                request, TO_LIST, subject, request.user.email,
                'characterquest/application_email.txt', applicant, BCC
            )

            return HttpResponseRedirect('/forms/character-quest/success/')
    else:
        form = ApplicationForm(prefix='applicant')
        profile_form=ApplicationProfileForm(prefix='profile',instance=profile)

    return render(
        request, 'characterquest/application_form.html',
        {'form': form, 'profile_form':profile_form, 'expired':expired}
    )
