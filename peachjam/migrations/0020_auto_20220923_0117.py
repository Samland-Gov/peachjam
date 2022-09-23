# Generated by Django 3.2.14 on 2022-09-23 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("peachjam", "0019_ingestor_enabled"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="judgmentmediasummaryfile",
            name="mime_type",
        ),
        migrations.AddField(
            model_name="judgmentmediasummaryfile",
            name="mimetype",
            field=models.CharField(default="", max_length=1024),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="judgmentmediasummaryfile",
            name="filename",
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name="judgmentmediasummaryfile",
            name="size",
            field=models.BigIntegerField(default=0),
        ),
    ]
