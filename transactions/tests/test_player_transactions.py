from django.test import TestCase
from rest_framework.test import APIClient

from league.tests.factories import PlayerFactory, TeamFactory
from transactions.models import PlayerTransaction, TransactionRecord
from users.tests.factories import UserFactory, UserProfileFactory
from django.urls import reverse
from rest_framework import status
import pytest
from django.db import IntegrityError


class TransferPlayerTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = UserFactory()

        self.profile = UserProfileFactory(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_transactions_created_on_player_transfer(self):
        seller_team = TeamFactory()
        TeamFactory(user_profile=self.profile)
        player = PlayerFactory(team=seller_team, is_for_sale=True)

        url = reverse("players-buy-player", kwargs={"pk": player.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        trx = PlayerTransaction.objects.filter(player=player).first()
        
        self.assertIsNotNone(trx)
        self.assertIsNotNone(trx.transaction_no)
        
        records = TransactionRecord.objects.filter(transaction=trx)
        
        self.assertEqual(records.count(), 2)
        self.assertEqual(
            {r.transaction_type for r in records},
            {"Buy", "Sell"}
        )

    def test_unique_constraint_for_transaction_records(self):

        seller_team = TeamFactory()
        TeamFactory(user_profile=self.profile)
        player = PlayerFactory(team=seller_team, is_for_sale=True)

        url = reverse("players-buy-player", kwargs={"pk": player.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        trx = PlayerTransaction.objects.filter(player=player).first()
        record = trx.transactionrecord_set.first()

        # duplicating TransactionRecord manually
        with pytest.raises(IntegrityError):
            TransactionRecord.objects.create(
                transaction=trx,
                amount=record.amount,
                transaction_type=record.transaction_type,
                team=record.team,
            )

    def test_transaction_str_representation(self):
        seller_team = TeamFactory()
        TeamFactory(user_profile=self.profile)
        player = PlayerFactory(team=seller_team, is_for_sale=True)

        url = reverse("players-buy-player", kwargs={"pk": player.id})
        self.client.post(url)

        trx = PlayerTransaction.objects.get(player=player)
        self.assertEqual(str(trx), f"{trx.transaction_no} - {player}")

        record = trx.transactionrecord_set.first()
        self.assertEqual(str(record), f"{record.transaction_type} - {player} ({record.team})")