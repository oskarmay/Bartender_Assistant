from django.contrib.auth import views as auth_views
from django.urls import path

from core.views import HomeView, CustomLoginView, ChangePasswordView

app_name = "core"
urlpatterns = [
    path(
        "",
        HomeView.as_view(),
        name="home",
    ),
    path(
        "login/",
        CustomLoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
]
