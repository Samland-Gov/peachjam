# Generated by Django 3.2.18 on 2023-04-25 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("peachjam", "0066_auto_20230425_1103"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="courtclass",
            options={
                "ordering": ("order", "name"),
                "verbose_name": "court class",
                "verbose_name_plural": "court classes",
            },
        ),
        migrations.AddField(
            model_name="courtclass",
            name="order",
            field=models.IntegerField(blank=True, null=True, verbose_name="order"),
        ),
    ]
