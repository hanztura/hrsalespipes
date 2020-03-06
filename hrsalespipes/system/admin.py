from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Setting, VisaStatus, InterviewMode

# Register your models here
admin.site.register(User, UserAdmin)
admin.site.register(Setting)
admin.site.register(VisaStatus)
admin.site.register(InterviewMode)
