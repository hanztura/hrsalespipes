# Generated by Django 2.2.10 on 2020-03-17 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salespipes', '0019_pipeline_job_candidate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pipeline',
            name='job',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='pipeline', to='jobs.Job'),
        ),
    ]
