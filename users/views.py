from tokenize import generate_tokens
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.jwt_utils import get_tokens_for_user
from users.models import CustomUser, UserProfile
from users.serializers import (
    ResetPasswordSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserRegisterRequestSerializer,
    UserRegisterResponseSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import permissions, status, viewsets


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        user = serializer.save()
        response_serializer = UserRegisterResponseSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            tokens = generate_tokens(user)
            return Response(
                {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                    },
                    "tokens": tokens,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(
            data=request.data, context={"request": request}
        )

        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.validated_data["user"]

        tokens = get_tokens_for_user(user)

        response_data = {
            **tokens,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):

    def post(self, request):
        print(request.data)
        serializer = ResetPasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data["email"]
        current_password = serializer.validated_data["current_password"]
        new_password = serializer.validated_data["new_password"]

        try:
            user = CustomUser.objects.get(email=email, is_active=True)

            if not user.check_password(current_password):
                return Response(
                    {
                        "errors": {
                            "current_password": ["Current password is incorrect."]
                        }
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(new_password)
            user.save()

            return Response(
                {"message": "Password reset successfully."}, status=status.HTTP_200_OK
            )

        except CustomUser.DoesNotExist:
            return Response(
                {"message": "User does not exists"}, status=status.HTTP_404_NOT_FOUND
            )


class UserProfileViewSet(viewsets.ModelViewSet):
    from rest_framework.decorators import action


    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch", "put"]

    # def get_queryset(self):
    #     return UserProfile.objects.filter(user=self.request.user)

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    @action(detail=False, methods=["get", "patch", "put"], url_path="me")
    def me(self, request):
        profile = request.user.profile
        if request.method == "GET":
            serializer = self.get_serializer(profile)
            return Response(serializer.data)

        serializer = self.get_serializer(profile, data=request.data, partial=(request.method == "PATCH"))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)