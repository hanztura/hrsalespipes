# Generated by Django 2.2.10 on 2020-02-10 11:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('system', '0002_visastatus'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('contact_number', models.CharField(blank=True, max_length=32)),
                ('alternate_contact_number', models.CharField(blank=True, max_length=32)),
                ('whatsapp_link', models.URLField(blank=True)),
                ('email_address', models.EmailField(blank=True, max_length=254)),
                ('skype_id', models.CharField(blank=True, max_length=50)),
                ('ms_teams_id', models.CharField(blank=True, max_length=200)),
                ('industry', models.CharField(max_length=64)),
                ('location', models.CharField(max_length=64)),
                ('initial_approach', models.TextField(blank=True)),
                ('meeting_arranged', models.TextField(blank=True)),
                ('agreement_terms', models.CharField(blank=True, max_length=200)),
                ('agreement_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=2, null=True)),
                ('refund_scheme', models.TextField(blank=True)),
                ('validity', models.DateField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('contact_number', models.CharField(blank=True, max_length=32)),
                ('alternate_contact_number', models.CharField(blank=True, max_length=32)),
                ('whatsapp_link', models.URLField(blank=True)),
                ('email_address', models.EmailField(blank=True, max_length=254)),
                ('skype_id', models.CharField(blank=True, max_length=50)),
                ('ms_teams_id', models.CharField(blank=True, max_length=200)),
                ('location', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('contact_number', models.CharField(blank=True, max_length=32)),
                ('alternate_contact_number', models.CharField(blank=True, max_length=32)),
                ('whatsapp_link', models.URLField(blank=True)),
                ('email_address', models.EmailField(blank=True, max_length=254)),
                ('skype_id', models.CharField(blank=True, max_length=50)),
                ('ms_teams_id', models.CharField(blank=True, max_length=200)),
                ('location', models.CharField(blank=True, max_length=64)),
                ('current_previous_position', models.CharField(blank=True, max_length=200)),
                ('current_previous_company', models.CharField(blank=True, max_length=200)),
                ('current_previous_salary_and_benefits', models.TextField(blank=True)),
                ('motivation_for_leaving', models.TextField(blank=True)),
                ('nationality', models.CharField(blank=True, max_length=64)),
                ('languages', models.TextField(blank=True, max_length=200)),
                ('preferred_location', models.CharField(blank=True, max_length=200)),
                ('civil_status', models.CharField(blank=True, choices=[('S', 'Single'), ('M', 'Married'), ('W', 'Widowed'), ('D', 'Divorced'), ('Se', 'Separated')], max_length=16)),
                ('dependents', models.TextField(blank=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=8)),
                ('highest_educational_qualification', models.CharField(blank=True, max_length=200)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('expected_salary_and_benefits', models.TextField(blank=True)),
                ('availability_for_interview', models.CharField(blank=True, max_length=200)),
                ('notice_period', models.CharField(blank=True, max_length=100)),
                ('notes', models.TextField(blank=True)),
                ('candidate_owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('visa_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.VisaStatus')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
