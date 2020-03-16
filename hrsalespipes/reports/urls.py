from django.urls import path

from .views import IndexView, PipelineSummaryListView

app_name = 'reports'
urlpatterns = [
    path(
        'pipeline-summary/',
        PipelineSummaryListView.as_view(),
        name='pipeline_summary'),
    path('', IndexView.as_view(), name='index'),
]
