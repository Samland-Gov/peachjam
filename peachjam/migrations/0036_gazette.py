# Generated by Django 3.2.16 on 2022-11-14 11:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("peachjam", "0035_judgment_field_nulls"),
    ]

    operations = [
        migrations.CreateModel(
            name="Gazette",
            fields=[
                (
                    "coredocument_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="peachjam.coredocument",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            bases=("peachjam.coredocument",),
        ),
    ]
