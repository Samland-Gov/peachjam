# Generated by Django 3.2.18 on 2023-05-05 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("africanlii", "0007_alter_regionaleconomiccommunity_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="memberstate",
            name="code",
            field=models.CharField(
                default="--", editable=False, max_length=2, verbose_name="code"
            ),
            preserve_default=False,
        ),
    ]
