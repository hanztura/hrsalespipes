# Generated by Django 2.2.10 on 2020-03-15 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0008_setting_vat_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='company_name',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]