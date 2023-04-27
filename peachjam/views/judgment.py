from django.views.generic import TemplateView

from peachjam.models import CourtClass, Judgment
from peachjam.registry import registry
from peachjam.views.generic_views import BaseDocumentDetailView


class JudgmentListView(TemplateView):
    model = Judgment
    template_name = "peachjam/judgment_list.html"
    navbar_link = "judgments"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        court_classes = CourtClass.objects.prefetch_related("courts")
        context["court_classes"] = court_classes
        context["recent_judgments"] = Judgment.objects.order_by("-date")[:30]
        return context


@registry.register_doc_type("judgment")
class JudgmentDetailView(BaseDocumentDetailView):
    model = Judgment
    template_name = "peachjam/judgment_detail.html"
