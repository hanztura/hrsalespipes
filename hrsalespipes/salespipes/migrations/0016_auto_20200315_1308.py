# Generated by Django 2.2.10 on 2020-03-15 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salespipes', '0015_pipeline_candidate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pipeline',
            name='candidate',
        ),
        migrations.AddField(
            model_name='pipeline',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]