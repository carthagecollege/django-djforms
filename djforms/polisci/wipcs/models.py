from django.db import models

from djforms.core.models import GenericChoice
from djforms.processors.models import Contact
from tagging import fields, managers

SUBMITTING =(
    ("Paper for presentation", "Paper for presentation"),
    ("Poster for presentation", "Poster for presentation"),
    ("Roundtable proposal", "Roundtable proposal")
)

class RegistrationContact(Contact):

    how_hear = models.CharField(
        "How did you hear about this conference?",
         max_length="128"
    )
    abstract = models.TextField()
    cv = models.FileField(
        'CV', upload_to='files/polisci/conferences/cvs/',
        max_length="256"
    )
    submitting = models.CharField(
        "Are you submitting:",
        max_length="128", choices=SUBMITTING
    )
