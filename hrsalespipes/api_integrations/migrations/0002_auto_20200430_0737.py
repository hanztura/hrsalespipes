# Generated by Django 2.2.10 on 2020-04-30 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_integrations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='linkedinapi',
            name='error',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='linkedinapi',
            name='error_description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='linkedinapi',
            name='state_is_used',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='linkedinapi',
            name='expires_in',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
