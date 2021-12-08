from django.urls import path

from bartender.views import HomeView, StorageListView

app_name = "bartender"
urlpatterns = [
    path(
        "",
        HomeView.as_view(),
        name="home",
    ),
    path(
        "storage_list",
        StorageListView.as_view(),
        name="storage_list",
    ),
]
