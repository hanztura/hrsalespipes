# Generated by Django 2.2.10 on 2020-05-10 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_dashboard_sjpp_ytd_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboard',
            name='ytd_position_performance_label',
            field=models.CharField(blank=True, default='YTD Position Performance', max_length=100),
        ),
    ]