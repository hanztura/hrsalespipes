# Generated by Django 2.2.10 on 2020-03-12 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commissions', '0006_auto_20200312_0245'),
    ]

    operations = [
        migrations.AddField(
            model_name='commission',
            name='rate_role_type',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
