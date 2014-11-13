from django.db import models
from django.core.urlresolvers import reverse

#from djforms.core.models import Photo
from djforms.core.models import GenericContact

from localflavor.us.models import USStateField

class Questionnaire(GenericContact):
    """
    removed photos for now, since no one uses that feature
    and we need to upgrade to the more recent project on github:

    git@github.com:matthewwithanm/django-imagekit.git
    """
    address         = models.CharField(
        max_length=255, verbose_name = 'Address'
    )
    city            = models.CharField(
        max_length=128, verbose_name = 'City'
    )
    state           = USStateField()
    postal_code     = models.CharField(
        max_length=10, verbose_name = 'Zip code'
    )
    phone           = models.CharField(
        max_length=12, verbose_name='Phone Number',
        help_text="Format: XXX-XXX-XXXX"
    )
    occupation1     = models.CharField(
        max_length=100, verbose_name = 'Occupation',
        help_text = 'What someone pays you to do.', null=True, blank=True
    )
    occupation2     = models.CharField(
        max_length=100, verbose_name = 'Occupation',
        help_text = 'What no one pays you to do but you do anyway.',
        null=True, blank=True
    )
    why_carthage    = models.TextField(
        'How did you choose to attend Carthage?'
    )
    professor       = models.CharField(
        max_length=100,
        verbose_name = 'Who was your favorite Carthage professor?',
        null=True, blank=True
    )
    professor_why   = models.TextField(
        'Why?', null=True, blank=True
    )
    special         = models.TextField(
        'What makes the class of 1963 special?', null=True, blank=True
    )
    relive          = models.TextField(
        verbose_name="""If you had the chance to relive a single Carthage moment
            or event, which one would you choose?""",
        null=True, blank=True
    )
    message         = models.TextField(
        'Personal message',
        help_text="""You may want to include family, hobbies, travel
            experiences and fond rememberances.""",
            null=True, blank=True
    )
    #photos          = models.ManyToManyField(
    #    Photo, verbose_name="Photos",
    #    related_name="alumni_memory_questionaire_photos",null=True,blank=True
    #)

    class Meta:
        db_table = 'alumni_memory_questionnaire'

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse("memory_questionnaire_detail", args=[self.pk])
