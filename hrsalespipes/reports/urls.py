from django.urls import path

from .views import (
    IndexView, PipelineSummaryListView, JobsSummaryListView,
    JobsSummaryPDFView)

app_name = 'reports'
urlpatterns = [
    path(
        'pipeline-summary/',
        PipelineSummaryListView.as_view(),
        name='pipeline_summary'),
    path(
        'pdf/jobs-summary/',
        JobsSummaryPDFView.as_view(),
        name='pdf_jobs_summary'),
    path(
        'jobs-summary/',
        JobsSummaryListView.as_view(),
        name='jobs_summary'),
    path('', IndexView.as_view(), name='index'),
]
