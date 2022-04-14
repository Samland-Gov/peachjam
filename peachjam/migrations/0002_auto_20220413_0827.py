# Generated by Django 3.2.12 on 2022-04-13 08:27

from django.db import migrations, models

import peachjam.models.core_document_model


class Migration(migrations.Migration):

    dependencies = [
        ("peachjam", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="file",
            field=models.ImageField(
                max_length=1024,
                upload_to=peachjam.models.core_document_model.file_location,
            ),
        ),
        migrations.AlterField(
            model_name="sourcefile",
            name="file",
            field=models.FileField(
                max_length=1024,
                upload_to=peachjam.models.core_document_model.file_location,
            ),
        ),
    ]
