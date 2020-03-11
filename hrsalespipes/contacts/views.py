import json

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView

from .forms import ( ClientCreateModelForm, ContactCreateModelForm,
                     CandidateUpdateModelForm, ClientUpdateModelForm,
                     SupplierModelForm)
from .models import Candidate, Client, Supplier, Employee
from system.models import VisaStatus


class ContactsTemplatView(TemplateView):
    template_name = 'contacts/contacts.html'


class CandidateCreateView(CreateView):
    model = Candidate
    form_class = ContactCreateModelForm
    template_name = 'contacts/candidate_create_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        visa_status_objects = VisaStatus.objects.all()
        visa_status_objects = [{'value': data.pk, 'text': data.name}
                               for data in visa_status_objects]
        visa_status_objects = json.dumps(visa_status_objects)

        employees = Employee.objects.all()
        employees = [{'value': str(data.pk), 'text': data.name}
                     for data in employees]
        employees = json.dumps(employees)

        try:
            default_candidate_owner = self.request.user.as_employee
            context['default_candidate_owner'] = default_candidate_owner
        except Exception as e:
            context['default_candidate_owner'] = ''

        context['visa_status_objects'] = visa_status_objects
        context['employees'] = employees
        return context


class CandidateUpdateView(UpdateView):
    model = Candidate
    form_class = CandidateUpdateModelForm
    template_name = 'contacts/candidate_update_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        visa_status_objects = VisaStatus.objects.all()
        visa_status_objects = [{'value': data.pk, 'text': data.name}
                               for data in visa_status_objects]
        visa_status_objects = json.dumps(visa_status_objects)

        employees = Employee.objects.all()
        employees = [{'value': str(data.pk), 'text': data.name}
                     for data in employees]
        employees = json.dumps(employees)

        context['visa_status_objects'] = visa_status_objects
        context['employees'] = employees
        return context


class CandidateDetailView(DetailView):
    model = Candidate

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.select_related('visa_status', 'candidate_owner')
        return queryset


class CandidateListView(ListView):
    model = Candidate

    def get_queryset(self, **kwargs):
        q = super().get_queryset(**kwargs)
        q = q.select_related('candidate_owner')
        return q


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientCreateModelForm
    template_name = 'contacts/client_create_form.html'


class ClientListView(ListView):
    model = Client


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientUpdateModelForm
    template_name = 'contacts/client_update_form.html'


class ClientDetailView(DetailView):
    model = Client


class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierModelForm
    template_name = 'contacts/supplier_create_form.html'


class SupplierListView(ListView):
    model = Supplier


class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierModelForm
    template_name = 'contacts/supplier_update_form.html'


class SupplierDetailView(DetailView):
    model = Supplier
