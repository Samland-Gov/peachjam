# Generated by Django 3.2.18 on 2023-02-24 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("peachjam", "0057_alter_courtregistry_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="courtregistry",
            name="code",
            field=models.SlugField(max_length=255, unique=True, verbose_name="code"),
        ),
    ]
