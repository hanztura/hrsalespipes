# Generated by Django 2.2.10 on 2020-03-19 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dashboard',
            options={'permissions': [('view_dashboard_type_three', 'Can view Dashboard Type Three'), ('view_dashboard_type_two', 'Can view Dashboard Type Two'), ('view_dashboard_type_one', 'Can view Dashboard Type One')]},
        ),
    ]