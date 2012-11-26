from django.db import models
from django.conf import settings

from djforms.core.models import GenericContact

"""
Model Contact
"""

class Contact(GenericContact):
    second_name         = models.CharField("Middle name", max_length=128, null=True, blank=True)
    previous_name       = models.CharField("Previous name", max_length=128, help_text="e.g. Maiden name", null=True, blank=True)
    salutation          = models.CharField(max_length=16, null=True, blank=True,help_text="e.g. Ms., Mr. Dr.")
    suffix              = models.CharField(max_length=16, null=True, blank=True,help_text="e.g. PhD., Esquire, Jr., Sr., III")
    # core
    classyear           = models.CharField("Class",max_length=4)
    spousename          = models.CharField("Spouse's name", max_length=128,blank=True,null=True)
    spousepreviousname  = models.CharField("Spouse's previous name",help_text="e.g. maiden name",max_length=32,blank=True,null=True)
    spouseyear          = models.CharField("Spouse's class",max_length=4,blank=True,null=True)
    classnote           = models.TextField("Note")
    alumnistatus        = models.BooleanField("Almuni office status",default=False)
    alumnicomments      = models.TextField("Alumni office comments",blank=True,null=True)
    pubstatus           = models.BooleanField("Publication status",default=False)
    pubstatusdate       = models.DateTimeField("Web Publication Date",blank=True,null=True)
    carthaginianstatus  = models.BooleanField("Carthiginian status",default=False)
    picture             = models.ImageField("Photo",max_length=255,upload_to="files/alumni/classnotes/photos",help_text="75 dpi and .jpg only",blank=True,null=True)
    caption             = models.CharField("Caption for the photo",max_length=255,blank=True,null=True)

    class Meta:
        db_table = 'alumni_classnotes_contact'

    def __unicode__(self):
        return "%s, %s (%s)" % (self.last_name, self.first_name, self.classyear)

    def get_edit_url(self):
        return "http://%s/forms/admin/classnotes/contact/%s/" % (settings.SERVER_URL, self.id)