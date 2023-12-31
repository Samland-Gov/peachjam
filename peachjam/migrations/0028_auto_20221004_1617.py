# Generated by Django 3.2.15 on 2022-10-04 16:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("peachjam", "0027_backfill_polymorphic_content_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="AttachedFileNature",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=1024, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="AttachedFiles",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("filename", models.CharField(max_length=1024)),
                ("mimetype", models.CharField(max_length=1024)),
                ("size", models.BigIntegerField(default=0)),
                ("file", models.FileField(upload_to="")),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="peachjam.coredocument",
                    ),
                ),
                (
                    "nature",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="peachjam.attachedfilenature",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.DeleteModel(
            name="JudgmentMediaSummaryFile",
        ),
    ]
