# Generated by Django 2.2.10 on 2020-03-20 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0010_auto_20200319_1412'),
        ('jobs', '0019_jobcandidate_consultant'),
    ]

    operations = [
        migrations.AddField(
            model_name='interview',
            name='done_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='interviews', to='contacts.Employee'),
        ),
    ]
