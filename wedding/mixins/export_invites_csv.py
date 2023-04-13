import csv

from django.http import HttpResponse


class ExportInvitesCsvMixin:
    def export_invites_csv(self, request, queryset):

        column_names = ["Invite Code", "Name"]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=invites.csv"
        writer = csv.writer(response)

        writer.writerow(column_names)
        for obj in queryset:
            writer.writerow(
                [
                    obj.username,
                    obj.first_name,
                ]
            )

        return response

    export_invites_csv.short_description = "Export Invites"
