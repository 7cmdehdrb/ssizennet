from django.urls import path, reverse_lazy
from . import views

app_name = "reservations"

urlpatterns = [
    path("reservation/", views.MakeReservationView.as_view(), name="makereservation"),
    path(
        "instantreservation/",
        views.InstantReservationView.as_view(),
        name="instantreservation",
    ),
    path("list/", views.ReservationListView.as_view(), name="reservationlist"),
    path(
        "confirmlist/",
        views.ConfirmRevervationListView.as_view(),
        name="confirmreservationlist",
    ),
    path("<int:pk>/", views.ReservationDetailView.as_view(), name="reservationdetail"),
    path(
        "update-acception/<int:pk>/",
        views.UpdateAcceptView.as_view(),
        name="updateacception",
    ),
    path(
        "update-reservation-from-before-to-now/<int:pk>/",
        views.UpdateReservationNowView.as_view(),
        name="updatereservationnow",
    ),
    path(
        "update-reservation-from-now-to-finish/<int:pk>/",
        views.UpdateReservationFinishView.as_view(),
        name="updatereservationfinish",
    ),
    path(
        "confirm-instant-reservation/<int:pk>/",
        views.InstantReservationConfirmView.as_view(),
        name="confirminstantreservation",
    ),
    path(
        "delete/<int:pk>/",
        views.ReservationDeleteView.as_view(),
        name="reservationdelete",
    ),
    path(
        "reservation-change/<int:pk>/",
        views.ReservationChangeView.as_view(),
        name="reservationchange",
    ),
    path(
        "update-instant-reservation/<int:pk>/",
        views.InstantReservationChangeView.as_view(),
        name="instantreservationchange",
    ),
]

