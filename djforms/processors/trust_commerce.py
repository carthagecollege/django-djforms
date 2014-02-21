from django.conf import settings

import tclink

import logging
logging.basicConfig(filename=settings.LOG_FILENAME,level=logging.INFO)

class PaymentProcessor():
    """
    TrustCommerce payment processing module.
    Reqs:
    1) card object
    2) order object
    """

    def __init__(self, card=None, order=None, contact=None):
        self.demo = 'n'
        self.avs = settings.TC_AVS
        self.custid = settings.TC_LOGIN
        self.password = settings.TC_PASSWORD
        if not settings.TC_LIVE:
            self.demo = 'y'
        self.cycle = settings.TC_CYCLE
        self.auth = settings.TC_AUTH_TYPE
        self.order = order
        self.contact = contact
        self.card = card
        self.status = None
        self.success = None
        self.msg = None
        self.operator = settings.TC_OPERATOR
        self.tclink_version = tclink.getVersion()
        self.response = self.capture_payment()

    def prepare_post(self):
        # See tclink developer's guide for additional fields and info.

        # auth type
        if self.order.auth and self.order.auth != "":
            self.auth = self.order.auth

        # override avs from form
        if hasattr(self.order, 'avs') and self.order.avs == "True":
            self.avs = 'y'

        # billing period
        if hasattr(self.order, 'cycle'):
            self.cycle = self.order.cycle

        # operator
        if self.order.operator:
            # OJO: if value exceeds 20 characters, trans returns "baddata"
            self.operator = self.order.operator[:20]

        # Convert amount to cents, no decimal point
        amount = unicode( int( float(self.order.total) * 100 ) )

        # convert exp date to mmyy from mm/yy or mm/yyyy
        exp = u"%.2d%.2d" % (int(self.card['expiration_month']), (int(self.card['expiration_year']) % 100))

        self.transactionData = {
            # account data
            'custid'        : self.custid,
            'password'      : self.password,
            'demo'          : self.demo,
            # customer data
            'name'          : self.card['billing_name'],
            # transaction data
            'media'         : 'cc',
            'action'        : self.auth,
            'amount'        : amount,                       # in cents
            'cc'            : self.card['card_number'],     # 4111111111111111
            'exp'           : exp,                          # 4 digits eg 0108
            'cvv'           : self.card['security_code'],   # 3 or 4 digits
            'avs'           : self.avs,                     # address verification
            'operator'      : self.operator
        }

        # address verification
        if self.avs == 'y':
            self.transactionData['address1'] = self.contact.address1
            self.transactionData['address2'] = self.contact.address2
            self.transactionData['city']     = self.contact.city
            self.transactionData['state']    = self.contact.state
            self.transactionData['zip']      = self.contact.postal_code

        # subscription/recurring billing
        if self.auth == "store":
            self.transactionData['cycle'] = self.order.cycle
            self.transactionData['payments'] = unicode(self.order.payments)
            if hasattr(self.order, 'start_date'):
                if self.order.start_date:
                    self.transactionData['start'] = unicode(self.order.start_date)

        for key, value in self.transactionData.items():
            if isinstance(value, unicode):
                self.transactionData[key] = value.encode('utf7',"ignore")

    def capture_payment(self):
        """
        process the transaction through tclink
        """

        if self.order:
            self.prepare_post()
            result = tclink.send(self.transactionData)
            status = result['status']
            success = False

            logging.info("tdata = %s" % self.transactionData)
            if status == 'approved' or status == 'accepted':
                success = True
                msg = result
            else:
                if status == 'decline':
                    msg = result['declinetype']
                elif status == 'baddata':
                    msg = result['offenders']
                    #msg = result
                elif status == 'error':
                    msg == result['errortype']
                else:
                    status = "error"
                    msg = 'An error occurred: %s' % result

            self.status = status
            self.success = success
            self.msg = msg

        return self