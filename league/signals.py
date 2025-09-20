# teams/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Player, Team
from faker import Faker
from django.db import transaction

@receiver(post_save, sender=Team)
def create_initial_team_players(sender, instance, created, **kwargs):
    if created:
        fake = Faker()
        allocation = instance.POSITION_LIMITS

        players_to_create = []
        for position, count in allocation.items():

            # player_allocation_count = count - player_position_count
            for _ in range(count):
                players_to_create.append(
                    Player(
                        name=fake.name(),
                        position=position,
                        team=instance,
                        is_for_sale=False,
                        value=1000000,
                    )
                )

        with transaction.atomic():
            Player.objects.bulk_create(players_to_create)
                
