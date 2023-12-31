# Generated by Django 3.2.15 on 2022-08-26 10:58

from django.db import migrations, models


def backfill_size(apps, schema_editor):
    for name in ["SourceFile", "Image"]:
        model = apps.get_model("peachjam", name)
        for obj in model.objects.all():
            obj.size = obj.file.size
            obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ("peachjam", "0015_alter_documenttopic_document"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="size",
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="sourcefile",
            name="size",
            field=models.BigIntegerField(default=0),
        ),
        migrations.RunPython(backfill_size, migrations.RunPython.noop),
    ]
