from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "username",
        "email",
        "date_of_birth",
        "phone_number",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + (
        ("Other info", {"fields": ("phone_number", "date_of_birth", "address", "profile_picture")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Other info", {"fields": ("phone_number", "date_of_birth", "address", "profile_picture")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
