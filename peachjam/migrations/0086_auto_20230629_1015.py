# Generated by Django 3.2.19 on 2023-06-29 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("peachjam", "0085_citations_processing"),
    ]

    operations = [
        migrations.AddField(
            model_name="peachjamsettings",
            name="facebook_link",
            field=models.URLField(blank=True, null=True, verbose_name="facebook link"),
        ),
        migrations.AddField(
            model_name="peachjamsettings",
            name="twitter_link",
            field=models.URLField(blank=True, null=True, verbose_name="twitter link"),
        ),
    ]
