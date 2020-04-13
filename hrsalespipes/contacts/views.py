from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, Q
from django.urls import reverse
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView

from .forms import (ClientCreateModelForm,
                    CandidateUpdateModelForm, ClientUpdateModelForm,
                    SupplierModelForm, CandidateCreateModelForm)
from .models import Candidate, Client, Supplier, Employee, CVTemplate
from .utils import FilterNameMixin, DownloadCVBaseView
from jobs.models import JobCandidate
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
        return self.object.edit_href


class CandidateDetailView(PermissionRequiredMixin, DetailView):
    model = Candidate
    permission_required = ('contacts.view_candidate')

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.select_related(
            'visa_status', 'candidate_owner', 'cv_template')
        queryset = queryset.prefetch_related(Prefetch(
            'jobs',
            queryset=JobCandidate.objects.filter(
                job__status__is_job_open=True).select_related(
                    'candidate', 'status', 'associate', 'consultant', 'job')
        ))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        candidate = context['object']
        context['active_jobs'] = candidate.jobs.all()
        return context


class CandidateListView(
        FilterNameMixin,
        PermissionRequiredMixin,
        ListView):
    model = Candidate
    permission_required = ('contacts.view_candidate')

    def get_queryset(self, **kwargs):
        q = super().get_queryset(**kwargs)
        q = q.select_related('candidate_owner')

        owners = self.request.GET.get('owners', '')  # owner id
        self.owners = owners
        owners = owners.split(',') if owners else []
        if owners:
            q = q.filter(candidate_owner_id__in=owners)

        # filter one or more languages
        languages = self.request.GET.get('languages', '')
        self.languages = languages
        languages = languages.split(',') if languages else []
        if languages:
            # multiple or expressions
            filter_expression = Q()
            for language in languages:
                filter_expression |= Q(languages__icontains=language.strip())

            q = q.filter(filter_expression)

        # filter one or more nationalities
        nationalities = self.request.GET.get('nationalities', '')
        self.nationalities = nationalities
        nationalities = nationalities.split(',') if nationalities else []
        if nationalities:
            # multiple or expressions
            filter_expression = Q()
            for nationality in nationalities:
                filter_expression |= Q(
                    nationality__icontains=nationality.strip())

            q = q.filter(filter_expression)

        # filter is_male
        is_male = self.request.GET.get('is_male', '')
        self.is_male = is_male
        is_male = is_male.split(',') if is_male else []
        if is_male:
            # multiple or expressions
            filter_expression = Q()
            possible_values = {
                'None': None,
                'true': True,
                'false': False
            }
            for value in is_male:
                filter_expression |= Q(
                    is_male=possible_values[value])

            q = q.filter(filter_expression)

        # filter age range
        age_range = self.request.GET.get('age_range', '')
        self.age_range = age_range
        age_range = age_range.split(',') if age_range else []
        if age_range:
            today = timezone.localdate()
            oldest_year = today.year - int(age_range[1])  # oldest
            youngest_year = today.year - int(age_range[0])  # youngest
            oldest_dob = today.replace(day=1, month=1, year=oldest_year)
            youngest_dob = today.replace(day=31, month=12, year=youngest_year)
            q = q.filter(
                date_of_birth__range=(oldest_dob, youngest_dob))

        return q

    def get_context_data(self):
        context = super().get_context_data()
        context['owners'] = get_objects_as_choices(Employee)
        context['owners_query'] = self.owners
        context['search_languages'] = self.languages
        context['search_nationalities'] = self.nationalities
        context['search_is_male'] = self.is_male
        context['search_age_range'] = self.age_range
        return context


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
        context['locations'] = get_objects_as_choices(Location)
        context['industries'] = get_objects_as_choices(Industry)
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['locations'] = get_objects_as_choices(Location)
        context['industries'] = get_objects_as_choices(Industry)
        context['employees'] = get_objects_as_choices(Employee)
        return context

    def get_success_url(self):
        return reverse('contacts:clients_detail', args=[str(self.object.id)])


class ClientDetailView(PermissionRequiredMixin, DetailView):
    model = Client
    permission_required = ('contacts.view_client')

    def get_queryset(self):
        q = super().get_queryset()
        q = q.select_related('business_development_person')
        return q


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
