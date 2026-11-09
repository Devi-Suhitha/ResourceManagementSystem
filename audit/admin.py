from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        'access_request',
        'action',
        'performed_by',
        'timestamp',
    )

    list_filter = (
        'action',
        'timestamp',
    )

    search_fields = (
        'access_request__user__username',
        'access_request__resource__name',
        'performed_by__username',
    )

    ordering = (
        '-timestamp',
    )