# Generated by Django 2.2.10 on 2020-04-06 22:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields
import simple_history.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0036_historicaljob_historicaljobcandidate'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('salespipes', '0029_auto_20200330_0700'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalPipeline',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('date', models.DateField(default=django.utils.timezone.localdate, verbose_name='Date')),
                ('recruitment_term', models.DecimalField(blank=True, decimal_places=5, default=1.0, max_digits=15)),
                ('recruitment_rate', models.DecimalField(blank=True, decimal_places=10, default=0.0, max_digits=11)),
                ('base_amount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('potential_income', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('invoice_date', models.DateField(blank=True, null=True)),
                ('invoice_number', models.CharField(blank=True, max_length=50)),
                ('invoice_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10)),
                ('vat', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('job', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='jobs.Job')),
                ('job_candidate', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='jobs.JobCandidate')),
                ('status', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='salespipes.Status')),
            ],
            options={
                'verbose_name': 'historical pipeline',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
