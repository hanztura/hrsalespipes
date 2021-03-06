# Generated by Django 2.2.10 on 2020-03-06 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salespipes', '0004_auto_20200306_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pipeline',
            name='base_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='pipeline',
            name='invoice_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pipeline',
            name='potential_income',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='pipeline',
            name='recruitment_rate',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=2),
        ),
    ]
