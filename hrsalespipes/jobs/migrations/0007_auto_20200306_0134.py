# Generated by Django 2.2.10 on 2020-03-06 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_auto_20200306_0133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobcandidate',
            name='actual_income',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Actual Income'),
        ),
    ]