from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from .models import Job
from .rules import is_allowed_to_edit_close_job


class JobIsClosedMixin:
    job_pk_kwarg = 'pk'

    def get_job_pkwarg(self):
        return self.job_pk_kwarg

    def get_job_object(self):
        """Get the Job object.

        Override if not Job object.
        """
        job = self._kwargs[self.get_job_pkwarg()]
        job = get_object_or_404(Job, pk=job)

        return job

    def redirect_to_if_closed(self, job):
        """Redirect here. Override if needed"""
        return redirect(
            'jobs:detail', pk=str(job.pk)
        )

    def dispatch(self, request, *args, **kwargs):
        # check if status is closed and redirect to detail if yes
        self._kwargs = kwargs
        job = self.get_job_object()
        if not is_allowed_to_edit_close_job(request.user, job):
            msg = job.closed_job_msg
            messages.info(request, msg)

            return self.redirect_to_if_closed(job)

        return super().dispatch(request, *args, **kwargs)


class JobIsClosedContextMixin:

    def get_job_object(self):
        """Get the Job object.

        Override if not Job object.
        """
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        edit_not_allowed = not is_allowed_to_edit_close_job(
            self.request.user, self.get_job_object())

        context['edit_not_allowed'] = edit_not_allowed
        return context
