# Generated by Django 2.2.10 on 2020-03-15 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0014_remove_jobcandidate_actual_income'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Job Boards',
            },
        ),
        migrations.AddField(
            model_name='job',
            name='board',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='jobs.Board', verbose_name='Job Board'),
        ),
    ]