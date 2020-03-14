from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):

    """ Reservation admin define """

    list_display = (
        "lender",
        "purpose",
        "catagory",
        "check_in",
        "check_out",
        "accept",
        "instant_boolean",
        "reserv_code",
    )

    list_filter = (
        "accept",
        "status",
        "check_in",
        "check_out",
        "catagory",
    )

    filter_horizontal = ("equipment",)

    search_fields = [
        "lender__username",
        "purpose",
    ]
