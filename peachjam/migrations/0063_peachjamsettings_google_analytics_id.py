# Generated by Django 3.2.16 on 2023-03-22 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("peachjam", "0062_backfill_size"),
    ]

    operations = [
        migrations.AddField(
            model_name="peachjamsettings",
            name="google_analytics_id",
            field=models.CharField(
                blank=True,
                max_length=1024,
                null=True,
                verbose_name="google analytics id",
            ),
        ),
    ]
