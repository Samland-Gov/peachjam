from django.views.generic import DetailView, ListView

from africanlii.models import LegalInstrument
from africanlii.registry import registry
from peachjam.views import AuthedViewMixin


class LegalInstrumentListView(AuthedViewMixin, ListView):
    model = LegalInstrument
    template_name = "africanlii/legal_instrument_list.html"
    context_object_name = "documents"
    paginate_by = 20


@registry.register_doc_type("legal_instrument")
class LegalInstrumentDetailView(AuthedViewMixin, DetailView):
    model = LegalInstrument
    template_name = "africanlii/legal_instrument_detail.html"
    context_object_name = "document"
