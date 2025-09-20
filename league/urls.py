from django.urls import path, include
from rest_framework.routers import DefaultRouter

from league.views import PlayerViewset, TeamViewset


router = DefaultRouter()
router.register(r"team", TeamViewset, basename="teams")
router.register(r"players", PlayerViewset, basename="players")

urlpatterns = [
    path("", include(router.urls)),
]
