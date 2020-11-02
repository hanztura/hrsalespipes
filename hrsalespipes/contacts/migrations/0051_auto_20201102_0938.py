# Generated by Django 2.2.13 on 2020-11-02 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0050_employee_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='haad_dha_license_type',
            field=models.CharField(blank=True, choices=[('HAAD', 'HAAD'), ('DHA', 'DHA'), ('SCHS', 'SCHS')], max_length=5),
        ),
        migrations.AlterField(
            model_name='historicalcandidate',
            name='haad_dha_license_type',
            field=models.CharField(blank=True, choices=[('HAAD', 'HAAD'), ('DHA', 'DHA'), ('SCHS', 'SCHS')], max_length=5),
        ),
    ]
