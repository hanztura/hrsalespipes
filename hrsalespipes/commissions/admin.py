from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .forms import RateModelForm
from .models import Rate, RateDetail, Commission


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


commission_fields = (
    'id',
    'date',
    'pipeline',
    'employee',
    'rate_role_type',
    'rate_used',
    'amount',
    'is_paid',
    'is_deleted',
)


class CommissionAdmin(SimpleHistoryAdmin):
    fields = commission_fields
    readonly_fields = commission_fields


admin.site.register(Rate, RateAdmin)
admin.site.register(Commission, CommissionAdmin)
