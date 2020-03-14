from django.urls import path
from . import views as core_views

app_name = "core"

urlpatterns = [path("", core_views.HomeView.as_view(), name="core")]
