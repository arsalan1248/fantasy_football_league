from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from users.views import (
    LoginView,
    ResetPasswordView,
    UserProfileViewSet,
    UserRegisterView,
)

router = DefaultRouter()
router.register(r"profile", UserProfileViewSet, basename="profile")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("token/", LoginView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
]
