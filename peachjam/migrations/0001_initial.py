# Generated by Django 3.2.12 on 2022-04-08 07:29

import django.db.models.deletion
from django.db import migrations, models

import peachjam.models.core_document_model


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("countries_plus", "0005_auto_20160224_1804"),
        ("languages_plus", "0004_auto_20171214_0004"),
    ]

    operations = [
        migrations.CreateModel(
            name="CoreDocument",
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
                    "doc_type",
                    models.CharField(
                        choices=[
                            ("core_document", "Core Document"),
                            ("legislation", "Legislation"),
                            ("generic_document", "Generic Document"),
                            ("legal_instrument", "Legal Instrument"),
                            ("judgment", "Judgment"),
                        ],
                        default="core_document",
                        max_length=255,
                    ),
                ),
                ("title", models.CharField(max_length=1024)),
                ("date", models.DateField()),
                ("source_url", models.URLField(blank=True, max_length=2048, null=True)),
                ("citation", models.CharField(blank=True, max_length=1024, null=True)),
                ("content_html", models.TextField(blank=True, null=True)),
                ("expression_frbr_uri", models.CharField(max_length=1024, unique=True)),
                (
                    "work_frbr_uri",
                    models.CharField(blank=True, max_length=1024, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "jurisdiction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="countries_plus.country",
                    ),
                ),
                (
                    "language",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="languages_plus.language",
                    ),
                ),
            ],
            options={
                "ordering": ["doc_type", "title"],
            },
        ),
        migrations.CreateModel(
            name="SourceFile",
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
                (
                    "file",
                    models.FileField(
                        upload_to=peachjam.models.core_document_model.file_location
                    ),
                ),
                (
                    "document",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="source_file",
                        to="peachjam.coredocument",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Locality",
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
                ("name", models.CharField(max_length=255)),
                (
                    "jurisdiction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="countries_plus.country",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "localities",
                "ordering": ["name"],
                "unique_together": {("name", "jurisdiction")},
            },
        ),
        migrations.CreateModel(
            name="Image",
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
                (
                    "file",
                    models.ImageField(
                        upload_to=peachjam.models.core_document_model.file_location
                    ),
                ),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="images",
                        to="peachjam.coredocument",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="coredocument",
            name="locality",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="peachjam.locality",
            ),
        ),
    ]