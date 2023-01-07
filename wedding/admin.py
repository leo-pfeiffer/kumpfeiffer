from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Q, Count, Sum
from django.forms import forms
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.html import format_html

from wedding.mixins.export_csv_mixin import ExportCsvMixin
from wedding.mixins.generate_invite_links_mixin import GenerateInviteLinksMixin
from wedding.mixins.generate_qr_codes import GenerateQrCodes
from wedding.mixins.send_reminder_mixin import SendReminderMixin
from wedding.models import Rsvp, User, RsvpSummary, Guest

from wedding.utils import save_guest_list_rows


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class HasRsvpFilter(SimpleListFilter):
    title = "has RSVP"
    parameter_name = "has_rsvp"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Yes"),
            ("no", "No"),
        )

    def queryset(self, request, queryset):
        rsvp_users = Rsvp.objects.values_list("guest_id")
        if self.value() == "yes":
            return queryset.filter(id__in=rsvp_users)
        if self.value() == "no":
            return queryset.filter(~Q(id__in=rsvp_users)).filter(is_superuser=False)


@admin.register(User)
class UserAdmin(
    admin.ModelAdmin,
    ExportCsvMixin,
    SendReminderMixin,
    GenerateInviteLinksMixin,
    GenerateQrCodes,
):
    list_display = (
        "name",
        "invite_code",
        "email",
        "is_rehearsal_guest",
        "has_rsvp",
    )
    list_filter = (
        HasRsvpFilter,
        "is_rehearsal_guest",
        "is_superuser",
    )
    actions = [
        "export_as_csv",
        "generate_invite_links",
        "generate_qr_codes",
        "send_reminder",
    ]

    change_list_template = "entities/guests_changelist.html"

    def name(self, obj):
        if obj.is_superuser:
            return obj.username
        else:
            return obj.first_name

    def invite_code(self, obj):
        if obj.is_superuser:
            return ""
        else:
            return obj.username

    def is_rehearsal_guest(self, obj: User):
        return obj.is_rehearsal_guest

    def has_rsvp(self, obj):
        if obj.is_superuser:
            return None
        return Rsvp.objects.filter(guest__primary_guest=obj).exists()

    has_rsvp.boolean = True

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            file = request.FILES["csv_file"]
            file_data = file.read().decode("utf-8")

            rows = file_data.split("\n")
            rows = [row.split(",") for row in rows]

            # create users
            save_guest_list_rows(rows)

            self.message_user(request, "Guest list has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "admin/csv_form.html", payload)


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ("name", "primary_guest", "rsvp", "has_rsvp")

    def primary_guest(self, obj):
        return obj.primary_guest.first_name

    def name(self, obj):
        return obj.name

    def rsvp(self, obj):
        rsvp_obj = Rsvp.objects.filter(guest=obj).first()
        has_rsvp = rsvp_obj is not None

        if has_rsvp:
            url = reverse("admin:wedding_rsvp_changelist") + str(rsvp_obj.id)
            return format_html('<a href="{}">View</a>', url)
        else:
            return ""

    def has_rsvp(self, obj):
        return Rsvp.objects.filter(guest=obj).exists()


@admin.register(Rsvp)
class RsvpAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "invite_code",
        "coming",
        "first_course",
        "second_course",
        "note",
    )

    def invite_code(self, obj):
        return obj.guest.primary_guest.username

    def name(self, obj):
        return obj.guest.name

    def first_course(self, obj):
        return obj.first_course

    def second_course(self, obj):
        return obj.second_course
