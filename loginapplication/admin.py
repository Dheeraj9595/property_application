from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User

    # Fields to display in the admin list view
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    # Fieldsets for user editing in admin panel
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Roles", {"fields": ("role",)}),
    )

    # Fields for user creation in admin panel
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role", "is_staff", "is_active")}
        ),
    )

    search_fields = ("username", "email")
    ordering = ("username",)

# Register the custom User model
admin.site.register(User, CustomUserAdmin)
