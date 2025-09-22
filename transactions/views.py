from rest_framework import permissions, viewsets
from transactions.models import TransactionRecord
from .serializers import TransactionRecordSerializer

class UserTransactionHistoryRecordViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TransactionRecord.objects.filter(
            team__user_profile__user=self.request.user
        ).select_related("transaction", "transaction__player", "team").order_by("-created_at")