from django.contrib import admin
from .models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'resource_type',
        'owner',
        'is_active',
        'created_at'
    )

    list_filter = (
        'resource_type',
        'is_active'
    )

    search_fields = (
        'name',
        'description'
    )