from django.urls import path, include

from core.views import home_view

app_name = "core"
urlpatterns = [
    path(
        "",
        home_view,
        name="home",
    ),
]
