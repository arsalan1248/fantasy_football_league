from django.contrib import admin

from core.models import BaseAdminWithAudit
from league.models import Player, Team


@admin.register(Team)
class TeamAdmin(BaseAdminWithAudit):
    list_display = (
        "name",
        "user_profile",
        "capital",
        "currency",
        "total_players_value",
    )
    search_fields = (
        "name",
        "user_profile__user__username",
        "user_profile__display_name",
    )
    list_filter = ("currency",)
    readonly_fields = ("total_players_value",)


@admin.register(Player)
class PlayerAdmin(BaseAdminWithAudit):
    list_display = ("name", "position", "team", "value", "is_for_sale", "is_active")
    list_filter = ("position", "is_for_sale", "is_active", "team")
    search_fields = ("name", "team__name")
    readonly_fields = ("value",)
