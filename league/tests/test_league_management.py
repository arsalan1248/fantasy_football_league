from django.test import TestCase
from rest_framework.test import APIClient

from league.tests.factories import PlayerFactory, TeamFactory
from users.tests.factories import UserFactory, UserProfileFactory
from django.urls import reverse
from rest_framework import status


class TransferPlayerTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = UserFactory()

        self.profile = UserProfileFactory(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_successful_transfer(self):
        seller_team = TeamFactory()
        buyer_team = TeamFactory(user_profile=self.profile)
        player = PlayerFactory(team=seller_team, is_for_sale=True)

        url = reverse("players-buy-player", kwargs={"pk": player.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        player.refresh_from_db()
        seller_team.refresh_from_db()
        buyer_team.refresh_from_db()

        self.assertEqual(player.team, buyer_team)
        self.assertEqual(buyer_team.capital, 4000000)
        self.assertEqual(seller_team.capital, 6000000)
        self.assertTrue(player.value > 1000000)
        self.assertCountEqual(player.transfers.count(), 1)

        trx = player.transfers.first()
        self.assertCountEqual(trx.transactionrecord_set.count(), 2)

    def test_cannot_buy_own_player(self):
        team = TeamFactory(user_profile=self.profile)
        player = PlayerFactory(team=team, is_for_sale=True, value=1000000)

        url = reverse("players-buy-player", kwargs={"pk": player.id})
        response = self.client.post(url, {"buyer_team": team.id})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["error"][0]), "You already own this player.")

    def test_insufficient_funds(self):
        seller_team = TeamFactory(capital=5000000)
        buyer_team = TeamFactory(user_profile=self.profile, capital=100000)
        player = PlayerFactory(team=seller_team, is_for_sale=True, value=1000000)

        url = reverse("players-buy-player", kwargs={"pk": player.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data["error"][0]), "Insufficient capital to buy this player."
        )

    def test_already_sold_player(self):
        seller_team = TeamFactory(capital=5000000)
        buyer_team = TeamFactory(user_profile=self.profile, capital=5000000)
        player = PlayerFactory(team=seller_team, is_for_sale=False, value=1000000)

        url = reverse("players-buy-player", kwargs={"pk": player.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["error"][0]), "Player is not for sale.")

    def test_cannot_exceed_max_team_size(self):
        seller_team = TeamFactory(capital=5000000)
        buyer_team = TeamFactory(user_profile=self.profile, capital=5000000)

        PlayerFactory.create_batch(20, team=buyer_team)

        player = PlayerFactory(team=seller_team, is_for_sale=True, value=1000000)

        url = reverse("players-buy-player", kwargs={"pk": player.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data["error"][0]),
            "Cannot buy player: team already has maximum number of players.",
        )

    def test_cannot_exceed_position_limit(self):
        seller_team = TeamFactory(capital=5000000)
        TeamFactory(
            user_profile=self.profile, capital=5000000, players=[("GK", 3), ("DEF", 6)]
        )

        player = PlayerFactory(
            team=seller_team, is_for_sale=True, value=1000000, position="DEF"
        )

        url = reverse("players-buy-player", kwargs={"pk": player.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already has", str(response.data["error"][0]))
