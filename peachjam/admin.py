from django.contrib import admin
from django.http.response import FileResponse
from django.shortcuts import get_object_or_404
from django.urls import path, reverse
from django.utils.html import format_html

from peachjam.models import Image, Locality, SourceFile

admin.site.register(
    [
        Image,
        Locality,
        SourceFile,
    ]
)


class SourceFileInline(admin.TabularInline):
    model = SourceFile
    extra = 0
    readonly_fields = ("filename", "mimetype", "attachment_link")

    def attachment_link(self, obj):
        if obj.pk:
            return format_html(
                '<a href="{url}">{title}</a>',
                url=reverse(
                    "admin:peachjam_source_file",
                    kwargs={
                        "pk": obj.pk,
                    },
                ),
                title=obj.filename,
            )


class DocumentAdmin(admin.ModelAdmin):
    inlines = [SourceFileInline]
    list_display = ("title", "date")
    search_fields = ("title", "date")
    readonly_fields = ("expression_frbr_uri",)
    exclude = ("doc_type",)

    def get_urls(self):
        return [
            path(
                "source_files/<int:pk>",
                self.admin_site.admin_view(self.download_sourcefile),
                name="peachjam_source_file",
            )
        ] + super().get_urls()

    def download_sourcefile(self, request, pk):
        source_file = get_object_or_404(SourceFile.objects, pk=pk)
        return FileResponse(source_file.file)


class CoreDocumentAdmin(admin.ModelAdmin):
    inlines = [
        SourceFileInline,
    ]
