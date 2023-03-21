from django.db.models import Q
from django.views.generic import TemplateView

from peachjam.models import (
    Author,
    CoreDocument,
    Court,
    GenericDocument,
    Judgment,
    LegalInstrument,
    Legislation,
)


class HomePageView(TemplateView):
    template_name = "peachjam/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_judgments = Judgment.objects.order_by("-date")[:5]
        recent_documents = GenericDocument.objects.order_by("-date")[:5]
        recent_instruments = LegalInstrument.objects.order_by("-date")[:5]
        recent_legislation = Legislation.objects.order_by("-date")[:5]
        documents_count = CoreDocument.objects.count()

        authors = Author.objects.exclude(
            Q(genericdocument__isnull=True),
            Q(legalinstrument__isnull=True),
        )

        courts = Court.objects.all()

        context["recent_judgments"] = recent_judgments
        context["recent_documents"] = recent_documents
        context["recent_instruments"] = recent_instruments
        context["recent_legislation"] = recent_legislation
        context["documents_count"] = documents_count
        context["authors"] = authors
        context["courts"] = courts

        return context
