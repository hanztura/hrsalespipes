import json
import uuid
import requests
from urllib.parse import urlencode, urlparse

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView, View
from django.views.generic.base import TemplateView

from .filters import CandidateFilter
from .forms import (ClientCreateModelForm,
                    CandidateUpdateModelForm, ClientUpdateModelForm,
                    SupplierModelForm, CandidateCreateModelForm,
                    SupplierUpdateModelForm)
from .models import Candidate, Client, Supplier, Employee, CVTemplate
from .utils import FilterNameMixin, DownloadCVBaseView
from api_integrations.models import LinkedinApi, CreateLinkedinProfile
from jobs.models import JobCandidate
from system.helpers import get_objects_as_choices, ActionMessageViewMixin
from system.utils import (
    PermissionRequiredWithCustomMessageMixin as PermissionRequiredMixin)
from system.models import VisaStatus, Location, Nationality, Industry, Setting


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
    populatable_fields = (
        'name', 'current_previous_position',
        'highest_educational_qualification', 'notes')

    def dispatch(self, request, *args, **kwargs):
        for f in self.populatable_fields:
            setattr(
                self,
                'q_{}'.format(f),
                request.GET.get(f, ''))
        return super().dispatch(request, *args, **kwargs)

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

        for f in self.populatable_fields:
            field_name = 'q_{}'.format(f)
            context[field_name] = getattr(self, field_name, '')
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

        candidate_as_dict = model_to_dict(candidate)
        candidate_as_dict['visa_status'] = getattr(
            candidate.visa_status, 'name', '')
        candidate_as_dict['candidate_owner'] = getattr(
            candidate.candidate_owner, 'name', '')
        candidate_as_dict['cv_template'] = getattr(
            candidate.cv_template, 'name', '')

        context['object_in_json'] = json.dumps(candidate_as_dict, default=str)
        context['url_download_cv'] = reverse_lazy(
            'contacts:download_cv',
            args=[candidate.pk])

        setting = Setting.load()
        context['cv_download_tooltip'] = 'Download {}'.format(
            setting.cv_label)
        return context


class CandidateListView(
        PermissionRequiredMixin,
        ListView):
    model = Candidate
    permission_required = ('contacts.view_candidate')
    paginate_by = 25

    def get_queryset(self, **kwargs):
        q = super().get_queryset(**kwargs)
        q = q.select_related('candidate_owner', 'visa_status')

        # set object attribute from query params
        # ( attribute_name, query_name )
        query_params = (
            ('owners', 'candidate_owner_id__in'),
            ('languages', 'languages'),
            ('nationalities', 'nationalities'),
            ('is_male', 'is_male'),
            ('age_range', 'age_range'),
            ('name', 'name__icontains'),

            ('positions', 'positions'),
            ('current_previous_company', 'current_previous_company__icontains'),
            ('visa_status', 'visa_status_id__in'),
            ('notice_period', 'notice_period'),
        )
        for param in query_params:
            name = param[0]
            value = self.request.GET.get(param[1], '')
            setattr(self, name, value)

        q = CandidateFilter(self.request.GET, q).qs
        return q

    def get_context_data(self):
        context = super().get_context_data()
        context['owners'] = get_objects_as_choices(Employee)
        context['owners_query'] = self.owners
        context['visa_status_choices'] = get_objects_as_choices(VisaStatus)
        context['visa_status_query'] = self.visa_status
        context['search_languages'] = self.languages
        context['search_nationalities'] = self.nationalities
        context['search_is_male'] = self.is_male
        context['search_age_range'] = self.age_range
        context['search_name'] = self.name
        context['search_positions'] = self.positions
        context['search_current_previous_company'] = self.current_previous_company
        context['search_notice_period'] = self.notice_period
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

    def get_queryset(self, **kwargs):
        q = super().get_queryset(**kwargs)
        q = q.select_related('business_development_person')

        self.bd_person = self.request.GET.get('bd_person', '')  # owner id
        if self.bd_person:
            q = q.filter(business_development_person_id=self.bd_person)

        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bd_person'] = self.bd_person
        context['employees'] = get_objects_as_choices(Employee)
        return context


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

        context['label_meeting_arranged'] = settings.CLIENTS_MEETING_ARRANGED
        context['label_notes'] = settings.CLIENTS_NOTES
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
    form_class = SupplierUpdateModelForm
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


class CandidateCreateLinkedinRedirectView(PermissionRequiredMixin, View):
    permission_required = ('contacts.add_candidate')

    def post(self, request, *args, **kwargs):
        profile_url = request.POST.get('profile_url', None)
        if profile_url:
            # check if user has access token
            user = request.user
            linkedin_transaction, created = CreateLinkedinProfile.objects.update_or_create(
                user=user, target_url=profile_url, defaults={
                    'user': user, 'target_url': profile_url
                })
            api_record, created = LinkedinApi.objects.get_or_create(
                user=user)

            if api_record.expired:
                # request authorization
                url = 'https://www.linkedin.com/oauth/v2/authorization?{}'
                redirect_uri = request.build_absolute_uri(str(
                    reverse_lazy('linkedin_authorization_redirect_uri')))

                api_record.state = str(uuid.uuid4())
                api_record.save()

                url = url.format(urlencode({
                    'response_type': 'code',
                    'client_id': settings.LINKEDIN_CLIENT_ID,
                    'redirect_uri': redirect_uri,
                    'state': api_record.state,
                    'scope': 'r_liteprofile'
                }))
                return HttpResponseRedirect(url)
                # return HttpResponse(url)

            else:
                # get profile
                person_id = urlparse(profile_url).path.split('/')[-2]
                url = 'https://api.linkedin.com/v2/people/{}'.format(person_id)
                print(url)
                headers = {
                    'Authorization': 'Bearer {}'.format(
                        api_record.access_token),
                    'X-RestLi-Protocol-Version': '2.0.0'
                }
                response = requests.get(url, headers=headers)
                print(response.json())
                return HttpResponse('do something')

        else:
            return HttpResponse('no linked url provided')


class LinkedInAuthorizationRedirect(PermissionRequiredMixin, View):
    permission_required = ('contacts.add_candidate')

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code', None)
        state = request.GET.get('state', None)
        api_record, created = LinkedinApi.objects.get_or_create(state=state)
        api_updates = {
            'state_is_used': True,
        }

        if code:
            # get access token if authorized
            url = 'https://www.linkedin.com/oauth/v2/accessToken'
            redirect_uri = request.build_absolute_uri(str(
                reverse_lazy('linkedin_authorization_redirect_uri')))
            response = requests.post(
                url,
                {
                    'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': redirect_uri,
                    'client_id': settings.LINKEDIN_CLIENT_ID,
                    'client_secret': settings.LINKEDIN_CLIENT_SECRET
                })
            data = response.json()
            access_token = data['access_token']
            expires_in = data['expires_in']
            api_updates['access_token'] = access_token
            api_updates['expires_in'] = expires_in

            # get user profile
        else:
            error = request.GET.get('error', True)
            error_description = request.GET.get('error_description', '')
            api_updates['error'] = error
            api_updates['error_description'] = error_description

        for attr, value in api_updates.items():
            setattr(api_record, attr, value)
        api_record.save()
        return HttpResponse('crate profile now') if code else HttpResponse('error')
