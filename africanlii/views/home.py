from django.views.generic import TemplateView

from africanlii.models import GenericDocument, Judgment, LegalInstrument, Legislation
from peachjam.views import AuthedViewMixin


class HomePageView(AuthedViewMixin, TemplateView):
    template_name = "africanlii/home.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        recent_judgments = Judgment.objects.order_by("-date")[:5]
        recent_documents = GenericDocument.objects.order_by("-date")[:5]
        recent_instruments = LegalInstrument.objects.order_by("-date")[:5]
        recent_legislation = Legislation.objects.order_by("-date")[:5]
        documents_count = GenericDocument.objects.all().count()

        context["documents_count"] = documents_count
        context["recent_judgments"] = recent_judgments
        context["recent_documents"] = recent_documents
        context["recent_instruments"] = recent_instruments
        context["recent_legislation"] = recent_legislation

        return self.render_to_response(context)
