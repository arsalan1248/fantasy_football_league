from django.contrib import admin

from core.models import BaseAdminWithAudit
from transactions.models import PlayerTransaction, TransactionRecord


# class TransactionRecordInline(admin.TabularInline):
#     model = TransactionRecord
#     extra = 0  # no extra empty rows
#     readonly_fields = ("amount", "transaction_type", "team")
#     can_delete = False  # optional: prevent deletion from inline
class TransactionRecordInline(admin.TabularInline):
    model = TransactionRecord
    extra = 0  # no extra empty rows
    fields = ("team", "amount", "transaction_type") 
    readonly_fields = ("amount", "transaction_type", "team")  # prevent editing
    can_delete = False
    show_change_link = True  # optional, allows opening the record in full page


@admin.register(PlayerTransaction)
class PlayerTransactionAdmin(BaseAdminWithAudit):
    list_display = (
        "transaction_no",
        "player",
        "is_free_agent_at_transaction",
    )
    search_fields = (
        "transaction_no",
    )
    list_filter = ("player",)
    inlines = [TransactionRecordInline]


@admin.register(TransactionRecord)
class TransactionRecordAdmin(BaseAdminWithAudit):
    list_display = (
        "transaction",
        "team",
        "amount",
        "transaction_type",
        "transaction__is_free_agent_at_transaction"
    )
    search_fields = (
        "transaction_type",
    )
    list_filter = ("team","transaction_type")
    