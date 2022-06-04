import csv

from django.contrib import admin
from django.forms import forms
from django.shortcuts import redirect, render
from django.urls import path

from wedding.mixins.export_csv_mixin import ExportCsvMixin
from wedding.models import Guest, Allergy, Rsvp


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


@admin.register(Guest)
class UserAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ("name", "email", "invite_code")
    actions = ["export_as_csv"]

    change_list_template = "entities/guests_changelist.html"

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

            # create user object
            for row in rows:
                Guest.objects.create(name=row[0], email=row[1])

            self.message_user(request, "Guest list has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ("guest", "allergy", "note")


@admin.register(Rsvp)
class RsvpAdmin(admin.ModelAdmin):
    list_display = ("guest", "num_guests")
