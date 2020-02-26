import json

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView

from .forms import CandidateCreateModelForm, CandidateUpdateModelForm
from .models import Candidate
from system.models import VisaStatus


class CandidateCreateView(CreateView):
    model = Candidate
    form_class = CandidateCreateModelForm
    template_name = 'contacts/candidate_create_form.html'

    def form_valid(self, form):
        form.instance.candidate_owner = self.request.user
        return super().form_valid(form)


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

        context['visa_status_objects'] = visa_status_objects
        return context


class CandidateDetailView(DetailView):
    model = Candidate

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.select_related('visa_status', 'candidate_owner')
        return queryset
