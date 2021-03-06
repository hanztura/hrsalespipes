# Generated by Django 2.2.10 on 2020-03-24 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0022_auto_20200320_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_job_open', models.BooleanField(default=True)),
                ('is_default', models.BooleanField(blank=True, default=False)),
                ('order', models.PositiveSmallIntegerField(default=1, help_text='Display order. 1 positioned at the top')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name': 'Job Candidate Status'},
        ),
        migrations.AddField(
            model_name='job',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='jobs.JobStatus'),
        ),
    ]
