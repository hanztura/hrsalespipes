# Generated by Django 2.2.10 on 2020-03-22 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0012_candidate_driving_license'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candidate',
            old_name='current_previous_salary_and_benefits',
            new_name='current_previous_benefits',
        ),
        migrations.RenameField(
            model_name='candidate',
            old_name='expected_salary_and_benefits',
            new_name='expected_benefits',
        ),
        migrations.AddField(
            model_name='candidate',
            name='current_previous_salary',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='candidate',
            name='expected_salary',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
