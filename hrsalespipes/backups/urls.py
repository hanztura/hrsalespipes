from django.urls import path

from .views import BackupCreateView, BackupListView, BackupDownloadView


app_name = 'backups'
urlpatterns = [
    path('new/', BackupCreateView.as_view(), name='new'),
    path('download/<str:pk>/', BackupDownloadView.as_view(), name='download'),
    path('', BackupListView.as_view(), name='list'),
]
