from django.urls import path

from .views import JobCreateView, JobDetailView, JobListView, JobUpdateView


app_name = 'jobs'
urlpatterns = [
    path('new/', JobCreateView.as_view(), name='new'),
    path('edit/<str:pk>/', JobUpdateView.as_view(), name='edit'),
    path('<str:pk>/', JobDetailView.as_view(), name='detail'),

    path('', JobListView.as_view(), name='list'),
]
