# Generated by Django 2.2.10 on 2020-03-15 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0007_auto_20200311_0708'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='code',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='client',
            name='code',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='employee',
            name='code',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='supplier',
            name='code',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
