# Generated by Django 3.2.12 on 2022-03-24 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peachjam', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='decision',
            name='author',
        ),
        migrations.RemoveField(
            model_name='decision',
            name='matter_type',
        ),
        migrations.DeleteModel(
            name='Court',
        ),
        migrations.DeleteModel(
            name='Decision',
        ),
        migrations.DeleteModel(
            name='MatterType',
        ),
    ]
