# Generated by Django 2.2.10 on 2020-03-25 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0019_auto_20200323_0224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='highest_educational_qualification',
            field=models.TextField(blank=True),
        ),
    ]