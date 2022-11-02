from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView

from peachjam.models import Taxonomy
from peachjam.views.generic_views import FilteredDocumentListView


class TopLevelTaxonomyListView(TemplateView):
    template_name = "peachjam/top_level_taxonomy_list.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["taxonomies"] = Taxonomy.get_tree()
        return self.render_to_response(context)


class FirstLevelTaxonomyListView(ListView):
    template_name = "peachjam/first_level_taxonomy_list.html"
    model = Taxonomy

    def get(self, request, *args, **kwargs):
        self.taxonomy = get_object_or_404(Taxonomy, slug=self.kwargs["topic"])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["taxonomy"] = self.taxonomy
        return context


class TaxonomyDetailView(FilteredDocumentListView):
    template_name = "peachjam/taxonomy_detail.html"

    def get(self, request, *args, **kwargs):

        if "/" in self.kwargs["topics"]:
            slug = self.kwargs["topics"].split("/")[-1]
            self.taxonomy = get_object_or_404(Taxonomy, slug=slug)
        else:
            self.taxonomy = get_object_or_404(Taxonomy, slug=self.kwargs["topics"])

        return super().get(request, *args, **kwargs)

    def get_base_queryset(self):
        return super().get_base_queryset().filter(taxonomies__topic=self.taxonomy)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["taxonomy"] = self.taxonomy
        context["taxonomies"] = self.taxonomy.get_children()
        context["path"] = self.request.path

        return context
