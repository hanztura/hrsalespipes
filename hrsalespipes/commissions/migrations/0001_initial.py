# Generated by Django 2.2.10 on 2020-03-06 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('straight_rate', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_commission_individual', models.BooleanField(default=True)),
                ('rate', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='roles', to='commissions.Rate')),
            ],
        ),
        migrations.CreateModel(
            name='RateDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_minimum', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='minimum')),
                ('base_maximum', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='maximum')),
                ('rate_value_type', models.CharField(choices=[('amount', 'Amount'), ('percentage', 'Percentage')], max_length=50)),
                ('rate_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rate_record', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='details', to='commissions.Rate')),
            ],
        ),
    ]
