import random
from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from league.models import Team, Player

fake = Faker()


class Command(BaseCommand):
    help = "Generate 20 standard players for an existing team (empty team only)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--team",
            type=str,
            required=True,
            help="The name of the team to assign players to.",
        )

    def handle(self, *args, **options):
        team_name = options["team"]

        try:
            team = Team.objects.get(name=team_name)
        except Team.DoesNotExist:
            raise CommandError(f"Team '{team_name}' does not exist.")

        if not team.can_add_more_players:
            raise CommandError(
                f"Team '{team_name}' already has {team.players.count()} players."
            )

        allocation = team.POSITION_LIMITS

        created_count = 0
        for position, count in allocation.items():
            player_position_count = Player.objects.filter(
                team=team, position=position
            ).count()
            player_allocation_count = count - player_position_count
            for _ in range(player_allocation_count):

                player = Player.objects.create(
                    name=fake.name(),
                    position=position,
                    team=team,
                    is_for_sale=False,
                    value=1000000,
                )
                created_count += 1
                self.stdout.write(
                    self.style.NOTICE(
                        f"Added {player.name} ({player.position}) to {team.name}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully allocated players to team '{team.name}'.")
        )
