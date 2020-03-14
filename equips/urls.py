from django.urls import path
from . import views

app_name = "equips"

urlpatterns = [
    path("list/", views.EquipView.as_view(), name="equiplist"),
    path("list/<int:pk>/", views.EquipDetail.as_view(), name="detail"),
]

