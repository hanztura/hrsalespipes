# Generated by Django 2.2.10 on 2020-03-13 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_auto_20200305_0429'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
    ]
