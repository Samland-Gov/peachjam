# Generated by Django 3.2.15 on 2022-10-27 13:30

from django.conf import settings
from django.db import connection, migrations
from django.db.models import F, Value
from django.db.models.functions import Concat, Substr


def add_s3_bucket(apps, schema_editor):
    """add s3:bucket: to stored files"""
    if getattr(settings, "DYNAMIC_STORAGE") and getattr(
        settings, "AWS_STORAGE_BUCKET_NAME"
    ):
        bucket = settings.AWS_STORAGE_BUCKET_NAME

        for model_name in ["SourceFile", "AttachedFiles"]:
            model = apps.get_model("peachjam", model_name)
            model.objects.exclude(file__startswith="s3:").update(
                file=Concat(Value(f"s3:{bucket}:"), F("file"))
            )


def remove_s3_bucket(apps, schema_editor):
    """strip the s3:bucket: from stored files"""
    for model_name in ["SourceFile", "AttachedFiles"]:
        model = apps.get_model("peachjam", model_name)

        with connection.cursor() as cursor:
            cursor.execute(
                f"""
UPDATE {model._meta.db_table}
SET file = SUBSTRING(file FROM 4 + POSITION(':' IN SUBSTRING(file FROM 4)))
WHERE file like 's3:%'
"""
            )


class Migration(migrations.Migration):
    dependencies = [
        ("peachjam", "0030_attachement_location"),
    ]

    operations = [migrations.RunPython(add_s3_bucket, remove_s3_bucket)]
