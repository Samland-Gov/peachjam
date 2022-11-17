import copy
from os.path import splitext

from django import forms
from django.core.files import File
from django.http import QueryDict
from django.utils.text import slugify

from peachjam.models import CoreDocument, Ingestor, SourceFile
from peachjam.plugins import plugins
from peachjam.storage import clean_filename


def work_choices():
    return [("", "---")] + [
        (doc.work.pk, doc.title) for doc in CoreDocument.objects.order_by("title")
    ]


def adapter_choices():
    return [(key, p.name) for key, p in plugins.registry["ingestor-adapter"].items()]


class IngestorForm(forms.ModelForm):
    adapter = forms.ChoiceField(choices=adapter_choices)
    last_refreshed_at = forms.DateTimeField(required=False)
    name = forms.CharField(max_length=255)

    class Meta:
        model = Ingestor
        fields = ("adapter", "name")


class NewDocumentFormMixin:
    """Mixin for the admin view when creating a new document that adds a new field to allow the user to upload a
    file from which key data can be extracted.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["upload_file"] = forms.FileField(required=False)

    def save(self, commit=True):
        obj = super().save(commit)
        if self.cleaned_data.get("upload_file"):
            self.process_upload_file(self.cleaned_data["upload_file"])
            self.run_analysis()
        return obj

    def process_upload_file(self, upload_file):
        # store the uploaded file
        self.instance.save()
        upload_file.seek(0)
        file_ext = splitext(upload_file.name)[1]
        SourceFile(
            document=self.instance,
            file=File(
                upload_file, name=f"{slugify(self.instance.title[-250:])}{file_ext}"
            ),
            mimetype=upload_file.content_type,
        ).save()

        # extract content, if we can
        if self.instance.extract_content_from_source_file():
            self.instance.save()

    def run_analysis(self):
        """Apply analysis pipelines for this newly created document."""
        if self.instance.extract_citations():
            self.instance.save()

    @classmethod
    def adjust_fieldsets(cls, fieldsets):
        # add the upload_file to the first set of fields to include on the page
        fieldsets = copy.deepcopy(fieldsets)
        fieldsets[0][1]["fields"].append("upload_file")
        return fieldsets

    @classmethod
    def adjust_fields(cls, fields):
        # don't include 'upload_field' when generating the form
        return [f for f in fields if f != "upload_file"]


class BaseDocumentFilterForm(forms.Form):
    """This is the main form used for filtering Document ListViews,
    using facets such as year and alphabetical title.
    """

    years = forms.CharField(required=False)
    alphabet = forms.CharField(required=False)
    authors = forms.CharField(required=False)
    doc_type = forms.CharField(required=False)
    judges = forms.CharField(required=False)

    def __init__(self, data, *args, **kwargs):
        self.params = QueryDict(mutable=True)
        self.params.update(data)

        super().__init__(self.params, *args, **kwargs)

    def filter_queryset(self, queryset, exclude=None):

        years = self.params.getlist("years")
        alphabet = self.cleaned_data.get("alphabet")
        authors = self.params.getlist("authors")
        courts = self.params.getlist("courts")
        doc_type = self.params.getlist("doc_type")
        judges = self.params.getlist("judges")

        if years and exclude != "years":
            queryset = queryset.filter(date__year__in=years)

        if alphabet and exclude != "alphabet":
            queryset = queryset.filter(title__istartswith=alphabet)

        if authors and exclude != "author":
            queryset = queryset.filter(author__name__in=authors)

        if courts and exclude != "courts":
            queryset = queryset.filter(court__name__in=courts)

        if doc_type and exclude != "doc_type":
            queryset = queryset.filter(doc_type__in=doc_type)

        if judges and exclude != "judges":
            queryset = queryset.filter(judges__name__in=judges)

        return queryset


class SourceFileForm(forms.ModelForm):
    class Meta:
        model = SourceFile
        fields = "__all__"

    def clean_file(self):
        # dynamic storage files don't like colons in filenames
        self.cleaned_data["file"].name = clean_filename(self.cleaned_data["file"].name)
        return self.cleaned_data["file"]

    def save(self, commit=True):
        obj = super().save(commit=True)
        if "file" in self.changed_data:
            if obj.document.extract_content_from_source_file():
                obj.document.save()
        return obj
