# Generated by Django 2.2.10 on 2020-03-25 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backup',
            name='backup',
            field=models.FilePathField(editable=False, path='/home/hanz/projects/hrsalespipes/db/backups'),
        ),
    ]