from django.urls import path

from bartender.views import HomeView

app_name = "bartender"
urlpatterns = [
    path(
        "",
        HomeView.as_view(),
        name="home",
    ),
]
