from uuid import uuid4

from django.db import models

from django_extensions.db.models import TimeStampedModel

from system.models import Location


class ContactModel(TimeStampedModel):

    class Meta:
        abstract = True
        ordering = 'name',

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    code = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=100, unique=True)
    contact_number = models.TextField(max_length=32, blank=True)
    alternate_contact_number = models.CharField(max_length=32, blank=True)
    whatsapp_link = models.URLField(blank=True)
    email_address = models.EmailField(blank=True)
    skype_id = models.CharField(max_length=50, blank=True)
    ms_teams_id = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=64, blank=True)

    def __str_(self):
        return self.name


class FormCleanContactNumber:

    def clean_contact_number(self):
        contact_number = self.cleaned_data['contact_number']
        try:
            if contact_number[0] == '0':
                contact_number = contact_number[1:]
        except Exception as e:
            pass

        return contact_number


class FilterNameMixin:
    paginate_by = 25

    def get_queryset(self, **kwargs):
        q = super().get_queryset(**kwargs)

        name = self.request.GET.get('name', '')
        if name:
            q = q.filter(name__icontains=name)
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get('name', '')
        context['search_name'] = name
        return context
