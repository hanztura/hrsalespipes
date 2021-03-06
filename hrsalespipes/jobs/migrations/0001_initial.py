# Generated by Django 2.2.10 on 2020-02-10 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contacts', '0001_initial'),
        ('system', '0003_interviewmode'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reference_number', models.CharField(max_length=100, unique=True, verbose_name='Job Reference Number')),
                ('date', models.DateField(verbose_name='Job Reference Number')),
                ('position', models.CharField(max_length=100)),
                ('location', models.CharField(blank=True, max_length=64)),
                ('potential_income', models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='Potential Income')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contacts.Client')),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('probability', models.DecimalField(blank=True, decimal_places=2, max_digits=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobCandidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('registration_date', models.DateField()),
                ('cv_date_shared', models.DateField(blank=True)),
                ('remarks', models.TextField(blank=True)),
                ('salary_offered_currency', models.CharField(blank=True, max_length=3)),
                ('salary_offered', models.DecimalField(blank=True, decimal_places=2, max_digits=8)),
                ('tentative_date_of_joining', models.DateField(blank=True)),
                ('actual_income', models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='Actual Income')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='jobs', to='contacts.Candidate')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='candidates', to='jobs.Job')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jobs.Status')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('1', '1st'), ('2', '2nd'), ('A', 'Assessment'), ('F', 'Final')], max_length=1)),
                ('job_candidate', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='interviews', to='jobs.JobCandidate')),
                ('mode', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='system.InterviewMode')),
            ],
        ),
    ]
