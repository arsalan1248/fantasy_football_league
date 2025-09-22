from django.test import TestCase
from rest_framework.test import APIClient

from league.tests.factories import PlayerFactory, TeamFactory
from transactions.models import PlayerTransaction, TransactionRecord
from users.tests.factories import UserFactory, UserProfileFactory
from django.urls import reverse
from rest_framework import status
import pytest
from django.db import IntegrityError


class UserTransactionHistoryTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.profile1 = UserProfileFactory(user=self.user1)
        self.profile2 = UserProfileFactory(user=self.user2)
        
        self.client.force_authenticate(user=self.user1)
        
        self.team1 = TeamFactory(user_profile=self.profile1)
        self.team2 = TeamFactory(user_profile=self.profile2)
        
        self.player = PlayerFactory(team=self.team2)
        self.txn = PlayerTransaction.objects.create(player=self.player)
        
        self.sell_record = TransactionRecord.objects.create(
            transaction=self.txn,
            amount=1000000,
            transaction_type=TransactionRecord.TransactionType.SELL,
            team=self.team2
        )
        self.buy_record = TransactionRecord.objects.create(
            transaction=self.txn,
            amount=1000000,
            transaction_type=TransactionRecord.TransactionType.BUY,
            team=self.team1
        )

    def test_authenticated_user_sees_only_their_transactions(self):
        url = reverse('transaction-history-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]['team_id'], str(self.team1.id))
        self.assertEqual(response.data["results"][0]['transaction_type'], 'Buy')

    def test_unauthenticated_user_cannot_access(self):
        self.client.force_authenticate(user=None)
        url = reverse('transaction-history-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ordering_by_created_at(self):
        txn2 = PlayerTransaction.objects.create(player=self.player)
        TransactionRecord.objects.create(
            transaction=txn2,
            amount=2000000,
            transaction_type=TransactionRecord.TransactionType.BUY,
            team=self.team1
        )

        url = reverse('transaction-history-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(
            response.data["results"][0]['transaction_no'],
            txn2.transaction_no
        )

    def test_response_structure_contains_team_name_and_id(self):
        url = reverse('transaction-history-list')
        response = self.client.get(url)
        record = response.data["results"][0]
        self.assertIn('team_name', record)
        self.assertIn('id', record)
        self.assertIn('team_id', record)
        self.assertIn('transaction_type', record)
        self.assertIn('amount', record)