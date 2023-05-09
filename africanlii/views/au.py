from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, TemplateView

from africanlii.models import RatificationCountry
from peachjam.models import AfricanUnionOrgan, MemberState, RegionalEconomicCommunity
from peachjam.views import AuthorDetailView, PlaceDetailView


class AfricanUnionDetailPageView(TemplateView):
    template_name = "peachjam/au_detail_page.html"
    model = AfricanUnionOrgan
    navbar_link = "au"

    def get_queryset(self):
        return self.model.objects.prefetch_related("author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["au_organs"] = self.get_queryset()
        context["recs"] = RegionalEconomicCommunity.objects.prefetch_related("locality")
        context["member_states"] = MemberState.objects.prefetch_related("country")
        return context


class AfricanUnionOrganDetailView(AuthorDetailView):
    template_name = "peachjam/au_organ_detail.html"


class RegionalEconomicCommunityDetailView(PlaceDetailView):
    template_name = "peachjam/regional_economic_community_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rec"] = get_object_or_404(
            RegionalEconomicCommunity, locality=self.locality
        )
        return context


class MemberStateDetailView(DetailView):
    template_name = "peachjam/member_state_detail.html"
    queryset = MemberState.objects.prefetch_related("country")
    slug_url_kwarg = "country"
    slug_field = "country"
    context_object_name = "member_state"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context[
            "ratification_countries"
        ] = ratification_countries = RatificationCountry.objects.prefetch_related(
            "ratification", "country"
        ).filter(
            country=self.get_object().country
        )
        context["doc_count"] = ratification_countries.count()

        return context
