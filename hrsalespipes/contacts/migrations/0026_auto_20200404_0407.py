# Generated by Django 2.2.10 on 2020-04-04 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0025_client_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='supplier',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]