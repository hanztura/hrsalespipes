# Generated by Django 2.2.10 on 2020-03-06 08:22

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobs', '0008_auto_20200306_0148'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('probability', models.DecimalField(decimal_places=2, max_digits=2)),
            ],
        ),
        migrations.CreateModel(
            name='Pipeline',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField(verbose_name='Date')),
                ('invoice_date', models.DateField(blank=True)),
                ('recruitment_term', models.CharField(blank=True, max_length=100)),
                ('recruitment_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=2)),
                ('base_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('potential_income', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('invoice_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('vat', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('job_candidate', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jobs.JobCandidate')),
                ('status', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='salespipes.Status')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
