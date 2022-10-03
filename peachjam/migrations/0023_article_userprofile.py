# Generated by Django 3.2.15 on 2022-09-20 09:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import peachjam.models.article


def create_user_profiles(apps, schema_editor):
    User = apps.get_model("auth", "User")
    UserProfile = apps.get_model("peachjam", "UserProfile")
    for user in User.objects.all():
        UserProfile.objects.get_or_create(user=user)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("peachjam", "0022_judgment_hearing_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=peachjam.models.article.file_location,
                    ),
                ),
                ("profile_description", models.TextField()),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("title", models.CharField(max_length=1024)),
                ("body", models.TextField()),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=peachjam.models.article.file_location,
                    ),
                ),
                ("summary", models.TextField()),
                (
                    "slug",
                    models.SlugField(max_length=1024, unique=True),
                ),
                ("published", models.BooleanField(default=False)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="articles",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "topics",
                    models.ManyToManyField(to="peachjam.Taxonomy"),
                ),
            ],
        ),
        migrations.RunPython(create_user_profiles, migrations.RunPython.noop),
    ]
