# Generated by Django 2.2.10 on 2020-03-16 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0008_auto_20200315_1622'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidate',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ('name',)},
        ),
    ]