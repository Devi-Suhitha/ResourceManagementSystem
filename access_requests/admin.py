from django.contrib import admin
from .models import AccessRequest


@admin.register(AccessRequest)
class AccessRequestAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'resource',
        'duration_days',
        'status',
        'requested_at',
    )

    list_filter = (
        'status',
        'resource',
    )

    search_fields = (
        'user__username',
        'resource__name',
        'reason',
    )