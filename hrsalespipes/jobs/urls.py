from django.urls import path

from .views import (JobCreateView, JobDetailView, JobListView, JobUpdateView,
                    JobCandidateUpdateView, JobCandidateCreateView,
                    JobCandidateDetailView, InterviewCreateView,
                    InterviewUpdateView)


app_name = 'jobs'
urlpatterns = [
    path('new/', JobCreateView.as_view(), name='new'),
    path('edit/<str:pk>/', JobUpdateView.as_view(), name='edit'),

    path('<str:job_pk>/candidates/new/',
         JobCandidateCreateView.as_view(), name='candidates_new'),
    path('<str:job_pk>/candidates/edit/<str:pk>/',
         JobCandidateUpdateView.as_view(), name='candidates_edit'),
    path('<str:job_pk>/candidates/<str:pk>/',
         JobCandidateDetailView.as_view(), name='candidates_detail'),

    path('<str:job_pk>/candidates/<str:candidate_pk>/interviews/new/',
         InterviewCreateView.as_view(), name='interviews_new'),
    path('<str:job_pk>/candidates/<str:candidate_pk>/interviews/edit/<str:pk>/',
         InterviewUpdateView.as_view(), name='interviews_edit'),

    path('<str:pk>/', JobDetailView.as_view(), name='detail'),


    path('', JobListView.as_view(), name='list'),
]
