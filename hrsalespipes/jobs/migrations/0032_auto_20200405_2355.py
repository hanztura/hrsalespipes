# Generated by Django 2.2.10 on 2020-04-05 23:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0031_auto_20200330_0700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.localtime),
        ),
    ]
