from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "desc",
        "complete",
        "user",
        "board_id",
        "ip_address",
    )

    list_filter = (
        "user",
        "board_id",
        "complete",
    )

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser


admin.site.register(Task, TaskAdmin)