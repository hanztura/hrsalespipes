from django.urls import path

from .views import IndexView, PipelineSummaryListView, JobsSummaryListView

app_name = 'reports'
urlpatterns = [
    path(
        'pipeline-summary/',
        PipelineSummaryListView.as_view(),
        name='pipeline_summary'),
    path(
        'jobs-summary/',
        JobsSummaryListView.as_view(),
        name='jobs_summary'),
    path('', IndexView.as_view(), name='index'),
]
