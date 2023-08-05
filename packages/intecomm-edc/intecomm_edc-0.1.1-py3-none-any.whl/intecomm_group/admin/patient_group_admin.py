from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from intecomm_form_validators import DISSOLVED, IN_FOLLOWUP

from intecomm_screening.admin.modeladmin_mixins import BaseModelAdminMixin

from ..admin_site import intecomm_group_admin
from ..forms import PatientGroupForm
from ..models import PatientGroup


@admin.register(PatientGroup, site=intecomm_group_admin)
class PatientGroupAdmin(BaseModelAdminMixin):

    """Modeladmin for patient groups in follow-up or dissolved.

    See `get_queryset`"""

    form = PatientGroupForm

    show_object_tools = True
    change_list_template: str = "intecomm_group/admin/patientgroup_change_list.html"
    show_save_next = False
    show_cancel = True

    fieldsets = (
        (
            None,
            {"fields": ("report_datetime", "name", "patients", "status", "notes")},
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "__str__",
        "opened",
        "status",
        "meetings",
        "members",
        "user_created",
        "created",
    )

    list_filter = (
        "status",
        "randomized",
        "report_datetime",
        "randomized_datetime",
    )

    search_fields = (
        "name",
        "patients__name",
    )

    filter_horizontal = ("patients",)

    radio_fields = {
        "status": admin.VERTICAL,
    }

    readonly_fields = (
        "report_datetime",
        "name",
        "status",
        "randomized",
        "randomized_datetime",
        "patients",
    )

    @admin.display(description="Opened", ordering="report_datetime")
    def opened(self, obj=None):
        return obj.report_datetime.date()

    @admin.display(description="Meetings")
    def meetings(self, obj=None):
        name = "+".join(obj.name.split(" "))
        url = reverse("intecomm_prn_admin:intecomm_group_patientgroupmeeting_changelist")
        url = f"{url}?q={name}"
        return format_html(f'<a href="{url}">Meetings</a>')

    @admin.display(description="Members")
    def members(self, obj=None):
        cnt = obj.patients.all().count()
        url = reverse("intecomm_prn_admin:intecomm_prn_patientlog_changelist")
        url = f"{url}?q={obj.name}"
        return format_html(f'<a href="{url}">{cnt} patients</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status__in=[IN_FOLLOWUP, DISSOLVED])
