# Generated by Django 3.2.13 on 2022-07-17 09:30
from cobalt import FrbrUri
from django.db import migrations


def backfill_components(apps, schema_editor):
    CoreDocument = apps.get_model("peachjam", "CoreDocument")
    for doc in CoreDocument.objects.all():
        frbr_uri = FrbrUri.parse(doc.work_frbr_uri)
        doc.frbr_uri_doctype = frbr_uri.doctype
        doc.frbr_uri_subtype = frbr_uri.subtype
        doc.frbr_uri_actor = frbr_uri.actor
        doc.frbr_uri_date = frbr_uri.date
        doc.frbr_uri_number = frbr_uri.number
        doc.save()


class Migration(migrations.Migration):

    dependencies = [("peachjam", "0009_frbr_uri_components")]

    operations = [
        migrations.RunPython(backfill_components, migrations.RunPython.noop),
    ]
