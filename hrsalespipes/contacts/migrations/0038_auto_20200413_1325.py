# Generated by Django 2.2.10 on 2020-04-13 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0037_auto_20200413_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='current_previous_salary',
            field=models.TextField(blank=True, null=True, verbose_name='current salary and benefits'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='expected_salary',
            field=models.TextField(blank=True, null=True, verbose_name='expected salary and benefits'),
        ),
        migrations.AlterField(
            model_name='historicalcandidate',
            name='current_previous_salary',
            field=models.TextField(blank=True, null=True, verbose_name='current salary and benefits'),
        ),
        migrations.AlterField(
            model_name='historicalcandidate',
            name='expected_salary',
            field=models.TextField(blank=True, null=True, verbose_name='expected salary and benefits'),
        ),
    ]
