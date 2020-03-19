# Generated by Django 2.2.10 on 2020-03-19 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('view_dashboard_type_one', 'Can view Dashboard Type One'), ('view_dashboard_type_two', 'Can view Dashboard Type Two'), ('view_dashboard_type_three', 'Can view Dashboard Type Three')],
            },
        ),
    ]