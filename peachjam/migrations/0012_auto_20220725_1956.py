# Generated by Django 3.2.13 on 2022-07-25 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("languages_plus", "0004_auto_20171214_0004"),
        ("countries_plus", "0005_auto_20160224_1804"),
        ("peachjam", "0011_frbr_uri_required_components"),
    ]

    operations = [
        migrations.AlterField(
            model_name="peachjamsettings",
            name="document_jurisdictions",
            field=models.ManyToManyField(
                blank=True,
                related_name="_peachjam_peachjamsettings_document_jurisdictions_+",
                to="countries_plus.Country",
            ),
        ),
        migrations.AlterField(
            model_name="peachjamsettings",
            name="document_languages",
            field=models.ManyToManyField(
                blank=True,
                related_name="_peachjam_peachjamsettings_document_languages_+",
                to="languages_plus.Language",
            ),
        ),
    ]
