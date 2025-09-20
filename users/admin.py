from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.admin import BaseAdminWithAudit
from users.models import CustomUser, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )
    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name",
    )


@admin.register(UserProfile)
class UserProfileAdmin(BaseAdminWithAudit):
    list_display = (
        "user__username",
        "user",
    )
    search_fields = (
        "user__username",
        "user__email",
    )
