from django.urls import path, reverse_lazy
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("<int:pk>/", views.UserProfileView.as_view(), name="profile"),
    path("update-profile/", views.UpdateProfileView.as_view(), name="updateprofile"),
    path(
        "update-password/",
        views.UpdatePasswordView.as_view(success_url=reverse_lazy("core:core")),
        name="updatepassword",
    ),
]

