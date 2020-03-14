from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.

# I can see this "user" in admin pannel and this class will control user
# decorator will be operated if it is located above the classes


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    fieldsets = UserAdmin.fieldsets + (
        (
            "SSIZEN.NET",
            {"fields": ("departure", "order", "kakaotalk", "avatar", "upperuser",)},
        ),
    )

    list_display = (
        "__str__",
        "email",
        "departure",
        "order",
        "kakaotalk",
        "upperuser",
    )


# Combine Django fieldsets and my own fieldsets
