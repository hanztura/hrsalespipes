from django.urls import path

from .views import DashboardTemplateView, DashboardView

app_name = 'dashboard'
urlpatterns = [
    path('test/', DashboardView.as_view(), name='test'),
    path('', DashboardView.as_view(), name='index'),
]
