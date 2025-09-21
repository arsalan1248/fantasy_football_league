import factory
from django.test import TestCase
from league.models import Currency, Team, Player
from users.tests.factories import UserProfileFactory
from django.db.models import signals


class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Player

    name = factory.Sequence(lambda n: f"Player {n}")
    team = factory.SubFactory("league.tests.factories.TeamFactory")
    value = 1000000
    currency = Currency.USD
    position = factory.Iterator(
        [
            Player.PlayerPosition.GOALKEEPER,
            Player.PlayerPosition.DEFENDER,
            Player.PlayerPosition.MIDFIELDER,
            Player.PlayerPosition.ATTACKER,
        ]
    )
    is_for_sale = False


@factory.django.mute_signals(signals.pre_save, signals.post_save)
class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    user_profile = factory.SubFactory(UserProfileFactory)
    name = factory.Sequence(lambda n: f"Team {n}")
    capital = 5000000
    currency = "USD"

    @factory.post_generation
    def players(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        for position, count in extracted:
            for i in range(count):
                PlayerFactory(team=self, position=position)
