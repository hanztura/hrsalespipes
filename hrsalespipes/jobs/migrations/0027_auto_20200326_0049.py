# Generated by Django 2.2.10 on 2020-03-26 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0026_auto_20200324_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='reference_number',
            field=models.CharField(max_length=100, verbose_name='Job Reference Number'),
        ),
    ]
