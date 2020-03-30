import random

from django.core.management.base import BaseCommand
from django.db import transaction

from faker import Faker
from faker.providers import internet, phone_number, python, lorem

from contacts.forms import (
    CandidateCreateModelForm, CandidateUpdateModelForm)
from contacts.models import Employee, Client, Supplier, Candidate, CVTemplate
from jobs.forms import (
    JobCreateModelForm, JobUpdateModelForm, JobCandidateCreateModelForm,
    JobCandidateUpdateModelForm)
from jobs.models import Status as JobCandidateStatus
from system.models import (
    User, Industry, Location, Nationality, VisaStatus)


class Command(BaseCommand):
    help = 'Set up initial data for locations'

    @transaction.atomic
    def handle(self, *args, **options):
        faker = Faker()

        providers = [
            internet, phone_number, python, lorem]
        for provider in providers:
            faker.add_provider(provider)

        # create users
        objects_to_create = int(
            input('Number of users & employees to create: '))
        default_password = 'hrsalespipes'
        objects_created = []
        users_created_profile = []
        for i in range(objects_to_create):
            user_profile = faker.simple_profile()
            user = User.objects.create_user(
                username=user_profile['username'],
                password=default_password,
                email=user_profile['mail'],
                first_name=user_profile['name'])
            objects_created.append(user)
            users_created_profile.append(user_profile)

        msg = '{} created: {}'.format('Users', len(objects_created))
        print(msg)  

        # create employees based on users created
        employees_created = []
        for i, user in enumerate(objects_created):
            address = users_created_profile[i]['address']
            employee = Employee.objects.create(
                name=user.first_name,
                user=user,
                location=address,
                email_address=user.email,
                contact_number=faker.phone_number())
            employees_created.append(employee)

        msg = '{} created: {}'.format('Employees', len(employees_created))
        print(msg)

        # create clients
        objects_to_create = int(input('Number of clients to create: '))
        objects_created = []
        industries = tuple(Industry.objects.values_list('name', flat=True))
        for i in range(objects_to_create):
            profile = faker.simple_profile()
            industry = random.sample(industries, 1)[0]
            client = Client.objects.create(
                name=profile['name'],
                contact_number=faker.phone_number(),
                email_address=profile['mail'],
                industry=industry)
            objects_created.append(client)

        msg = '{} created: {}'.format('Clients', len(objects_created))
        print(msg)

        # create suppliers
        objects_created = []
        names = ['LinkedIn', 'Zoho', 'Jobstreet']
        for name in names:
            profile = faker.simple_profile()
            supplier, created = Supplier.objects.update_or_create(
                name=name,
                defaults={
                    'contact_number': faker.phone_number(),
                    'email_address': profile['mail']
                })
            if created:
                objects_created.append(supplier)

        msg = '{} created: {}'.format('Suppliers', len(objects_created))
        print(msg)

        # create candidates
        objects_to_create = int(
            input('Number of candidates to create: '))
        objects_created = []

        locations = list(Location.objects.values_list('name', flat=True))
        nationalities = list(
            Nationality.objects.values_list('name', flat=True))
        civil_statuses = Candidate.CIVIL_STATUS_CHOICES
        visas = list(
            VisaStatus.objects.values_list('id', flat=True))
        employees = list(Employee.objects.all())  # objects
        users = list(User.objects.all())  # objects
        templates = list(
            CVTemplate.objects.values_list('id', flat=True))

        for i in range(objects_to_create):
            profile = faker.profile(sex=['Male', 'Female'])
            data = {
                'name': profile['name'],
                'contact_number': faker.phone_number(),
                'alternate_contact_number': faker.phone_number(),
                'email_address': profile['mail'],
                'location': random.sample(locations, 1)[0],
            }
            form = CandidateCreateModelForm(
                data, user=random.sample(users, 1)[0])

            if form.is_valid():
                form.save()
                objects_created.append(form.instance)

                candidate_owner = str(random.sample(employees, 1)[0].pk)
                template = str(random.sample(templates, 1)[0])
                sex = 'Male' if profile['sex'] == 'M' else 'Female'

                # update with other details
                current_salary = faker.pyint(
                    min_value=10000, max_value=100000, step=1000)
                expected_salary = faker.pyint(
                    min_value=current_salary, max_value=200000, step=1000)
                motivation = faker.sentence(
                    nb_words=10, variable_nb_words=True, ext_word_list=None)
                note = faker.sentence(
                    nb_words=10, variable_nb_words=True, ext_word_list=None)
                data = {
                    'name': data['name'],
                    'contact_number': data['contact_number'],
                    'alternate_contact_number':
                        data['alternate_contact_number'],
                    'email_address': data['email_address'],
                    'location': data['location'],
                    'current_previous_position': profile['job'],
                    'current_previous_company': profile['company'],
                    'current_previous_salary': current_salary,
                    'current_previous_benefits': '',
                    'motivation_for_leaving': motivation,
                    'expected_salary': expected_salary,
                    'expected_benefits': '',

                    'nationality': random.sample(nationalities, 1)[0],
                    'civil_status': random.sample(civil_statuses, 1)[0][0],
                    'dependents': '',
                    'gender': sex,
                    'date_of_birth': profile['birthdate'],

                    'visa_status': str(random.sample(visas, 1)[0]),
                    'candidate_owner': candidate_owner,
                    'cv_template': template,
                    'notes': note,
                }
                form = CandidateUpdateModelForm(data, instance=form.instance)

                if form.is_valid():  # udpate form
                    form.save()
                else:
                    print(form.errors)

        msg = '{} created: {}'.format('Candidates', len(objects_created))
        print(msg)

        # delete not needed variables
        delete_variables = (
            nationalities,
            civil_statuses,
            visas,
            templates,
            candidate_owner,
            template,
            sex,
            current_salary,
            expected_salary,
            motivation,
            users,
            note,
            data,
            form
        )
        for i in delete_variables:
            del(i)

        # create job records
        objects_to_create = int(
            input('Number of jobs to create: '))
        min_job_candidats = int(
            input('Minimum number of Job Candidates: '))
        max_job_candidats = int(
            input('Max number of Job Candidates: '))
        objects_created = []
        job_candidates_created = []
        clients = list(Client.objects.values_list('id', flat=True))
        candidates = list(Candidate.objects.values_list('id', flat=True))
        suppliers = list(Supplier.objects.values_list('name', flat=True))
        job_candidate_statuses = list(
            JobCandidateStatus.objects.values_list('id', flat=True))
        for i in range(objects_to_create):
            data = {
                'reference_number': faker.numerify(text='JOB-####'),
                'client': str(random.sample(clients, 1)[0]),
                'position': faker.job(),
            }
            form = JobCreateModelForm(data)

            if form.is_valid():
                job = form.save()
                objects_created.append(job)

                data = {
                    'reference_number': job.reference_number,
                    'date': job.date,
                    'client': job.client_id,
                    'position': job.position,
                    'location': random.sample(locations, 1)[0],
                    'potential_income': faker.pyint(
                        min_value=5000, max_value=20000, step=100),
                    'status': job.status_id,
                }

                # update job
                form = JobUpdateModelForm(data, instance=job, request=None)
                if form.is_valid():
                    job = form.save()

                # create job candidates
                random_number_of_job_candidates = random.randint(
                    min_job_candidats, max_job_candidats)

                for i in range(random_number_of_job_candidates):
                    # create a job candidate
                    data = {
                        'candidate': str(random.sample(candidates, 1)[0])
                    }
                    employee = random.sample(employees, 1)[0]  # instance
                    job_candidate_form = JobCandidateCreateModelForm(
                        data, job=job, employee=employee, request=None)

                    if job_candidate_form.is_valid():
                        job_candidate = job_candidate_form.save()
                        job_candidates_created.append(job_candidate)

                        # instance
                        consultant = str(random.sample(employees, 1)[0].pk)

                        # update job candidate
                        data = {
                            'candidate': job_candidate.candidate_id,
                            'registration_date': str(
                                job_candidate.registration_date),
                            'status': str(
                                random.sample(job_candidate_statuses, 1)[0]),
                            'cv_source': random.sample(suppliers, 1)[0],
                            'cv_date_shared': str(
                                job_candidate.registration_date),
                            'remarks': '',
                            'salary_offered_currency': '',
                            'salary_offered': faker.pyint(
                                min_value=20000, max_value=300000, step=1000),
                            'tentative_date_of_joining': '',
                            'associate': str(job_candidate.associate_id),
                            'consultant': consultant,
                        }
                        job_candidate_form = JobCandidateUpdateModelForm(
                            data, instance=job_candidate, request=None)

                        if job_candidate_form.is_valid():
                            job_candidate = job_candidate_form.save()
                        else:
                            print(job_candidate_form.errors)
            else:
                print(form.errors)

        msg = '{} created: {}'.format('Jobs', len(objects_created))
        print(msg)

        msg = '{} created: {}'.format(
            'Job Candidates', len(job_candidates_created))
        print(msg)
