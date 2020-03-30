from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView

from .forms import (ClientCreateModelForm,
                    CandidateUpdateModelForm, ClientUpdateModelForm,
                    SupplierModelForm, CandidateCreateModelForm)
from .models import Candidate, Client, Supplier, Employee, CVTemplate
from .utils import FilterNameMixin, DownloadCVBaseView
from system.helpers import get_objects_as_choices, ActionMessageViewMixin
from system.utils import (
    PermissionRequiredWithCustomMessageMixin as PermissionRequiredMixin)
from system.models import VisaStatus, Location, Nationality, Industry


class ContactsTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'contacts/contacts.html'


class CandidateCreateView(
        PermissionRequiredMixin,
        ActionMessageViewMixin,
        CreateView):
    model = Candidate
    form_class = CandidateCreateModelForm
    template_name = 'contacts/candidate_create_form.html'
    permission_required = ('contacts.add_candidate')
    success_msg = 'Candidate created.'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        employees = get_objects_as_choices(Employee)
        locations = get_objects_as_choices(Location)

        try:
            default_candidate_owner = self.request.user.as_employee
            context['default_candidate_owner'] = default_candidate_owner
        except Exception as e:
            context['default_candidate_owner'] = ''

        context['employees'] = employees
        context['locations'] = locations
        return context


class CandidateUpdateView(
        PermissionRequiredMixin,
        ActionMessageViewMixin,
        UpdateView):
    model = Candidate
    form_class = CandidateUpdateModelForm
    template_name = 'contacts/candidate_update_form.html'
    permission_required = ('contacts.change_candidate')
    success_msg = 'Candidate updated.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['visa_status_objects'] = get_objects_as_choices(VisaStatus)
        context['cv_templates'] = get_objects_as_choices(CVTemplate)
        context['employees'] = get_objects_as_choices(Employee)
        context['locations'] = get_objects_as_choices(Location)
        context['nationalities'] = get_objects_as_choices(Nationality)
        return context

    def get_success_url(self):
        return reverse(
            'contacts:candidates_detail',
            args=[str(self.object.id), ])


class CandidateDetailView(PermissionRequiredMixin, DetailView):
    model = Candidate
    permission_required = ('contacts.view_candidate')

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.select_related(
            'visa_status', 'candidate_owner', 'cv_template')
        return queryset


class CandidateListView(FilterNameMixin, PermissionRequiredMixin, ListView):
    model = Candidate
    permission_required = ('contacts.view_candidate')

    def get_queryset(self, **kwargs):
        q = super().get_queryset(**kwargs)
        q = q.select_related('candidate_owner')
        return q


class ClientCreateView(
        PermissionRequiredMixin,
        ActionMessageViewMixin,
        CreateView):
    model = Client
    form_class = ClientCreateModelForm
    template_name = 'contacts/client_create_form.html'
    permission_required = ('contacts.add_client')
    success_msg = 'Client created.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        locations = get_objects_as_choices(Location)

        context['locations'] = locations
        return context


class ClientListView(FilterNameMixin, PermissionRequiredMixin, ListView):
    model = Client
    permission_required = ('contacts.view_client')


class ClientUpdateView(
        PermissionRequiredMixin,
        ActionMessageViewMixin,
        UpdateView):
    model = Client
    form_class = ClientUpdateModelForm
    template_name = 'contacts/client_update_form.html'
    permission_required = ('contacts.change_client')
    success_msg = 'Client updated.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['locations'] = get_objects_as_choices(Location)
        context['industries'] = get_objects_as_choices(Industry)
        return context

    def get_success_url(self):
        return reverse('contacts:clients_detail', args=[str(self.object.id)])


class ClientDetailView(PermissionRequiredMixin, DetailView):
    model = Client
    permission_required = ('contacts.view_client')


class SupplierCreateView(
        PermissionRequiredMixin,
        ActionMessageViewMixin,
        CreateView):
    model = Supplier
    form_class = SupplierModelForm
    template_name = 'contacts/supplier_create_form.html'
    permission_required = ('contacts.add_supplier')
    success_msg = 'Supplier created.'


class SupplierListView(FilterNameMixin, PermissionRequiredMixin, ListView):
    model = Supplier
    permission_required = ('contacts.view_supplier')


class SupplierUpdateView(
        PermissionRequiredMixin,
        ActionMessageViewMixin,
        UpdateView):
    model = Supplier
    form_class = SupplierModelForm
    template_name = 'contacts/supplier_update_form.html'
    permission_required = ('contacts.change_supplier')
    success_msg = 'Supplier updated.'

    def get_success_url(self):
        return reverse('contacts:suppliers_detail', args=[str(self.object.id)])


class SupplierDetailView(PermissionRequiredMixin, DetailView):
    model = Supplier
    permission_required = ('contacts.view_supplier')


class DownloadCVView(PermissionRequiredMixin, DownloadCVBaseView):
    model = Candidate
    permission_required = 'contacts.view_candidate'
