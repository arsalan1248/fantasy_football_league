from django.contrib import admin

from core.admin import BaseAdminWithAudit
from transactions.models import PlayerTransaction, TransactionRecord


class TransactionRecordInline(admin.TabularInline):
    model = TransactionRecord
    extra = 0  
    fields = ("team", "amount", "transaction_type") 
    readonly_fields = ("amount", "transaction_type", "team")
    can_delete = False


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
    