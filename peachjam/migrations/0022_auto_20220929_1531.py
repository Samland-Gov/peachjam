# Generated by Django 3.2.14 on 2022-09-29 15:31

import django.db.models.deletion
from django.db import migrations, models


def forwards(apps, _):
    judgment_model = apps.get_model("peachjam", "Judgment")
    old_court_detail = apps.get_model("liiweb", "CourtDetail")
    new_court_class = apps.get_model("peachjam", "CourtClass")
    new_court = apps.get_model("peachjam", "Court")

    for court in old_court_detail.objects.all():
        court_class, _ = new_court_class.objects.get_or_create(
            name=court.court_class.name
        )
        new_court.objects.create(
            name=court.court.name, code=court.court.code, court_class=court_class
        )

    for judgment in judgment_model.objects.all():
        court_code = judgment.author.code
        court = new_court.objects.get(code=court_code)
        judgment.court = court
        judgment.save()


class Migration(migrations.Migration):

    dependencies = [
        ("peachjam", "0021_auto_20220923_1111"),
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
            options={
                "verbose_name_plural": "Court classes",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Court",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("code", models.SlugField(max_length=255, unique=True)),
                (
                    "court_class",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="peachjam.courtclass",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="judgment",
            name="court",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="peachjam.court",
            ),
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
