# Generated by Django 2.2.10 on 2020-04-09 03:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0031_auto_20200408_0117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='business_development_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contacts.Employee'),
        ),
    ]