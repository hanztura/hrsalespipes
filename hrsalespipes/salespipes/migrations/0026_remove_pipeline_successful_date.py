# Generated by Django 2.2.10 on 2020-03-28 05:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salespipes', '0025_auto_20200326_1916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pipeline',
            name='successful_date',
        ),
    ]