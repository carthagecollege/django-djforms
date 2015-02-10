from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

from localflavor.us.forms import USPhoneNumberField

from djforms.communications.printrequest.models import PrintRequest
from djforms.communications.printrequest.models import FORMATS, CONSENT

from djtools.fields import BINARY_CHOICES

class PrintRequestForm(forms.ModelForm):

    print_format = forms.MultipleChoiceField(
        label = "What is the format of your finished piece",
        choices=FORMATS,
        help_text="Check all that apply"
    )
    consent = forms.TypedChoiceField(
        label = mark_safe("""
        If the Office of Communications coordinates
        your mailing with a mail house, we need your
        mailing list at least one week before the mail
        date. It is your responsibility to coordinate
        the request from Institutional Advancement within
        their established guidelines and procedures.
        Advancement requires two weeks lead time to produce
        a mail file. Requests can be submitted via the
        <a href="https://docs.google.com/a/carthage.edu/forms/d/1rIaD2Sm-UZSo8RBgLYk6XmnlqwPUF9di4v2f22-Iz-U/viewform?c=0&w=1">
        Advancement Office List Request Form
        </a>.
        """),
        choices=CONSENT, widget=forms.RadioSelect(),
    )
    is_mailing = forms.TypedChoiceField(
        label = "Is this project being mailed?",
        choices=BINARY_CHOICES, widget=forms.RadioSelect(),
    )
    attachments = forms.TypedChoiceField(
        label = "Are you submitting any files with this print request?",
        choices=BINARY_CHOICES, widget=forms.RadioSelect(),
    )

    def clean(self):
        cleaned_data = super(PrintRequestForm, self).clean()
        is_mailing = cleaned_data.get("is_mailing")
        who_mailing = cleaned_data.get("who_mailing")
        how_mailing = cleaned_data.get("how_mailing")
        speed_mailing = cleaned_data.get("speed_mailing")

        if is_mailing == "Yes":
            if who_mailing == "":
                self._errors["who_mailing"] = self.error_class(["Required field."])
            if how_mailing == "":
                self._errors["how_mailing"] = self.error_class(["Required field."])
            if speed_mailing == "":
                self._errors["speed_mailing"] = self.error_class(["Required field."])

        print_format = cleaned_data.get("print_format")
        print_format_other = cleaned_data.get("print_format_other")

        if print_format and "Other" in print_format and print_format_other == "":
            error = '''
                This field is required since you chose "Other"
                in the previous field
            '''

            self._errors["print_format_other"] = self.error_class([error])

        return cleaned_data

    class Meta:
        model = PrintRequest
        widgets = {
            'phone': forms.TextInput(attrs={
                'placeholder': 'eg. 123-456-7890', 'class': 'phoneUS'
            }),
        }
        exclude = (
            'user','updated_by','date_created','date_updated'
        )

