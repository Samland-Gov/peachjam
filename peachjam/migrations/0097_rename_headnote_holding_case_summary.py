# Generated by Django 3.2.19 on 2023-08-16 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("peachjam", "0096_auto_20230814_1557"),
    ]

    operations = [
        migrations.RenameField(
            model_name="judgment",
            old_name="headnote_holding",
            new_name="case_summary",
        ),
    ]
