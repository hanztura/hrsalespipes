# Generated by Django 2.2.10 on 2020-04-06 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0033_auto_20200406_0017'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='interview',
            options={'ordering': ['-date_time', 'job_candidate'], 'permissions': [('view_all_interviews', 'Can view all Interviews')]},
        ),
    ]
