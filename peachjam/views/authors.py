from django.db.models import Q
from django.shortcuts import get_object_or_404

from peachjam.models import Author, CoreDocument
from peachjam.views.generic_views import FilteredDocumentListView


class AuthorDetailView(FilteredDocumentListView):
    template_name = "peachjam/author_detail.html"
    navbar_link = "author_detail"

    def get_base_queryset(self):
        return CoreDocument.objects.prefetch_related("nature", "work").filter(
            Q(genericdocument__author=self.author)
            | Q(legalinstrument__author=self.author)
        )

    def get_queryset(self):
        self.author = get_object_or_404(Author, code=self.kwargs["code"])
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doc_types = list(
            set(
                self.form.filter_queryset(
                    self.get_base_queryset(), exclude="doc_type"
                ).values_list("doc_type", flat=True)
            )
        )

        context["author"] = self.author
        context["doc_table_show_author"] = False
        context["doc_table_show_doc_type"] = bool(doc_types)
        context["facet_data"]["docTypes"] = doc_types

        return context
