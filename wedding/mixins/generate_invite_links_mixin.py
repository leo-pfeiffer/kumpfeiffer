import csv
from django.utils.http import urlencode
from django.http import HttpResponse


class GenerateInviteLinksMixin:
    def generate_invite_links(self, request, queryset):

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=invite-links.csv"
        writer = csv.writer(response)

        login_url = f"{request.scheme}://{request.get_host()}/login"

        writer.writerow(["Name", "Invite Code", "URL"])
        for obj in queryset:
            if obj.is_superuser:
                continue
            invite_url = f"{login_url}?{urlencode({'inviteCode': obj.username})}"
            writer.writerow([obj.first_name, obj.username, invite_url])

        return response

    generate_invite_links.short_description = "Generate Invite Links"
