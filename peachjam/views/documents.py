from cobalt import FrbrUri
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import get_language
from django.views.generic import DetailView, View

from peachjam.helpers import add_slash, add_slash_to_frbr_uri
from peachjam.models import CoreDocument
from peachjam.registry import registry


class RedirectResolver:

    RESOLVER_MAPPINGS = {
        "africanlii": {
            "country_code": "aa",
            "domain": "africanlii.org",
        },
        "eswatinilii": {
            "country_code": "sz",
            "domain": "eswatinilii.org",
        },
        "ghalii": {
            "country_code": "gh",
            "domain": "ghalii.org",
        },
        "lawlibrary": {
            "country_code": "za",
            "domain": "lawlibrary.org.za",
        },
        "leslii": {
            "country_code": "ls",
            "domain": "lesotholii.org",
        },
        "malawilii": {
            "country_code": "mw",
            "domain": "malawilii.org",
        },
        "namiblii": {
            "country_code": "na",
            "domain": "namiblii.org",
        },
        "nigerialii": {
            "country_code": "ng",
            "domain": "nigerialii.org",
        },
        "open by-laws": {
            "place_code": [],
            "domain": "obl.laws.africa",
        },
        "senlii": {
            "country_code": "sn",
            "domain": "senlii.org",
        },
        "seylii": {
            "country_code": "sc",
            "domain": "seylii.org",
        },
        "sierralii": {
            "country_code": "sl",
            "domain": "sierralii.org",
        },
        "tanzlii": {
            "country_code": "tz",
            "domain": "tanzlii.org",
        },
        "tcilii": {
            "country_code": "tc",
            "domain": "tcilii.org",
        },
        "ulii": {
            "country_code": "ug",
            "domain": "ulii.org",
        },
        "zambialii": {
            "country_code": "zm",
            "domain": "zambialii.org",
        },
        "zanzibarlii": {
            "place_code": "tz-znz",
            "domain": "zanzibarlii.org",
        },
        "zimlii": {
            "country_code": "zw",
            "domain": "zimlii.org",
        },
    }

    def __init__(self, app_name):
        self.current_authority = self.RESOLVER_MAPPINGS[app_name.lower()]

    def get_domain_for_frbr_uri(self, parsed_uri):
        best_domain = self.get_best_domain(parsed_uri)
        if best_domain != self.current_authority["domain"]:
            return best_domain
        return None

    def get_best_domain(self, parsed_uri):
        country_code = parsed_uri.country
        place_code = parsed_uri.place

        if country_code != place_code:
            for key, mapping in self.RESOLVER_MAPPINGS.items():
                if mapping.get("place_code") == place_code:
                    return mapping.get("domain")

        # if no domain matching with place code is found use country code
        for key, mapping in self.RESOLVER_MAPPINGS.items():
            if mapping.get("country_code") == country_code:
                return mapping.get("domain")
        return None


class DocumentDetailViewResolver(View):
    """Resolver view that returns detail views for documents based on their doc_type."""

    def dispatch(self, request, *args, **kwargs):
        # redirect /akn/foo/ to /akn/foo because FRBR URIs don't end in /
        if kwargs["frbr_uri"].endswith("/"):
            return redirect("document_detail", frbr_uri=kwargs["frbr_uri"][:-1])

        frbr_uri = add_slash(kwargs["frbr_uri"])

        try:
            # return 404 early if frbr_uri is invalid
            parsed_frbr_uri = FrbrUri.parse(frbr_uri)
        except ValueError:
            raise Http404()

        obj, exact = CoreDocument.objects.best_for_frbr_uri(frbr_uri, get_language())

        if not obj:
            resolver = RedirectResolver(settings.PEACHJAM["APP_NAME"])
            domain = resolver.get_domain_for_frbr_uri(parsed_frbr_uri)
            if domain:
                url = f"https://{domain}{frbr_uri}"
                return redirect(url)
            raise Http404()

        if not exact:
            return redirect(obj.get_absolute_url())

        view_class = registry.views.get(obj.doc_type)
        if view_class:
            view = view_class()
            view.setup(request, *args, **kwargs)

            return view.dispatch(request, *args, **kwargs)


@method_decorator(add_slash_to_frbr_uri(), name="setup")
class DocumentSourceView(DetailView):
    model = CoreDocument
    slug_field = "expression_frbr_uri"
    slug_url_kwarg = "frbr_uri"

    def render_to_response(self, context, **response_kwargs):
        if hasattr(self.object, "source_file") and self.object.source_file.file:
            source_file = self.object.source_file

            if source_file.source_url:
                return redirect(source_file.source_url)

            file = source_file.file.open()
            file_bytes = file.read()
            response = HttpResponse(file_bytes, content_type=source_file.mimetype)
            response[
                "Content-Disposition"
            ] = f"inline; filename={source_file.filename_for_download()}"
            response["Content-Length"] = str(len(file_bytes))
            return response
        raise Http404


class DocumentSourcePDFView(DocumentSourceView):
    def render_to_response(self, context, **response_kwargs):
        if hasattr(self.object, "source_file"):
            source_file = self.object.source_file

            if source_file.source_url and source_file.mimetype == "application/pdf":
                return redirect(source_file.source_url)

            file = source_file.as_pdf()
            return HttpResponse(file.read(), content_type="application/pdf")

        raise Http404()


@method_decorator(add_slash_to_frbr_uri(), name="setup")
class DocumentMediaView(DetailView):
    """Serve an image file, such as

    /akn/za/judgment/afchpr/2022/1/eng@2022-09-14/media/tmpwx2063x2_html_31b3ed1b55e86754.png
    """

    model = CoreDocument
    slug_field = "expression_frbr_uri"
    slug_url_kwarg = "frbr_uri"

    def render_to_response(self, context, **response_kwargs):
        img = get_object_or_404(self.object.images, filename=self.kwargs["filename"])
        file = img.file.open()
        file_bytes = file.read()
        response = HttpResponse(file_bytes, content_type=img.mimetype)
        response["Content-Length"] = str(len(file_bytes))
        return response
