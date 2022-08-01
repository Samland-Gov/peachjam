from django.shortcuts import get_object_or_404

from africanlii.utils import lowercase_alphabet
from peachjam.models import Author, Judgment
from peachjam.views.generic_views import FilteredDocumentListView


class BaseCourtDetailView(FilteredDocumentListView):
    """Generic List View class for filtering a court's judgments."""

    context_object_name = "documents"
    paginate_by = 20
    model = Judgment
    template_name = "lawlibrary/court_detail.html"

    def get_base_queryset(self):
        if "year" in self.kwargs:
            return self.model.objects.filter(
                author=self.author, date__year=self.kwargs["year"]
            )
        return self.model.objects.filter(author=self.author)

    def get_queryset(self):
        self.author = get_object_or_404(Author, code=self.kwargs["code"])
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        years = list(
            set(
                self.model.objects.filter(author=self.author).values_list(
                    "date__year", flat=True
                )
            )
        )

        context["years"] = sorted(years, reverse=True)

        judges = list(
            set(self.get_base_queryset().values_list("judges__name", flat=True))
        )
        if None in judges:
            judges.remove(None)

        context["court"] = self.author
        if "year" in self.kwargs:
            context["year"] = self.kwargs["year"]
        context["facet_data"] = {
            "judges": judges,
            "alphabet": lowercase_alphabet(),
        }

        return context


class CourtDetailView(BaseCourtDetailView):
    """View for listing a court's judgments."""

    pass


class YearView(BaseCourtDetailView):
    """View for filtering a court's judgments, based on the year."""

    pass
