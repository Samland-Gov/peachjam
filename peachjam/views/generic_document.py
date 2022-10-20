from peachjam.models import GenericDocument
from peachjam.registry import registry
from peachjam.views.generic_views import (
    BaseDocumentDetailView,
    BaseQuerysetPrefetchMixin,
    FilteredDocumentListView,
)


class GenericDocumentListView(FilteredDocumentListView, BaseQuerysetPrefetchMixin):
    template_name = "peachjam/generic_document_list.html"
    model = GenericDocument
    navbar_link = "generic_documents"

    def get_queryset(self):
        queryset = super(GenericDocumentListView, self).get_queryset()
        return queryset.order_by("-date")


@registry.register_doc_type("generic_document")
class GenericDocumentDetailView(BaseDocumentDetailView):
    model = GenericDocument
    template_name = "peachjam/generic_document_detail.html"
