# Generated by Django 3.2.19 on 2023-06-30 12:42

import django.db.models.deletion
from django.db import migrations, models

import peachjam.models.core_document_model
import peachjam.storage


class Migration(migrations.Migration):

    dependencies = [
        ("peachjam", "0086_auto_20230629_1015"),
    ]

    operations = [
        migrations.AlterField(
            model_name="peachjamsettings",
            name="google_analytics_id",
            field=models.CharField(
                blank=True,
                help_text="Enter one or more Google Analytics IDs separated by spaces.",
                max_length=1024,
                null=True,
                verbose_name="google analytics id",
            ),
        ),
        migrations.CreateModel(
            name="ArticleAttachment",
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
                (
                    "filename",
                    models.CharField(max_length=1024, verbose_name="filename"),
                ),
                (
                    "mimetype",
                    models.CharField(max_length=1024, verbose_name="mimetype"),
                ),
                ("size", models.BigIntegerField(default=0, verbose_name="size")),
                (
                    "file",
                    peachjam.storage.DynamicStorageFileField(
                        max_length=1024,
                        upload_to=peachjam.models.core_document_model.file_location,
                        verbose_name="file",
                    ),
                ),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attachments",
                        to="peachjam.article",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
