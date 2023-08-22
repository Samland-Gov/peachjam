# Generated by Django 3.2.19 on 2023-08-16 10:46

from django.db import migrations, models

import peachjam.models.core_document_model


class Migration(migrations.Migration):

    dependencies = [
        ("peachjam", "0099_peachjamsettings_pocket_law_repo"),
    ]

    operations = [
        migrations.AddField(
            model_name="sourcefile",
            name="file_as_pdf",
            field=models.FileField(
                blank=True,
                max_length=1024,
                null=True,
                upload_to=peachjam.models.core_document_model.file_location,
                verbose_name="file as pdf",
            ),
        ),
    ]
