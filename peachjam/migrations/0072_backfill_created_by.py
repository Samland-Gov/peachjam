# Generated by Django 3.2.16 on 2023-05-05 15:27

from django.contrib.admin.models import ADDITION
from django.db import migrations


def forwards(apps, schema_editor):
    CoreDocument = apps.get_model("peachjam", "CoreDocument")
    LogEntry = apps.get_model("admin", "LogEntry")

    for doc in (
        CoreDocument.objects.filter(created_by=None)
        .prefetch_related("polymorphic_ctype")
        .only("polymorphic_ctype", "pk")
        .all()
        .iterator()
    ):
        # get the log entry for this document
        log = (
            LogEntry.objects.filter(
                content_type=doc.polymorphic_ctype,
                object_id=doc.pk,
                action_flag=ADDITION,
            )
            .order_by("action_time")
            .first()
        )
        if log:
            doc.created_by = log.user
            doc.save(update_fields=["created_by"])


class Migration(migrations.Migration):

    dependencies = [
        ("peachjam", "0071_coredocument_created_by"),
    ]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
