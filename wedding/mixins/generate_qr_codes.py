from django.utils.http import urlencode
from django.http import HttpResponse

from wedding.qr_codes import generate_qr_code, zip_images


class GenerateQrCodes:
    def generate_qr_codes(self, request, queryset):

        base_url = f"{request.scheme}://{request.get_host()}"

        data = []

        for obj in queryset:
            if obj.is_superuser:
                continue

            invite_url = f"{base_url}?{urlencode({'inviteCode': obj.username})}"

            qr_code = generate_qr_code(invite_url, obj.username)

            data.append(
                {
                    "url": invite_url,
                    "code": obj.username,
                    "name": obj.first_name,
                    "image": qr_code,
                }
            )

        zipped = zip_images(data)

        response = HttpResponse(zipped, content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=qr-codes.zip"

        return response

    generate_qr_codes.short_description = "Generate QR Codes"
