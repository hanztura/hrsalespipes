import os

from django.core.management.base import BaseCommand
from django.db import transaction

from system.models import Setting, Nationality


class Command(BaseCommand):
    help = 'Set up initial data for locations'

    @transaction.atomic
    def handle(self, *args, **options):
        # create Countries
        print('Setting up Nationalities')
        current_path = os.path.dirname(os.path.abspath(__file__))
        filename = 'data/nationalities.txt'
        filename = os.path.join(current_path, filename)
        with open(filename) as f:
            data = f.read().split('\n')

        created_count = 0
        for c in data:
            nationality, created = Nationality.objects.get_or_create(name=c)
            if created:
                msg = 'created nationality: {}'.format(c)
                print(msg)
                created_count += 1

        msg = 'created total of {} nationalities'.format(created_count)
        print(msg)

        if created_count:
            Setting.objects.update_or_create(
                id=1,
                defaults={'runned_nationalities_initial_data': True})
