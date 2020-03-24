# Generated by Django 2.2.10 on 2020-03-24 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0025_auto_20200324_1148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ['-date', '-reference_number'], 'permissions': [('view_report_jobs_summary', 'Can view report Jobs Summary'), ('view_report_job_to_pipeline_analysis', 'Can view report Job to Pipeline Analysis'), ('can_edit_closed_job', 'Can edit closed Job')]},
        ),
    ]
