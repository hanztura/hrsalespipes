from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView

from .forms import CandidateCreateModelForm, CandidateUpdateModelForm
from .models import Candidate


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


class CandidateDetailView(DetailView):
    model = Candidate

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.select_related('visa_status', 'candidate_owner')
        return queryset
