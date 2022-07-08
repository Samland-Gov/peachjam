from django.db.models import Q
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from africanlii.forms import BaseDocumentFilterForm
from africanlii.utils import lowercase_alphabet
from peachjam.models import Author, CoreDocument


def add_facet_data_to_context(years, doc_types):
    return {"years": years, "doc_types": doc_types, "alphabet": lowercase_alphabet()}


class BaseAuthorListView(ListView):
    context_object_name = "documents"
    paginate_by = 20
    model = Author
    template_name = "africanlii/_author_detail.html"


class AuthorListView(BaseAuthorListView):
    def get_queryset(self):
        self.form = BaseDocumentFilterForm(self.request.GET)
        self.form.is_valid()
        author = get_object_or_404(self.model, pk=self.kwargs["pk"])

        queryset = CoreDocument.objects.filter(
            Q(genericdocument__author=author)
            | Q(legalinstrument__author=author)
            | Q(judgment__author=author)
        )

        return self.form.filter_queryset(queryset)

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        author = get_object_or_404(self.model, pk=self.kwargs["pk"])

        # Fetch the author's documents
        docs = CoreDocument.objects.filter(
            Q(genericdocument__author=author)
            | Q(legalinstrument__author=author)
            | Q(judgment__author=author)
        )

        # Initialize facet_data values
        years = list(set(docs.values_list("date__year", flat=True)))
        doc_types = list(set(docs.values_list("doc_type", flat=True)))

        # Read parameter values
        params = QueryDict(mutable=True)
        params.update(self.request.GET)

        year = params.get("year")
        doc_type = params.get("doc_type")
        alphabet = params.get("alphabet")

        # Use parameter values to filter
        if year:
            years = list(
                set(docs.filter(date__year=year).values_list("date__year", flat=True))
            )

        if doc_type:
            doc_types = list(
                set(docs.filter(doc_type=doc_type).values_list("doc_type", flat=True))
            )

        if alphabet:
            documents = self.get_queryset().filter(title__istartswith=alphabet)
            years = list(set(documents.values_list("date__year", flat=True)))
            doc_types = list(set(documents.values_list("doc_type", flat=True)))
            context["documents"] = documents

        context["author"] = author
        context["author_listing_view"] = True
        context["facet_data"] = add_facet_data_to_context(years, doc_types)

        return context
