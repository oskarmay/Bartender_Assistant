from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from core.views import ChangePasswordView, CustomLoginView, HomeTemplateView

app_name = "core"
urlpatterns = [
    path(
        "",
        HomeTemplateView.as_view(),
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
