# Generated by Django 2.2.10 on 2020-03-13 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0005_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='runned_locations_initial_data',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
