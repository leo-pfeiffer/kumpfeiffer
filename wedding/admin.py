from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Q, Count, Sum
from django.forms import forms
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from wedding.mixins.export_csv_mixin import ExportCsvMixin
from wedding.models import Allergy, Rsvp, User, AllergySummary, RsvpSummary

from django.contrib.auth.hashers import make_password

from wedding.utils import generate_invite_code


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
            return queryset\
                .filter(~Q(id__in=rsvp_users))\
                .filter(is_superuser=False)


@admin.register(User)
class UserAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ("name", "invite_code", "email", "has_rsvp", "rsvp")
    list_filter = (HasRsvpFilter, "is_superuser", )
    actions = ["export_as_csv"]

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

    def has_rsvp(self, obj):
        if obj.is_superuser:
            return None
        return Rsvp.objects.filter(guest=obj).exists()

    def rsvp(self, obj):
        if obj.is_superuser:
            return ""
        else:
            rsvp_obj = Rsvp.objects.filter(guest=obj).first()
            has_rsvp = rsvp_obj is not None

            if has_rsvp:
                url = (
                    reverse("admin:wedding_rsvp_changelist") + str(obj.id)
                )
                return format_html('<a href="{}">View</a>', url)
            else:
                return ""

    has_rsvp.boolean = True

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            file = request.FILES["csv_file"]
            file_data = file.read().decode("utf-8")

            rows = file_data.split("\n")
            rows = [row.split(",") for row in rows]

            # assert row before saving
            for row in rows:
                assert len(row) == 2

            # create users
            for row in rows:
                invite_code = generate_invite_code()
                user = User(username=invite_code)
                user.first_name = row[0]
                user.email = row[1]
                user.password = make_password(invite_code)
                user.save()

            self.message_user(request, "Guest list has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ("name", "allergy", "note")

    def name(self, obj):
        return obj.guest.first_name


@admin.register(AllergySummary)
class AllergySummaryAdmin(admin.ModelAdmin):
    change_list_template = "admin/allergy_summary_change_list.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total': Count('id'),
        }

        summary = qs.filter(allergy__isnull=False)\
            .values('allergy')\
            .annotate(**metrics)\
            .order_by('-total')

        response.context_data['summary'] = list(summary)
        response.context_data['total_allergies'] = summary.\
            aggregate(Sum("total"))["total__sum"]

        response.context_data['notes'] = list(
            qs.filter(note__isnull=False).values('allergy', 'note')
        )

        return response


@admin.register(Rsvp)
class RsvpAdmin(admin.ModelAdmin):
    list_display = ("guest", "num_guests")


@admin.register(RsvpSummary)
class RsvpSummaryAdmin(admin.ModelAdmin):
    change_list_template = "admin/rsvp_summary_change_list.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        rsvp_users = Rsvp.objects.values_list("guest_id")
        num_rsvp = User.objects.filter(id__in=rsvp_users).count()
        num_not_rsvp = User.objects.filter(is_superuser=False)\
            .filter(~Q(id__in=rsvp_users)).count()
        guest_count = Rsvp.objects.all().aggregate(Sum("num_guests"))

        response.context_data['summary'] = {
            "Has RSVP'd": num_rsvp,
            "Has not RSVP'd": num_not_rsvp,
            "Guest Count (so far)": guest_count['num_guests__sum']
        }

        return response

