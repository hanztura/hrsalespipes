# Generated by Django 2.2.10 on 2020-03-14 08:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('commissions', '0007_commission_rate_role_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commission',
            name='id',
        ),
        migrations.AddField(
            model_name='commission',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
