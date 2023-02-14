from countries_plus.models import Country
from django.db import models
from django.utils.translation import gettext_lazy as _

from peachjam.models import Work


class Ratification(models.Model):
    work = models.OneToOneField(
        Work,
        related_name="ratification",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name=_("work"),
    )
    source_url = models.URLField(_("source URL"), null=True, blank=True)
    last_updated = models.DateField(_("last updated"), null=True, blank=True)

    class Meta:
        verbose_name = _("ratification")
        verbose_name_plural = _("ratifications")

    def __str__(self):
        return f"{self.work}"


class RatificationCountry(models.Model):
    ratification = models.ForeignKey(
        Ratification,
        related_name="countries",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name=_("ratification"),
    )
    country = models.ForeignKey(
        Country,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name=_("country"),
    )
    ratification_date = models.DateField(_("ratification date"), null=True, blank=True)
    deposit_date = models.DateField(_("deposit date"), null=True, blank=True)
    signature_date = models.DateField(_("signature date"), null=True, blank=True)

    class Meta:
        verbose_name = _("ratification country")
        verbose_name_plural = _("ratification countries")
        ordering = ["country__name"]

        constraints = [
            models.UniqueConstraint(
                fields=["ratification", "country"], name="unique_ratification_country"
            )
        ]

    def __str__(self):
        return f"{self.country} - {self.ratification.work}"
