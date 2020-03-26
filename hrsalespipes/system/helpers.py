import json

from django.conf import settings
from django.contrib import admin, messages


def get_objects_as_choices(model):
    objects = model.objects.all()
    objects = [{'value': str(data.pk), 'text': data.name}
               for data in objects]
    objects = json.dumps(objects)

    return objects


def register_optional_admin_items(items):
    enable_import_export = settings.ENABLE_IMPORT_EXPORT_IN_ADMIN

    if enable_import_export not in ['No', 'no', 'NO', False]:
        for model, admin_type in items:
            admin.site.register(model, admin_type)


class ActionMessageViewMixin:
    @property
    def success_msg(self):
        return '{} created/updated.'.format(self.model._meta.verbose_name)

    def form_valid(self, form):
        if form.is_valid():
            messages.info(self.request, self.success_msg)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
