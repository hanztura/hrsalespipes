# Generated by Django 2.2.10 on 2020-03-11 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0010_jobcandidate_associate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobcandidate',
            name='associate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='as_associate', to='contacts.Employee'),
        ),
    ]