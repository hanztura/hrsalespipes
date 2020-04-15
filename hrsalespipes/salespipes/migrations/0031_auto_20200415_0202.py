# Generated by Django 2.2.10 on 2020-04-15 02:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salespipes', '0030_historicalpipeline'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pipeline',
            options={'ordering': ['-date', '-job'], 'permissions': [('view_report_pipeline_summary', 'Can view report Pipeline Summary'), ('view_report_pipeline_details', 'Can view report Pipeline Details'), ('view_report_monthly_invoices_summary', 'Can view report Monthly Invoices Summary'), ('view_report_successful_jobs', 'Can view report on Successful Jobs'), ('view_all_pipelines', 'Can view all Pipeline records'), ('view_start_date_per_week_month', 'Can view Report on Start date per week/month')]},
        ),
    ]
