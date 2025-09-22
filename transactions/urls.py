from django.urls import path, include
from rest_framework.routers import DefaultRouter
from transactions.views import UserTransactionHistoryRecordViewSet

router = DefaultRouter()
router.register(r'transaction-history', UserTransactionHistoryRecordViewSet, basename='transaction-history')

urlpatterns = [
    path("", include(router.urls)),
]
