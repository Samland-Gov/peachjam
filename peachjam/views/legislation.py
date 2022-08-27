from datetime import datetime, timedelta
from itertools import groupby

from django.contrib import messages
from django.utils.html import format_html

from peachjam.models import Legislation
from peachjam.registry import registry
from peachjam.views.generic_views import (
    BaseDocumentDetailView,
    FilteredDocumentListView,
)


class LegislationListView(FilteredDocumentListView):
    model = Legislation
    template_name = "peachjam/legislation_list.html"
    context_object_name = "documents"
    paginate_by = 20


@registry.register_doc_type("legislation")
class LegislationDetailView(BaseDocumentDetailView):
    model = Legislation
    template_name = "peachjam/legislation_detail.html"

    def get_notices(self):
        notices = super().get_notices()
        repeal = self.get_repeal_info()
        friendly_type = self.get_friendly_type()

        if self.object.repealed and repeal:
            msg = "This {} was repealed on {} by <a href='{}'>{}</a>."
            notices.append(
                {
                    "type": messages.ERROR,
                    "html": format_html(
                        msg.format(
                            friendly_type,
                            repeal["date"],
                            repeal["repealing_uri"],
                            repeal["repealing_title"],
                        )
                    ),
                }
            )

        points_in_time = self.get_points_in_time()
        if points_in_time:
            current_object_date = self.object.date.strftime("%Y-%m-%d")
            dates = [point_in_time["date"] for point_in_time in points_in_time]
            index = dates.index(current_object_date)

            if index == len(dates) - 1:
                if self.object.repealed and repeal:
                    msg = (
                        "This is the version of this {} as it was when it was repealed."
                    )
                else:
                    msg = "This is the latest version of this {}."

                notices.append(
                    {
                        "type": messages.INFO,
                        "html": format_html(msg.format(friendly_type)),
                    }
                )
            else:
                date = datetime.strptime(
                    dates[index + 1], "%Y-%m-%d"
                ).date() - timedelta(days=1)

                if self.object.repealed and repeal:
                    msg = (
                        "This is the version of this {} as it was from {} to {}. "
                        "<a href='{}'>Read the version as it was when it was repealed</a>."
                    )
                else:
                    msg = (
                        "This is the version of this {} as it was from {} to {}. "
                        "<a href='{}'>Read the version currently in force</a>."
                    )

                notices.append(
                    {
                        "type": messages.WARNING,
                        "html": format_html(
                            msg.format(
                                friendly_type,
                                current_object_date,
                                date,
                                points_in_time[-1]["expressions"][0][
                                    "expression_frbr_uri"
                                ],
                            )
                        ),
                    }
                )

        return notices

    def get_repeal_info(self):
        return self.object.metadata_json.get("repeal", None)

    def get_friendly_type(self):
        return self.object.metadata_json.get("type_name", None)

    def get_points_in_time(self):
        return self.object.metadata_json.get("points_in_time", None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_object_date"] = self.object.date.strftime("%Y-%m-%d")
        context["timeline_events"] = self.get_timeline_events()
        context["friendly_type"] = self.get_friendly_type()
        return context

    def get_timeline_events(self):
        events = []

        work = self.object.metadata_json

        points_in_time = self.get_points_in_time()
        expressions = {
            point_in_time["date"]: point_in_time["expressions"][0]
            for point_in_time in points_in_time or []
        }

        assent_date = self.object.metadata_json.get("assent_date", None)
        if assent_date:
            events.append(
                {
                    "date": (work["assent_date"]),
                    "event": "assent",
                }
            )

        publication_date = self.object.metadata_json.get("publication_date", None)
        if publication_date:
            events.append(
                {
                    "date": (publication_date),
                    "event": "publication",
                    "publication_name": work["publication_name"],
                    "publication_number": work["publication_number"],
                    "publication_url": work["publication_document"]["url"],
                }
            )

        commencement_date = self.object.metadata_json.get("commencement_date", None)
        if commencement_date:
            events.append(
                {
                    "date": (commencement_date),
                    "event": "commencement",
                    "friendly_type": work["type_name"],
                }
            )

        amendments = self.object.metadata_json.get("amendments", None)
        if amendments:
            events.extend(
                [
                    {
                        "date": (amendment["date"]),
                        "event": "amendment",
                        "amending_title": amendment["amending_title"],
                        "amending_uri": amendment["amending_uri"],
                    }
                    for amendment in amendments
                ]
            )

        repeal = self.get_repeal_info()
        if repeal:
            events.append(
                {
                    "date": (repeal["date"]),
                    "event": "repeal",
                    "repealing_title": repeal["repealing_title"],
                    "repealing_uri": repeal["repealing_uri"],
                }
            )

        events.sort(key=lambda event: event["date"])
        events = [
            {
                "date": date,
                "events": list(group),
            }
            for date, group in groupby(events, lambda event: event["date"])
        ]

        for event in events:
            for e in event["events"]:
                del e["date"]
            uri = expressions.get(event["date"], {}).get("expression_frbr_uri")
            if uri:
                event["expression_frbr_uri"] = uri

        events.sort(key=lambda event: event["date"], reverse=True)

        return events
