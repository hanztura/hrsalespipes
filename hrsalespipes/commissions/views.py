import datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView

from .models import Commission
from contacts.models import Employee
from salespipes.models import Pipeline
from system.helpers import get_objects_as_choices, ActionMessageViewMixin
from system.utils import PermissionRequiredWithCustomMessageMixin


class CommissionCreateView(
        PermissionRequiredWithCustomMessageMixin,
        ActionMessageViewMixin,
        CreateView):
    model = Commission
    permission_required = 'commissions.add_commission'
    fields = [
        'employee',
        'rate_role_type',
        'rate_used',
        'amount',
    ]
    success_msg = 'Commission created.'

    def form_valid(self, form):
        pipeline = self.kwargs['pipeline_pk']
        pipeline = get_object_or_404(Pipeline, pk=pipeline)

        form.instance.pipeline = pipeline
        form.instance.date = datetime.date.today()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['mode'] = 'New'
        context['employees'] = get_objects_as_choices(Employee)
        return context


class CommissionUpdateView(
        PermissionRequiredWithCustomMessageMixin,
        ActionMessageViewMixin,
        UpdateView):
    model = Commission
    permission_required = 'commissions.change_commission'
    fields = [
        'date',
        'employee',
        'rate_role_type',
        'rate_used',
        'amount',
        'is_paid',
    ]
    template_name = 'commissions/commission_update_form.html'
    success_msg = 'Commission updated.'

    def get_queryset(self):
        q = super().get_queryset()
        q = q.select_related('pipeline__job', 'employee')

        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object.is_paid:
            is_paid = 'true'
        else:
            is_paid = 'false'

        context['is_paid'] = is_paid
        context['mode'] = 'Edit'
        context['employees'] = get_objects_as_choices(Employee)
        return context

    def get_success_url(self):
        return reverse('commissions:detail', args=[str(self.object.id)])


class CommissionDetailView(
        PermissionRequiredWithCustomMessageMixin,
        DetailView):
    model = Commission
    permission_required = 'commissions.view_commission'

    def get_queryset(self, **kwargs):
        q = super().get_queryset(**kwargs)
        q = q.select_related(
            'pipeline__job_candidate__job',
            'pipeline__job_candidate__candidate',
            'employee')

        return q


class CommissionListView(
        PermissionRequiredWithCustomMessageMixin,
        ListView):
    model = Commission
    permission_required = 'commissions.view_commission'
    paginate_by = 25

    def get_queryset(self, **kwargs):
        q = super().get_queryset(**kwargs)
        q = q.select_related(
            'pipeline__job_candidate__job',
            'pipeline__job_candidate__candidate',
            'employee')

        search_q = self.request.GET.get('q', '')
        if search_q:
            q = q.filter(
                Q(pipeline__job_candidate__job__reference_number__icontains=search_q) | \
                Q(employee__name__icontains=search_q))
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_q = self.request.GET.get('q', '')
        context['search_q'] = search_q
        return context
