# Generated by Django 3.2.14 on 2022-09-30 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("liiweb", "0002_alter_courtclass_options"),
        ("peachjam", "0024_court_model"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="courtdetail",
            name="court",
        ),
        migrations.RemoveField(
            model_name="courtdetail",
            name="court_class",
        ),
        migrations.DeleteModel(
            name="CourtClass",
        ),
        migrations.DeleteModel(
            name="CourtDetail",
        ),
    ]
