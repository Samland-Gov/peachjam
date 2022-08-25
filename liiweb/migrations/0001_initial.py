# Generated by Django 3.2.13 on 2022-07-25 19:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("peachjam", "0012_auto_20220725_1956"),
    ]

    operations = [
        migrations.CreateModel(
            name="CourtClass",
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
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="CourtDetail",
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
                    "court",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="peachjam.author",
                    ),
                ),
                (
                    "court_class",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="liiweb.courtclass",
                    ),
                ),
            ],
        ),
    ]
