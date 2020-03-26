# Generated by Django 2.2.10 on 2020-03-26 01:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0028_auto_20200326_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobcandidate',
            name='associate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='as_associate', to='contacts.Employee'),
        ),
        migrations.AlterField(
            model_name='jobcandidate',
            name='consultant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='as_consultant', to='contacts.Employee'),
        ),
    ]