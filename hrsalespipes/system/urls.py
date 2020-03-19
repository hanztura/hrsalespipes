from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import LoginView, HomeView, AdminRedirectView

app_name = 'system'
urlpatterns = [
    path('go-admin/', AdminRedirectView.as_view(), name='admin'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', HomeView.as_view(), name='home'),
]
