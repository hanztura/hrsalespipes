from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView

from .models import Commission
from system.utils import PermissionRequiredWithCustomMessageMixin


class CommissionCreateView(
        PermissionRequiredWithCustomMessageMixin,
        CreateView):
    model = Commission
    permission_required = 'commissions.add_commission'


class CommissionUpdateView(
        PermissionRequiredWithCustomMessageMixin,
        UpdateView):
    model = Commission
    permission_required = 'commissions.change_commission'


class CommissionDetailView(
        PermissionRequiredWithCustomMessageMixin,
        DetailView):
    model = Commission
    permission_required = 'commissions.view_commission'


class CommissionListView(
        PermissionRequiredWithCustomMessageMixin,
        ListView):
    model = Commission
    permission_required = 'commissions.view_commission'

    def get_queryset(self, **kwargs):
        q = super().get_queryset(**kwargs)
        q = q.select_related('pipeline__job')

        return q
