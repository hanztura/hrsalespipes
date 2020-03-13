from django.urls import path

from .views import (
    CandidateCreateView, CandidateUpdateView, CandidateDetailView,
    CandidateListView, ContactsTemplateView, ClientCreateView, ClientListView,
    ClientUpdateView, ClientDetailView, SupplierCreateView, SupplierDetailView,
    SupplierListView, SupplierUpdateView)

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

    path('clients/new/', ClientCreateView.as_view(), name='clients_new'),
    path('clients/edit/<str:pk>/', ClientUpdateView.as_view(),
         name='clients_edit'),
    path('clients/<str:pk>/', ClientDetailView.as_view(),
         name='clients_detail'),
    path('clients/', ClientListView.as_view(), name='clients_list'),

    path('suppliers/new/', SupplierCreateView.as_view(), name='suppliers_new'),
    path('suppliers/edit/<str:pk>/',
         SupplierUpdateView.as_view(), name='suppliers_edit'),
    path('suppliers/<str:pk>/',
         SupplierDetailView.as_view(), name='suppliers_detail'),
    path('suppliers/', SupplierListView.as_view(), name='suppliers_list'),

    path('', ContactsTemplateView.as_view(), name='index'),
]
