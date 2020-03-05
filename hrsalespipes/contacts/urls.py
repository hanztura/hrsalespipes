from django.urls import path

from .views import (
    CandidateCreateView, CandidateUpdateView, CandidateDetailView,
    CandidateListView, ContactsTemplatView)

app_name = 'contacts'
urlpatterns = [
    path(
        'candidates/new/',
        CandidateCreateView.as_view(), name='candidates_new'),
    path('candidates/edit/<str:pk>/',
         CandidateUpdateView.as_view(), name='candidates_edit'),
    path('candidates/<str:pk>/', CandidateDetailView.as_view(),
         name='candidates_detail'),
    path('candidates/', CandidateListView.as_view(), name='candidates_list'),

    path('', ContactsTemplatView.as_view(), name='index'),
]
