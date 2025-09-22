# transactions/serializers.py
from rest_framework import serializers
from transactions.models import TransactionRecord

class TransactionRecordSerializer(serializers.ModelSerializer):
    team_id = serializers.UUIDField(source="team.id", read_only=True)
    player_name = serializers.CharField(source="transaction.player.name", read_only=True)
    team_name = serializers.CharField(source="team.name", read_only=True)
    transaction_no = serializers.CharField(source="transaction.transaction_no", read_only=True)

    class Meta:
        model = TransactionRecord
        fields = [
            "id",
            "transaction_no",
            "transaction_type",
            "amount",
            "player_name",
            "team_id",
            "team_name",
            "created_at",
        ]
