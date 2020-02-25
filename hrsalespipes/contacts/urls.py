from django.urls import path

from .views import CandidateCreateView, CandidateUpdateView

app_name = 'contacts'
urlpatterns = [
    path(
        'candidates/new/',
        CandidateCreateView.as_view(), name='candidates_new'),
    path('candidates/edit/<str:pk>/',
         CandidateUpdateView.as_view(), name='candidates_edit')
]
