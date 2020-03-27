from django.urls import path

from .views import (
    CommissionCreateView, CommissionUpdateView, CommissionDetailView,
    CommissionListView, CommissionDeleteView)


app_name = 'commissions'
urlpatterns = [
    path('delete/<str:pk>/', CommissionDeleteView.as_view(), name='delete'),
    path('edit/<str:pk>/', CommissionUpdateView.as_view(), name='edit'),
    path('<str:pipeline_pk>/new/', CommissionCreateView.as_view(), name='new'),
    path('<str:pk>/', CommissionDetailView.as_view(), name='detail'),
    path('', CommissionListView.as_view(), name='list'),
]
