from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = ["email", "username", "is_active", "is_staff", "created_at", "last_login"]
    list_filter = ["is_active", "is_staff"]
    list_editable = ["is_active", "is_staff"]
    search_fields = ["email", "username"]
    ordering = ["-created_at"]
