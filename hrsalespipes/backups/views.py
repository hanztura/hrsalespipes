import ntpath

from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView
from django.http import HttpResponse

from .models import Backup
from .utils import create_backup
from system.helpers import ActionMessageViewMixin
from system.utils import (
    PermissionRequiredWithCustomMessageMixin as PermissionRequiredMixin)


class BackupCreateView(
        PermissionRequiredMixin,
        ActionMessageViewMixin,
        CreateView):
    model = Backup
    permission_required = 'backups.add_backup'
    success_msg = 'Backup created.'
    fields = (
        'name',
    )

    def form_valid(self, form):
        """Set created by and backup file
        """
        form.instance.created_by = self.request.user

        # create backup file
        backup = create_backup()
        if backup:
            form.instance.backup = backup

        return super().form_valid(form)


class BackupListView(
        PermissionRequiredMixin,
        ListView):
    model = Backup
    permission_required = 'backups.view_backup'
    paginate_by = 25

    def get_queryset(self):
        q = super().get_queryset()
        q = q.select_related('created_by')
        return q


class BackupDownloadView(
        PermissionRequiredMixin,
        SingleObjectMixin,
        View):
    model = Backup
    permission_required = 'backups.download_backups'
    http_method_names = 'get',

    def get(self, request, *args, **kwargs):
        backup = self.get_object()
        with open(backup.backup, 'rb') as f:
            dispostion = 'attachment; filename={}'.format(
                ntpath.basename(backup.backup))

            response = HttpResponse(content=f)
            response['Content-Type'] = 'application/x-gzip'
            response['Content-Disposition'] = dispostion

        return response
