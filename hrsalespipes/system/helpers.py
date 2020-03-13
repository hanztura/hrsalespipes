import json


def get_objects_as_choices(model):
    objects = model.objects.all()
    objects = [{'value': str(data.pk), 'text': data.name}
               for data in objects]
    objects = json.dumps(objects)

    return objects
