import json

from django.contrib import messages


def get_objects_as_choices(model):
    objects = model.objects.all()
    objects = [{'value': str(data.pk), 'text': data.name}
               for data in objects]
    objects = json.dumps(objects)

    return objects


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
