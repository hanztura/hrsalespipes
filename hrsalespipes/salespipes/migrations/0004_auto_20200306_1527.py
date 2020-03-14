# Generated by Django 2.2.10 on 2020-03-06 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salespipes', '0003_pipeline_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pipeline',
            name='invoice_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='pipeline',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='salespipes.Status'),
        ),
        migrations.AlterField(
            model_name='pipeline',
            name='vat',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10),
        ),
    ]