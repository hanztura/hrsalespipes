# Generated by Django 2.2.10 on 2020-03-06 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_auto_20200306_0148'),
        ('salespipes', '0002_remove_pipeline_job_candidate'),
    ]

    operations = [
        migrations.AddField(
            model_name='pipeline',
            name='job',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='pipeline', to='jobs.Job'),
            preserve_default=False,
        ),
    ]
