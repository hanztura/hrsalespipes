from django.urls import path

from .views import (
    PipelineCreateView, PipelineDetailView, PipelineListView,
    PipelineUpdateView)


app_name = 'salespipes'
urlpatterns = [
    path('new/', PipelineCreateView.as_view(), name='new'),
    path('edit/<str:pk>/', PipelineUpdateView.as_view(), name='edit'),
    path('<str:pk>/', PipelineDetailView.as_view(), name='detail'),
    path('', PipelineListView.as_view(), name='list'),
]
