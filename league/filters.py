import django_filters
from .models import Player


class PlayerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    position = django_filters.ChoiceFilter(choices=Player.PlayerPosition.choices)

    class Meta:
        model = Player
        fields = ["name", "position"]
