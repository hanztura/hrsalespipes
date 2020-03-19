from django.conf import settings
from django.contrib.auth.views import LoginView as LiV
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic.base import RedirectView


class LoginView(LiV):
    template_name = 'system/login.html'
    redirect_authenticated_user = True


class HomeView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dashboard:index'))

        return render(request, 'system/home.html')


class AdminRedirectView(RedirectView):
    url = '/{}'.format(settings.ADMIN_URL)
    permanent = True
