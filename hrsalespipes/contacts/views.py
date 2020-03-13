import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView

from .forms import (ClientCreateModelForm, ContactCreateModelForm,
                    CandidateUpdateModelForm, ClientUpdateModelForm,
                    SupplierModelForm)
from .models import Candidate, Client, Supplier, Employee
from system.utils import PermissionRequiredWithCustomMessageMixin as PermissionRequiredMixin
from system.models import VisaStatus


class ContactsTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'contacts/contacts.html'


class CandidateCreateView(PermissionRequiredMixin, CreateView):
    model = Candidate
    form_class = ContactCreateModelForm
    template_name = 'contacts/candidate_create_form.html'
    permission_required = ('contacts.add_candidate')

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


class CandidateUpdateView(PermissionRequiredMixin, UpdateView):
    model = Candidate
    form_class = CandidateUpdateModelForm
    template_name = 'contacts/candidate_update_form.html'
    permission_required = ('contacts.change_candidate')

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


class CandidateDetailView(PermissionRequiredMixin, DetailView):
    model = Candidate
    permission_required = ('contacts.view_candidate')

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.select_related('visa_status', 'candidate_owner')
        return queryset


class CandidateListView(PermissionRequiredMixin, ListView):
    model = Candidate
    permission_required = ('contacts.view_candidate')

    def get_queryset(self, **kwargs):
        q = super().get_queryset(**kwargs)
        q = q.select_related('candidate_owner')
        return q


class ClientCreateView(PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientCreateModelForm
    template_name = 'contacts/client_create_form.html'
    permission_required = ('contacts.add_client')


class ClientListView(PermissionRequiredMixin, ListView):
    model = Client
    permission_required = ('contacts.view_client')


class ClientUpdateView(PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientUpdateModelForm
    template_name = 'contacts/client_update_form.html'
    permission_required = ('contacts.change_client')


class ClientDetailView(PermissionRequiredMixin, DetailView):
    model = Client
    permission_required = ('contacts.view_client')


class SupplierCreateView(PermissionRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierModelForm
    template_name = 'contacts/supplier_create_form.html'
    permission_required = ('contacts.add_supplier')


class SupplierListView(PermissionRequiredMixin, ListView):
    model = Supplier
    permission_required = ('contacts.view_supplier')


class SupplierUpdateView(PermissionRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierModelForm
    template_name = 'contacts/supplier_update_form.html'
    permission_required = ('contacts.change_supplier')


class SupplierDetailView(PermissionRequiredMixin, DetailView):
    model = Supplier
    permission_required = ('contacts.view_supplier')
