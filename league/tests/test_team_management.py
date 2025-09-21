from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

from league.tests.factories import PlayerFactory, TeamFactory
from users.tests.factories import UserFactory, UserProfileFactory
from rest_framework import status

User = get_user_model()


class TeamManagementTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "Pass1234!",
        }
        url = reverse("user-register")
        self.registration_response = self.client.post(url, payload)

        self.user = User.objects.get(email="newuser@example.com")
        self.client.force_authenticate(user=self.user)

    def test_create_team(self):
        payload = {"name": "Arsalan's Team"}

        response = self.client.post(reverse("teams-list"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_team(self):
        team = TeamFactory(user_profile=self.user.profile)
        payload = {"name": "Update Team"}

        response = self.client.patch(
            reverse("teams-detail", kwargs={"pk": team.id}), data=payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Update Team")

    def test_cannot_create_duplicate_team_name(self):
        TeamFactory(name="UniqueName")
        payload = {"name": "UniqueName"}
        response = self.client.post(reverse("teams-list"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_create_second_team(self):
        TeamFactory(user_profile=self.user.profile)
        payload = {"name": "Second Team"}
        response = self.client.post(reverse("teams-list"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_cannot_create_team(self):
        client = APIClient()  # no authentication
        payload = {"name": "NoAuth Team"}
        response = client.post(reverse("teams-list"), payload)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_team_properties(self):
        team = TeamFactory(user_profile=self.user.profile)
        PlayerFactory.create_batch(20, team=team)

        self.assertEqual(team.capital, 5000000)
        self.assertEqual(team.players.count(), 20)
        self.assertEqual(team.can_add_more_players, False)
        self.assertEqual(team.total_players_value, 20 * 1000000)


class TestPlayerManagement(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.profile = UserProfileFactory(user=self.user)
        self.client.force_authenticate(user=self.user)
        self.team = TeamFactory(user_profile=self.profile)

    def test_player_default_value(self):
        player = PlayerFactory(team=self.team)
        self.assertEqual(player.value, 1000000)

    def test_filter_by_name(self):
        PlayerFactory(team=self.team, name="Messi")
        PlayerFactory(team=self.team, name="Ronaldo")
        url = reverse("players-list")
        response = self.client.get(url, {"name": "Messi"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data.get("results")[0]["name"], "Messi")

    def test_filter_by_position(self):
        PlayerFactory(team=self.team, position="GK")
        PlayerFactory(team=self.team, position="DEF")
        url = reverse("players-list")
        response = self.client.get(url, {"position": "GK"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            all(p["position"] == "GK" for p in response.data.get("results"))
        )

    def test_filter_by_is_for_sale(self):
        PlayerFactory(team=self.team, is_for_sale=True)
        PlayerFactory(team=self.team, is_for_sale=False)
        url = reverse("players-list")
        response = self.client.get(url, {"is_for_sale": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            all(p["is_for_sale"] is True for p in response.data.get("results"))
        )

    def test_value_cannot_be_updated_via_api(self):
        player = PlayerFactory(team=self.team, is_for_sale=True)
        url = reverse("players-detail", kwargs={"pk": player.id})
        response = self.client.patch(url, {"value": 9999999})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        player.refresh_from_db()
        self.assertEqual(player.value, 1000000)

    def test_mark_player_for_sale(self):
        player = PlayerFactory(team=self.team, is_for_sale=False)
        url = reverse("players-detail", kwargs={"pk": player.id})
        response = self.client.patch(url, {"is_for_sale": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        player.refresh_from_db()
        self.assertTrue(player.is_for_sale)
