from django.conf import settings
from django.core.mail import EmailMessage
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect

from djforms.processors.forms import DonationOrderForm, SubscriptionOrderForm, ContactForm, TrustCommerceForm as CreditCardForm
from djforms.core.models import Promotion

def giving_form(request, transaction, campaign=None):
    # giving campaigns
    if campaign:
        campaign = get_object_or_404(Promotion, slug=campaign)
    status = None
    if request.POST:
        ct_form = ContactForm(request.POST, prefix="ct")
        or_form = OrderForm(request.POST, prefix="or")
        if ct_form.is_valid() and or_form.is_valid():
            # we might have a record for 'contact' so we use get_or_create() method
            contact, created = Contact.objects.get_or_create(first_name=con_data['first_name'], last_name=con_data['last_name'], email=con_data['email'], phone=con_data['phone'],address1=con_data[
'address1'],address2=con_data['address2'],city=con_data['city'],state=con_data['state'],postal_code=con_data['postal_code'])
            or_data = or_form.save(commit=False)
            or_data.contact = contact
            or_data.status = "In Process"
            or_data.save()
            cc_form = CreditCardForm(or_data, request.POST, prefix="cc")
            if cc_form.is_valid():
                # save and update order
                r = cc_form.processor_response
                # deal with payments
                years = str( int(or_data.payments) / 12 )
                if or_data.cycle != "1m":
                    or_data.payments = str( int(or_data.payments) / int(or_data.cycle[:-1]) )
                or_data.status = r.msg['status']
                or_data.billingid = r.msg['billingid']
                or_data.transid = r.msg['transid']
                if campaign:
                    or_data.promotion = campaign
                or_data.save()
                # sendmail
                bcc = settings.MANAGERS
                recipient_list = ["lpieta@carthage.edu","lhansen@carthage.edu",]
                t = loader.get_template('giving/pledge_email.html')
                c = RequestContext(request, {'order':or_data,'campaign':campaign,'years':years,})
                email = EmailMessage(("[pledge Donation] %s %s" % (or_data.contact.first_name,or_data.contact.last_name)), t.render(c), or_data.contact.email, recipient_list, bcc, headers = {'Reply-To': or_data.contact.email,'From': or_data.contact.email})
                email.content_subtype = "html"
                email.send(fail_silently=True)
                # redirect
                slug = ""
                if campaign:
                    slug = campaign.slug
                url = 'http://www.carthage.edu/forms/giving/pledge/success/%s' % slug
                return HttpResponseRedirect(url)
            else:
                r = cc_form.processor_response
                status = r.status
                if r:
                    or_data.status = status
                else:
                    or_data.status = "Blocked"
                or_data.save()
        else:
            cc_form = CreditCardForm(None, request.POST, prefix="cc")
            cc_form.is_valid()
    else:
        ct_form = ContactForm(prefix="ct")
        or_form = OrderForm(prefix="or", initial={'cycle': "1m", 'avs':False,'auth':'store',})
        cc_form = CreditCardForm(prefix="cc")

    return render_to_response('giving/pledge_form.html',
                              {'ct_form': ct_form, 'or_form': or_form, 'cc_form': cc_form, 'status': status, 'campaign': campaign,},
                              context_instance=RequestContext(request))

def pledge_success(request, transaction, campaign=None):
    # giving campaigns
    if campaign:
        campaign = get_object_or_404(Promotion, slug=campaign)

    return render_to_response('giving/pledge_success.html',
                              { 'campaign': campaign, },
                              context_instance=RequestContext(request))
