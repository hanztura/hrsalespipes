# Generated by Django 2.2.10 on 2020-04-11 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0018_auto_20200403_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='newly_signed_clients_number_of_days',
            field=models.PositiveSmallIntegerField(default=7),
        ),
    ]
