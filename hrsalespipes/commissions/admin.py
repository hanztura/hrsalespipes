from django.contrib import admin

from .forms import RateModelForm
from .models import Rate, RateDetail


class RateDetailInline(admin.TabularInline):
    model = RateDetail
    extra = 1


class RateAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'straight_rate',
        'role_type',
    ]
    form = RateModelForm
    inlines = [RateDetailInline]


admin.site.register(Rate, RateAdmin)
