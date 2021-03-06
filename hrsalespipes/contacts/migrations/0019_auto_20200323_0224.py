# Generated by Django 2.2.10 on 2020-03-23 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0018_auto_20200323_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='civil_status',
            field=models.CharField(blank=True, choices=[('Single', 'Single'), ('Married', 'Married'), ('Widowed', 'Widowed'), ('Divorced', 'Divorced'), ('Separated', 'Separated')], max_length=16),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=8),
        ),
    ]
