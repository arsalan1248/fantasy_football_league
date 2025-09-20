from django.db import models

from core.models import BaseModelWithAudit
from league.models import Player, Team

from django.db import models


class PlayerTransaction(BaseModelWithAudit):
    transaction_no = models.CharField(
        max_length=25, editable=False, db_index=True, unique=True
    )
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="transfers"
    )
    is_free_agent_at_transaction = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        from transactions.utils import generate_transaction_no

        if not self.transaction_no:
            self.transaction_no = generate_transaction_no()

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_no} - {self.player}"


class TransactionRecord(BaseModelWithAudit):
    class TransactionType(models.TextChoices):
        BUY = "Buy"
        SELL = "Sell"

    transaction = models.ForeignKey(PlayerTransaction, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    transaction_type = models.CharField(max_length=6, choices=TransactionType.choices)
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="transactions"
    )

    class Meta:
        verbose_name_plural = "Transaction Records"
        constraints = [
            models.UniqueConstraint(
                fields=["transaction", "team", "transaction_type"],
                name="unique_transaction_team_type",
            )
        ]

    def __str__(self):
        return f"{self.transaction_type} - {self.transaction.player} ({self.team})"
