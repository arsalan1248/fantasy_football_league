from django.db import models

from core.models import BaseModelWithAudit
from league.managers import ActivePlayerManager
from users.models import UserProfile


class Currency(models.TextChoices):
    USD = "USD", "US Dollar"
    PKR = "PKR", "Pakistani Rupee"


class Team(BaseModelWithAudit):

    POSITION_LIMITS = {
        "GK": 3,
        "DEF": 6,
        "MID": 6,
        "ATT": 5,
    }

    user_profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="team"
    )
    name = models.CharField(max_length=50, unique=True)
    capital = models.PositiveBigIntegerField(default=5000000)
    currency = models.CharField(
        max_length=3, choices=Currency.choices, default=Currency.USD
    )

    @property
    def total_players_value(self):
        return self.players.aggregate(total=models.Sum("value"))["total"] or 0

    @property
    def can_add_more_players(self):
        return self.players.count() < 20

    def __str__(self):
        return self.name


class Player(BaseModelWithAudit):
    class PlayerPosition(models.TextChoices):
        GOALKEEPER = "GK", "Goalkeeper"
        DEFENDER = "DEF", "Defender"
        MIDFIELDER = "MID", "Midfielder"
        ATTACKER = "ATT", "Attacker"

    name = models.CharField(max_length=50)
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="players"
    )
    value = models.PositiveBigIntegerField(default=1000000)
    currency = models.CharField(
        max_length=3, choices=Currency.choices, default=Currency.USD
    )
    position = models.CharField(max_length=3, choices=PlayerPosition.choices)
    is_for_sale = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActivePlayerManager()

    class Meta:
        indexes = [
            models.Index(fields=["team", "position"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.position}"
