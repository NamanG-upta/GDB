from django.contrib import admin
from .models import Task,NewUser,helptext
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea

class NewUseradmin(admin.ModelAdmin):
    model = NewUser
    list_filter = ('user', 'institute_name', 'contact')
    list_display = ('user','institute_name', 'contact')

admin.site.register(NewUser,NewUseradmin)

admin.site.register(helptext)

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