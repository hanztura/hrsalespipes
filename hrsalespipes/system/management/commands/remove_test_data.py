import random

from django.core.management.base import BaseCommand
from django.db import transaction

from commissions.models import Commission
from contacts.models import Employee, Client, Supplier, Candidate
from salespipes.models import Pipeline
from jobs.models import JobCandidate, Job


class Command(BaseCommand):
    help = 'Set up initial data for locations'

    @transaction.atomic
    def handle(self, *args, **options):
        querysets = [
            Commission.base_objects.all(),
            Pipeline.objects.all(),
            JobCandidate.objects.all(),
            Job.objects.all(),
            Candidate.objects.all(),
            Supplier.objects.all(),
            Client.objects.all(),
            Employee.objects.all()
        ]
        for q in querysets:
            print(q.delete())
