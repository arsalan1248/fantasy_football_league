from league.models import Player, Team
from rest_framework import serializers


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "name", "position", "value", "currency", "is_for_sale"]
        read_only_fields = ["id", "value", "currency", "name"]

    def validate_position(self, value):
        if value not in [choice.value for choice in Player.PlayerPosition]:
            raise serializers.ValidationError("Dont have this position")
        return value


class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    total_players = serializers.IntegerField(source="players.count", read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "capital",
            "currency",
            "total_players",
            "total_players_value",
            "players",
        ]
        read_only_fields = ["id", "capital", "currency", "total_players_value"]

    def validate(self, values):
        request = self.context.get("request")
        if not request or not hasattr(request.user, "profile"):
            raise serializers.ValidationError(
                {"user_profile": "A valid user profile is required to create a team."}
            )
        
        if hasattr(request.user.profile, "team"):
            raise serializers.ValidationError(
                {"user_profile": "This user already has a team."}
            )

        return values

    def create(self, validated_data):
        request = self.context.get("request")

        validated_data["user_profile"] = request.user.profile
        return super().create(validated_data)
