import environ
from uuid import uuid4

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import date as date_filter
from django.http import HttpResponse
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

import jinja2
from django_extensions.db.models import TimeStampedModel
from docxtpl import DocxTemplate


CURRENT_DIR = environ.Path(__file__) - 1
jinja_env = jinja2.Environment()
jinja_env.filters['date'] = date_filter


class ContactModel(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    code = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=100)
    contact_number = models.TextField(max_length=32, blank=True)
    alternate_contact_number = models.CharField(max_length=32, blank=True)
    website = models.URLField(blank=True)
    whatsapp_link = models.URLField(blank=True)
    email_address = models.EmailField(blank=True)
    skype_id = models.CharField(max_length=50, blank=True)
    ms_teams_id = models.CharField(max_length=200, blank=True)
    other_online_ids = models.TextField(blank=True)
    location = models.CharField(max_length=64, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        abstract = True
        ordering = 'name',
        unique_together = ['name', 'email_address']

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


class DocxResponseMixin(SingleObjectMixin):
    content_type = 'application/vnd.openxmlformats-officedocument.\
        wordprocessingml.document'
    docx_filename = None
    position = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_docx_template(self):
        """returns file path of the template"""
        cv_template = self.object.cv_template
        if cv_template:
            cv_template = cv_template
        else:
            CVTemplate = ContentType.objects.get(
                app_label='contacts',
                model='cvtemplate').model_class()
            cv_template = CVTemplate.objects.filter(is_default=True).first()

        return cv_template.template.file.name

    def get_docx(self):
        """ Returns a docx.Document object"""
        document = DocxTemplate(self.get_docx_template())
        instance = self.object

        context = {}
        if instance:
            Candidate = ContentType.objects.get(
                app_label='contacts',
                model='candidate').model_class()
            fields = Candidate.CV_FIELDS
            for field in fields:
                context[field] = str(getattr(instance, field, ''))
            context['position'] = self.position

        document.render(context, jinja_env)
        return document.docx

    def response(self):

        content_disposition = 'attachment; filename=CV.docx'
        response = HttpResponse(content_type=self.content_type)
        response['Content-Disposition'] = content_disposition

        docx = self.get_docx()
        docx.save(response)

        return response


class DownloadCVBaseView(DocxResponseMixin, View):

    def get(self, request, *args, **kwargs):
        self.position = request.GET.get('position', '')
        self.object = self.get_object()
        return self.response()
