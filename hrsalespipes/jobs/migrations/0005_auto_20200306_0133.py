# Generated by Django 2.2.10 on 2020-03-06 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_auto_20200306_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobcandidate',
            name='salary_offered',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]
