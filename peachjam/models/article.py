import os

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


def file_location(instance, filename):
    filename = os.path.basename(filename)
    return f"{instance.SAVE_FOLDER}/{instance.pk}/{filename}"


class Article(models.Model):
    SAVE_FOLDER = "articles"
    doc_type = "article"

    date = models.DateField(_("date"), null=False, blank=False)
    title = models.CharField(_("title"), max_length=1024, null=False, blank=False)
    body = models.TextField(_("body"))
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="articles",
        verbose_name=_("author"),
    )
    image = models.ImageField(
        _("image"), upload_to=file_location, blank=True, null=True
    )
    summary = models.TextField(_("summary"), null=True, blank=True)
    slug = models.SlugField(_("slug"), max_length=1024, unique=True)
    published = models.BooleanField(_("published"), default=False)
    topics = models.ManyToManyField(
        "peachjam.Taxonomy", verbose_name=_("topics"), blank=True
    )

    class Meta:
        verbose_name = _("article")
        verbose_name_plural = _("articles")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "article_detail",
            kwargs={
                "date": self.date.strftime("%Y-%m-%d"),
                "author": self.author.username,
                "slug": self.slug,
            },
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # save article first to get pk for image folder
        if not self.pk:
            saved_image = self.image
            self.image = None
            super().save(*args, **kwargs)
            self.image = saved_image

        return super().save(*args, **kwargs)


class UserProfile(models.Model):
    SAVE_FOLDER = "user_profiles"

    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, verbose_name=_("user")
    )
    photo = models.ImageField(
        _("photo"), upload_to=file_location, blank=True, null=True
    )
    profile_description = models.TextField(_("profile description"))

    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")

    def __str__(self):
        return f"{self.user.username}"


@receiver(post_save, sender=get_user_model())
def user_saved(sender, instance, created, **kwargs):
    if created:
        # ensure a user profile exists
        UserProfile.objects.get_or_create(user=instance)
