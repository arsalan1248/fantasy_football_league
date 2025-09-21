from django.contrib import admin


# Register your models here.
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
