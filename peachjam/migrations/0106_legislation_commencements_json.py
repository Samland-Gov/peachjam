# Generated by Django 3.2.20 on 2023-09-06 12:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('peachjam', '0105_legislation_timeline'),
    ]

    operations = [
        migrations.AddField(
            model_name='legislation',
            name='commencements_json',
            field=models.JSONField(default=list, verbose_name='commencements_json'),
        ),
    ]
