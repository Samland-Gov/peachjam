from peachjam.models import Book, Journal
from peachjam.registry import registry
from peachjam.views.generic_views import (
    BaseDocumentDetailView,
    FilteredDocumentListView,
)


class BookListView(FilteredDocumentListView):
    model = Book
    template_name = "peachjam/book_list.html"


@registry.register_doc_type("book")
class BookDetailView(BaseDocumentDetailView):
    model = Book
    template_name = "peachjam/book_detail.html"


class JournalListView(FilteredDocumentListView):
    model = Journal
    template_name = "peachjam/journal_list.html"


@registry.register_doc_type("journal")
class JournalDetailView(BaseDocumentDetailView):
    model = Journal
    template_name = "peachjam/journal_detail.html"
