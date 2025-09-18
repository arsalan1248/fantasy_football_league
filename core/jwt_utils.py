from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


def get_tokens_for_user(user):
    if not user or not user.is_active:
        raise ValueError("Cannot generate tokens for an inactive")

    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def get_user_from_token(token_string):

    try:
        token = AccessToken(token_string)
        user_id = token["user_id"]
        User = get_user_model()
        return User.objects.get(id=user_id, is_active=True)
    except (TokenError, User.DoesNotExist):
        return None


def decode_access_token(token):

    return AccessToken(token)
