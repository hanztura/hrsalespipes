# Generated by Django 2.2.10 on 2020-03-23 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0016_candidate_cv_template'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candidate',
            old_name='bls_acls_validity',
            new_name='acls_validity',
        ),
        migrations.AddField(
            model_name='candidate',
            name='bls_validity',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='candidate',
            name='haad_dha_license_type',
            field=models.CharField(blank=True, choices=[('HAAD', 'HAAD'), ('DHA', 'DHA')], max_length=5),
        ),
    ]
