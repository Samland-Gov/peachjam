from django.views.generic import DetailView, ListView

from africanlii.models import LegalInstrument
from africanlii.registry import registry
from peachjam.views import AuthedViewMixin


class LegalInstrumentListView(AuthedViewMixin, ListView):
    model = LegalInstrument
    template_name = "africanlii/legal_instrument_list.html"
    context_object_name = "documents"
    paginate_by = 20

    def get_queryset(self):
        self.form = DocumentFilterForm(self.request.GET)
        self.form.is_valid()
        queryset = LegalInstrument.objects.all()
        return self.form.filter_queryset(queryset)

    def get_context_data(self, **kwargs):
        context = super(LegalInstrumentListView, self).get_context_data(**kwargs)
        authors = list(
            set(LegalInstrument.objects.values_list("authoring_body__name", flat=True))
        )
        context["authors"] = authors
        return context


@registry.register_doc_type("legal_instrument")
class LegalInstrumentDetailView(AuthedViewMixin, DetailView):
    model = LegalInstrument
    slug_field = "expression_frbr_uri"
    slug_url_kwarg = "expression_frbr_uri"
    template_name = "africanlii/legal_instrument_detail.html"
    context_object_name = "document"
