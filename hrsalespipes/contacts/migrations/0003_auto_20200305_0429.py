# Generated by Django 2.2.10 on 2020-03-05 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_auto_20200211_0402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='current_previous_company',
            field=models.CharField(blank=True, max_length=200, verbose_name='company'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='current_previous_position',
            field=models.CharField(blank=True, max_length=200, verbose_name='position'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='current_previous_salary_and_benefits',
            field=models.TextField(blank=True, verbose_name='salary and benefits'),
        ),
    ]
