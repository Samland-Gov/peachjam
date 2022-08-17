from rest_framework import viewsets

from peachjam.models import CitationLink, Legislation, Relationship, Work
from peachjam_api.serializers import (
    CitationLinkSerializer,
    LegislationSerializer,
    RelationshipSerializer,
    WorkSerializer,
)


class RelationshipViewSet(viewsets.ModelViewSet):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer


class WorksViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    filterset_fields = {
        "frbr_uri": ["exact"],
        "title": ["exact", "icontains"],
    }


class CitationLinkViewSet(viewsets.ModelViewSet):
    queryset = CitationLink.objects.all()
    serializer_class = CitationLinkSerializer


class LegislationViewSet(viewsets.ModelViewSet):
    queryset = Legislation.objects.all()
    serializer_class = LegislationSerializer
