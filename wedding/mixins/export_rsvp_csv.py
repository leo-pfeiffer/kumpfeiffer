import csv
from datetime import date
from django.http import HttpResponse


class ExportRsvpMixin:
    def export_rsvp_csv(self, request, queryset):

        column_names = [
            "Invite",
            "Guest",
            "Coming",
            "First Course",
            "Second Course",
            "Note",
        ]

        response = HttpResponse(content_type="text/csv")
        response[
            "Content-Disposition"
        ] = f"attachment; filename={date.today()}_rsvps.csv"
        writer = csv.writer(response)

        writer.writerow(column_names)
        for obj in queryset:
            writer.writerow(
                [
                    obj.guest.primary_guest.first_name,
                    obj.guest.name,
                    obj.coming,
                    obj.first_course,
                    obj.second_course,
                    obj.note,
                ]
            )

        return response

    export_rsvp_csv.short_description = "Export RSVPs"
