# Generated by Django 2.2.10 on 2020-04-30 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0045_auto_20200430_0400'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='linked_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='historicalcandidate',
            name='linked_url',
            field=models.URLField(blank=True),
        ),
    ]
