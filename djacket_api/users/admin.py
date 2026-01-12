from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = ["email", "username", "email_verification_sent_at", "email_verified", "last_login"]
    list_filter = ["email_verified", "is_active", "is_staff"]
    search_fields = ["email", "username"]
