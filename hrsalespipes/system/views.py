from django.contrib.auth.views import LoginView as LiV


class LoginView(LiV):
    template_name = 'system/login.html'
    redirect_authenticated_user = True
