# Generated by Django 3.2.15 on 2022-10-21 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("peachjam", "0032_nature_codes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="documentnature",
            name="code",
            field=models.SlugField(max_length=1024, unique=True),
        ),
    ]
