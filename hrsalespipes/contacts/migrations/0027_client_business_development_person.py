# Generated by Django 2.2.10 on 2020-04-06 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0026_auto_20200404_0407'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='business_development_person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contacts.Employee'),
        ),
    ]
