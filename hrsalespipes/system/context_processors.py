from django.conf import settings

from .models import Setting


def get_icons(request):
    items = (
        ('ICON_DASHBOARD', 'mdi-view-dashboard-variant'),
        ('ICON_BACKUPS', 'mdi-database'),
        ('ICON_COMMISSIONS', 'mdi-calculator'),
        ('ICON_REPORTS', 'mdi-file-document'),
        ('ICON_PIPELINE', 'mdi-pipe'),
        ('ICON_JOBS', 'mdi-briefcase-search'),
        ('ICON_CONTACTS', 'mdi-contacts'),
        ('ICON_ACCOUNT', 'mdi-account-cirle'),
        ('ICON_CANDIDATES', 'mdi-account-tie'),
        ('ICON_CLIENTS', 'mdi-currency-usd'),
        ('ICON_SUPPLIERS', 'mdi-truck'),
    )
    icons = {}
    for key, default_value in items:
        icons[key] = getattr(settings, key, default_value)

    return icons


def get_app_label(request):
    setting = Setting.load()
    return {
        'PROJECT_LABEL': setting.get_project_label()
    }
