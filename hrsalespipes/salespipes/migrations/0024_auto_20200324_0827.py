# Generated by Django 2.2.10 on 2020-03-24 08:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('salespipes', '0023_auto_20200319_0743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pipeline',
            name='date',
            field=models.DateField(default=django.utils.timezone.localdate, verbose_name='Date'),
        ),
    ]
