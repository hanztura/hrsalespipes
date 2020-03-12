from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import LoginView

app_name = 'system'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
