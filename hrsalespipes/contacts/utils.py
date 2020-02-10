from uuid import uuid4

from django.db import models

from django_extensions.db.models import TimeStampedModel


class ContactModel(TimeStampedModel):

    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=32, blank=True)
    alternate_contact_number = models.CharField(max_length=32, blank=True)
    whatsapp_link = models.URLField(blank=True)
    email_address = models.EmailField(blank=True)
    skype_id = models.CharField(max_length=50, blank=True)
    ms_teams_id = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=64, blank=True)

    def __str_(self):
        return self.name
