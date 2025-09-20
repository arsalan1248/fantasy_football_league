from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.utils import timezone
from django_currentuser.middleware import get_current_authenticated_user
from django.contrib import admin


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class BaseModelWithAudit(BaseModel):
    created_by = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
    )
    updated_by = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )
    deleted_by = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_deleted",
    )
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        user = get_current_authenticated_user()
        if self._state.adding and not self.created_by:
            self.created_by = user
        self.updated_by = user
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Soft delete:
        - mark as deleted
        - set deleted_at
        - set deleted_by
        """
        user = get_current_authenticated_user()
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save(update_fields=["is_deleted", "deleted_at", "deleted_by"])


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    list_per_page = 20


class BaseAdminWithAudit(BaseAdmin):
    base_fields = (
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "deleted_by",
        "deleted_at",
        "is_deleted",
        "is_active",
    )
    base_list_filters = ("is_active", "is_deleted")
    base_readonly_fields = ("created_at", "updated_at", "deleted_at")  # Add this

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        if fieldsets and len(fieldsets) > 0:
            fieldsets[0][1]["fields"] = [
                field
                for field in fieldsets[0][1]["fields"]
                if field not in self.base_fields
            ]

        if not isinstance(fieldsets, list):
            fieldsets = list(fieldsets)

        # Add base fields as readonly in collapsed section
        fieldsets.append(
            (
                "Additional Information",
                {
                    "fields": self.base_fields,
                    "classes": ["collapse"],
                },
            )
        )

        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        return readonly_fields + self.base_readonly_fields
