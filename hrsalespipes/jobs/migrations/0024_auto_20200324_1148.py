# Generated by Django 2.2.10 on 2020-03-24 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0023_auto_20200324_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobstatus',
            name='order',
            field=models.PositiveSmallIntegerField(default=1, help_text='Display order. 1 positioned at the top', unique=True),
        ),
    ]
