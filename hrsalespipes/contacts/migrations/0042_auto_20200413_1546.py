# Generated by Django 2.2.10 on 2020-04-13 15:46

from django.db import migrations


def update_is_male_field(apps, schema_editor):
    Candidate = apps.get_model("contacts", "Candidate")
    db_alias = schema_editor.connection.alias

    # update males
    q = Candidate.objects.using(db_alias).filter(
        gender='Male')
    q.update(is_male=True)

    # update females
    q = Candidate.objects.using(db_alias).filter(
        gender='Female')
    q.update(is_male=False)


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0041_auto_20200413_1527'),
    ]

    operations = [
        migrations.RunPython(update_is_male_field)
    ]
