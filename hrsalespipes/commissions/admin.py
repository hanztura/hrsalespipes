from django.contrib import admin

from .models import Rate, RateDetail, Role, EmployeeRole

admin.site.register(Rate)
admin.site.register(RateDetail)
admin.site.register(Role)
admin.site.register(EmployeeRole)
