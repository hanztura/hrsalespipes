# Generated by Django 2.2.10 on 2020-03-19 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0009_auto_20200316_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='agreement_fee',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True),
        ),
    ]
