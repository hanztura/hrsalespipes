# Generated by Django 2.2.10 on 2020-04-11 03:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0041_auto_20200410_0113'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobcandidate',
            options={'ordering': ['-registration_date', 'job', 'candidate__name'], 'permissions': [('view_all_job_candidates', 'Can view all Job Candidates'), ('view_report_cv_sent', 'Can view report CV Sent to clients')]},
        ),
    ]