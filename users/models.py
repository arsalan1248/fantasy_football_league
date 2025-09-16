from django.db import models
from django.contrib.auth.models import AbstractUser

from core.models import BaseModelWithAudit


# Create your models here.
class CustomUser(AbstractUser, BaseModelWithAudit):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    @property
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class UserProfile(BaseModelWithAudit):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile"
    )
    display_name = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        "Profile Picture", upload_to="profile_picture/", null=True, blank=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
