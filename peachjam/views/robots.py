from django.views.generic import TemplateView

from peachjam.models import CoreDocument


class RobotsView(TemplateView):
    template_name = "peachjam/robots.txt"
    content_type = "text/plain"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        disallowed_content = [
            "Disallow: " + doc.expression_frbr_uri
            for doc in CoreDocument.objects.exclude(allow_robots=True)
        ]
        context["disallowed_content"] = "\n".join(disallowed_content)

        return context
