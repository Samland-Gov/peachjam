from django.views.generic import DetailView, ListView

from africanlii.models import Judgment
from africanlii.registry import registry
from peachjam.views import AuthedViewMixin


class JudgmentListView(AuthedViewMixin, ListView):
    model = Judgment
    template_name = "africanlii/judgment_list.html"
    context_object_name = "documents"
    paginate_by = 20


@registry.register_doc_type("judgment")
class JudgmentDetailView(AuthedViewMixin, DetailView):
    model = Judgment
    template_name = "africanlii/judgment_detail.html"
    context_object_name = "document"
