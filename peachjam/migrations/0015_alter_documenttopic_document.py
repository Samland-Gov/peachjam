# Generated by Django 3.2.14 on 2022-08-18 13:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("peachjam", "0014_auto_20220810_1055"),
    ]

    operations = [
        migrations.AlterField(
            model_name="documenttopic",
            name="document",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="taxonomies",
                to="peachjam.coredocument",
            ),
        ),
    ]
