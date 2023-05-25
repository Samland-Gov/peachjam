from django.views.generic import TemplateView

from peachjam.models import Article, CourtClass, Judgment, Legislation, Taxonomy


class HomePageView(TemplateView):
    template_name = "liiweb/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["court_classes"] = CourtClass.objects.prefetch_related("courts")
        context["recent_judgments"] = Judgment.objects.order_by("-date")[:5]
        context["recent_legislation"] = Legislation.objects.filter(
            metadata_json__stub=False
        ).order_by("-date")[:10]
        context["taxonomies"] = Taxonomy.get_tree()
        context["recent_articles"] = (
            Article.objects.prefetch_related("topics")
            .filter(published=True)
            .select_related("author")
            .order_by("-date")[:5]
        )
        return context


class PocketlawView(TemplateView):
    template_name = "liiweb/pocketlaw.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(pocketlaw_version="1.0.7", **kwargs)
