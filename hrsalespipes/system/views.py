from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView as LiV
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic.base import RedirectView


class LoginView(LiV):
    template_name = 'system/login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['errors'] = context['form'].errors
        return context

    def form_valid(self, form):
        msg = 'Successful login. Have a nice day!'
        messages.info(self.request, msg)
        return super().form_valid(form)

    def form_invalid(self, form):
        msg = 'Please enter a correct username and password. \
            Note that both fields may be case-sensitive.'
        messages.warning(self.request, msg)
        return super().form_invalid(form)


class HomeView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dashboard:index'))

        return render(request, 'system/home.html')


class AdminRedirectView(RedirectView):
    url = '/{}'.format(settings.ADMIN_URL)
    permanent = True
