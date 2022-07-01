import copy

from django import forms

from peachjam.models import CoreDocument, Ingestor, Relationship, Work
from peachjam.plugins import plugins


def work_choices():
    return [("", "---")] + [
        (doc.work.pk, doc.title) for doc in CoreDocument.objects.order_by("title")
    ]


class RelationshipForm(forms.ModelForm):
    object_work = forms.ChoiceField(choices=work_choices)

    class Meta:
        model = Relationship
        fields = ["predicate", "object_work"]

    def __init__(self, subject_work, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.subject_work = subject_work

    def clean_object_work(self):
        return Work.objects.get(pk=self.cleaned_data["object_work"])


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
        if "upload_file" in self.cleaned_data:
            self.process_upload_file(self.cleaned_data["upload_file"])
        return super().save(commit)

    def process_upload_file(self, upload_file):
        # TODO: .doc content type
        if (
            upload_file.content_type
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            # TODO: read the uploaded file and extract its contents
            self.instance.content_html = "contents of file"

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
