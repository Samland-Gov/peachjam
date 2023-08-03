from django.http import Http404, HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, DjangoModelPermissions

from peachjam.models import Judgment
from peachjam_api.serializers import JudgmentSerializer


class JudgmentAPIPermission(BasePermission):
    def has_permission(self, request, view):
        # user must have perms to access judgments through the api
        return (
            request.user
            and request.user.is_authenticated
            and request.user.has_perm("peachjam.api_judgment")
        )


class JudgmentsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [
        JudgmentAPIPermission,
        DjangoModelPermissions,
    ]
    queryset = Judgment.objects.select_related("court").all()
    serializer_class = JudgmentSerializer
    filterset_fields = {
        "jurisdiction": ["exact"],
        "work_frbr_uri": ["exact"],
        "title": ["exact", "icontains"],
        "date": ["exact", "gte", "lte"],
        "updated_at": ["exact", "gte", "lte"],
        "created_at": ["exact", "gte", "lte"],
    }
    ordering_fields = ["title", "date", "updated_at", "created_at"]
    ordering = ["updated_at"]

    @action(detail=True, url_path="source.txt")
    def source_txt(self, request, pk=None):
        """Source document (or text) for this judgment."""
        obj = self.get_object()
        # we only allow certain formats
        try:
            content = getattr(obj, "document_content")
        except AttributeError:
            raise Http404()

        # return content.content_text as a normal drf response object
        return HttpResponse(content.content_text, content_type="text/plain")

    @action(detail=True, url_path="source.pdf")
    def source_pdf(self, request, pk=None):
        """Source document in PDF form (if available)."""
        obj = self.get_object()
        # we only allow certain formats
        try:
            source_file = getattr(obj, "source_file")
        except AttributeError:
            raise Http404()

        if not source_file.file or source_file.mimetype != "application/pdf":
            raise Http404()

        return self.make_response(
            source_file.file, source_file.mimetype, source_file.filename_for_download()
        )

    def make_response(self, f, content_type, fname):
        file_bytes = f.read()
        response = HttpResponse(file_bytes, content_type=content_type)
        response["Content-Disposition"] = f"inline; filename={fname}"
        response["Content-Length"] = str(len(file_bytes))
        return response
