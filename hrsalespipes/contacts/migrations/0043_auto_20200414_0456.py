# Generated by Django 2.2.10 on 2020-04-14 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0042_auto_20200413_1546'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='supplier',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='employee',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='candidate',
            unique_together={('name', 'email_address')},
        ),
        migrations.AlterUniqueTogether(
            name='client',
            unique_together={('name', 'email_address')},
        ),
        migrations.AlterUniqueTogether(
            name='employee',
            unique_together={('name', 'email_address')},
        ),
        migrations.AlterUniqueTogether(
            name='supplier',
            unique_together={('name', 'email_address')},
        ),
    ]