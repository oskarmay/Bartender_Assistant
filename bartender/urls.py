from django.urls import path

from bartender.views import (
    HomeView,
    StorageListView,
    IngredientCreateView,
    IngredientUpdateView,
)

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
    path(
        "storage_list/add_ingredient",
        IngredientCreateView.as_view(),
        name="add_ingredient",
    ),
    path(
        "storage_list/<int:pk>/update_ingredient",
        IngredientUpdateView.as_view(),
        name="update_ingredient",
    ),
]
