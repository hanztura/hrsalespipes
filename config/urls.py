"""hrsalespipes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from jobs.api import JobCandidateListAPIView


urlpatterns = [
    path(
        'api/job-candidates/',
        JobCandidateListAPIView.as_view(),
        name='api_job_candidates'),
    path('backups/', include('backups.urls')),
    path('contacts/', include('contacts.urls')),
    path('commissions/', include('commissions.urls')),
    path('jobs/', include('jobs.urls')),
    path('pipeline/', include('salespipes.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('reports/', include('reports.urls')),
    path('', include('system.urls')),

    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('grappelli/', include('grappelli.urls')),
    path(settings.ADMIN_URL, admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    from debug_toolbar import urls as debug_toolbar_urls

    urlpatterns += [
        path('__debug__/', include(debug_toolbar_urls))
    ]
