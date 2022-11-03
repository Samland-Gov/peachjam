from tempfile import NamedTemporaryFile
from unittest import mock

import tablib
from django.test import TestCase

from peachjam.models import Judgment
from peachjam.resources import JudgmentResource

judgment_import_headers = [
    "skip",
    "case_name",
    "case_string_override",
    "case_number_numeric",
    "case_number_year",
    "court",
    "source_url",
    "mnc",
    "serial_number",
    "date",
    "jurisdiction",
    "language",
    "judges",
    "media_summary_file",
    "matter_type",
    "serial_number_override",
]
row = [
    "",
    "Sigcau and Another v President of Republic of South Africa and Others",
    "CCT 315/21|CCT 321/21|CCT 6/22",
    "315|321|6",
    "2021|2021|2021",
    "EACJ",
    "https://mediafile.pdf|https://mediafile.docx",
    "[2022] EACJ 121",
    "44",
    "2022-09-14",
    "ZA",
    "eng",
    "Maya P|Dambuza JA|Makgoka JA|Gorven JA|Makaula AJA",
    "",
    "",
    "121",
]


def mocked_response(*args, **kwargs):
    class MockResponse:
        def __init__(self, data, status_code):
            self.data = data
            self.status_code = status_code

        def raise_for_status(self):
            pass

    return MockResponse(None, 200)


class JudgmentBulkImportTestCase(TestCase):
    fixtures = ["tests/courts", "tests/countries", "tests/languages"]

    @mock.patch("peachjam.resources.requests.head", side_effect=mocked_response)
    @mock.patch(
        "peachjam.resources.download_source_file", return_value=NamedTemporaryFile()
    )
    def test_source_file_prefers_docx_over_pdf(self, mock_request, mock_download):
        dataset = tablib.Dataset(row, headers=judgment_import_headers)
        result = JudgmentResource().import_data(dataset=dataset, dry_run=False)
        j = Judgment.objects.get(mnc="[2022] EACJ 121")
        self.assertFalse(result.has_errors())
        self.assertEqual(j.source_url, "https://mediafile.docx")

    def test_case_number_import_without_matter_type(self):
        dataset = tablib.Dataset(row, headers=judgment_import_headers)
        case_numbers = JudgmentResource().get_case_numbers(dataset.dict[0])
        self.assertEqual(case_numbers[0].number, 315)

    def test_case_numbers_with_matter_type(self):
        row.append("CCT|CCT|CCT")
        judgment_import_headers.append("matter_type")
        dataset = tablib.Dataset(row, headers=judgment_import_headers)
        case_numbers = JudgmentResource().get_case_numbers(dataset.dict[0])
        self.assertEqual(case_numbers[0].matter_type.name, "CCT")

    @mock.patch("peachjam.resources.requests.head", side_effect=mocked_response)
    @mock.patch(
        "peachjam.resources.download_source_file", return_value=NamedTemporaryFile()
    )
    def test_judgment_bulk_import(self, mock_request, download):
        dataset = tablib.Dataset(row, headers=judgment_import_headers)
        result = JudgmentResource().import_data(dataset=dataset, dry_run=False)
        judgment = Judgment.objects.first()
        self.assertFalse(result.has_errors())
        self.assertEquals(judgment.case_numbers.first().year, 2021)
