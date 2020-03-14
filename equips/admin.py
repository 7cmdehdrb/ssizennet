from django.contrib import admin
from . import models

# Register your models here.


# @admin.register(models.Equiptype)
# class ItemAdmin(admin.ModelAdmin):

#     list_display = ("name",)


@admin.register(models.Equip)
class EquipAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "serial_number",
        "equiptype",
        "enable",
    )

    list_filter = (
        "equiptype",
        "enable",
    )
