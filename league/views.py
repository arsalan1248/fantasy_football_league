import random
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from league.filters import PlayerFilter
from transactions.models import PlayerTransaction, TransactionRecord
from .models import Player, Team
from .serializers import PlayerSerializer, TeamSerializer
from django.http import Http404
from rest_framework.decorators import action
from django.db import transaction


class TeamViewset(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    http_method_names = ["get", "post", "patch"]

    def get_queryset(self):
        return (
            Team.objects.filter(user_profile=self.request.user.profile)
            .select_related("user_profile", "user_profile__user")
            .prefetch_related("players")
        )

    def get_object(self):
        try:
            obj = Team.objects.get(
                id=self.kwargs["pk"], user_profile=self.request.user.profile
            )
            return obj
        except (ValidationError, ValueError) as e:
            from rest_framework.exceptions import ValidationError as DRFValidationError

            raise DRFValidationError(
                {
                    "error": "Invalid team ID format",
                    "detail": f'The provided ID {self.kwargs["pk"]} is not a valid UUID format.',
                    "code": "invalid_uuid",
                }
            )
        except Team.DoesNotExist:
            raise Http404(
                {
                    "error": "Team not found",
                    "detail": f'Team with ID {self.kwargs["pk"]} does not exist or you do not have permission to access it.',
                    "code": "team_not_found",
                }
            )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PlayerViewset(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["value"]
    filterset_class = PlayerFilter


    def get_queryset(self):
        if self.action == "list":
            return Player.active.all()
        return Player.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="buy")
    def buy_player(self, request, pk=None):
        try:
            player = self.get_object()
            buyer_team = self._get_buyer_team(request)
            self._validate_purchase(player, buyer_team)

            if player.team is None:
                bought, response_msg = self._buy_free_agent(player, buyer_team)

            else:
                bought, response_msg = self._buy_for_sale_player(player, buyer_team)

            return Response(
                {"message": response_msg, "player": PlayerSerializer(player).data},
                status=status.HTTP_200_OK if bought else status.HTTP_400_BAD_REQUEST,
            )

        except ValidationError as e:
            return Response(
                {"error": e.detail if hasattr(e, "detail") else str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {"error": "Unexpected error: " + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _get_buyer_team(self, request):
        team = getattr(request.user.profile, "team", None)
        if not team:
            raise ValidationError("Buyer does not have a team.")
        return team

    def _validate_purchase(self, player, buyer_team):
        if not buyer_team.can_add_more_players:
            raise ValidationError("Cannot buy player: team already has maximum number of players.")

        if player.team == buyer_team:
            raise ValidationError("You already own this player.")
        if player.team and not player.is_for_sale:
            raise ValidationError("Player is not for sale.")
        if player.team and player.value > buyer_team.capital:
            raise ValidationError("Insufficient capital to buy this player.")
        
        team_positions_by_type = buyer_team.players.filter(position=player.position).count()
        position_limit = buyer_team.POSITION_LIMITS[player.position]
        if team_positions_by_type >= position_limit:
            raise ValidationError(f"{buyer_team.name} already has {position_limit} {player.get_position_display()}")

    def _buy_free_agent(self, player, buyer_team):
        with transaction.atomic():
            self._create_transaction_records(player, buyer_team)
            self._transfer_player(player, buyer_team, None)

        bought, response_msg = True, "Player successfully bought (free agent)"
        return bought, response_msg
        
    def _buy_for_sale_player(self, player, buyer_team):
        seller_team = player.team
        with transaction.atomic():
            buyer_team.capital -= player.value
            seller_team.capital += player.value
            buyer_team.save()
            seller_team.save()

            self._create_transaction_records(player, buyer_team, seller_team)
            self._transfer_player(player, buyer_team, seller_team)

        bought, response_msg = True, "Player successfully bought"
        return bought, response_msg
        
    def _transfer_player(self, player, buyer_team, seller_team):
        player.team = buyer_team
        player.is_for_sale = False
        player.value = int(player.value * (1 + random.uniform(0.05, 0.15)))
        player.save()

    def _create_transaction_records(self, player, buyer_team, seller_team=None):
        is_free_agent = player.team is None

        transaction = PlayerTransaction.objects.create(
            player=player, is_free_agent_at_transaction=is_free_agent
        )

        TransactionRecord.objects.create(
            transaction=transaction,
            amount=player.value,
            transaction_type=TransactionRecord.TransactionType.BUY,
            team=buyer_team,
        )

        if seller_team:
            TransactionRecord.objects.create(
                transaction=transaction,
                amount=player.value,
                transaction_type=TransactionRecord.TransactionType.SELL,
                team=seller_team,
            )
